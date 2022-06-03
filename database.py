import sqlite3
import pygame as pg

WIDTH = 800
HEIGHT = 576

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 250, 64)


class DB:
    login = ""
    connection = sqlite3.connect('users.sqlite')
    cursor = connection.cursor()

    @staticmethod
    def authorisation():
        DB.cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                       name TEXT,
                       result INT);
                        """)
        DB.connection.commit()
        DB.cursor.execute(f"SELECT name FROM users WHERE name = '{DB.login}'")
        if DB.cursor.fetchone() is None:
            print("This user does not exist")
            DB.cursor.execute(f"INSERT INTO users VALUES (?, ?)", (DB.login, 0))
            DB.connection.commit()
        elif DB.cursor.execute(f"SELECT name FROM users WHERE name = '{DB.login}'") != DB.cursor.fetchone() is None:
            info = DB.cursor.fetchall()
            score = info[1]

            return score

    @staticmethod
    def draw_field():
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        font = pg.font.Font(None, 32)
        clock = pg.time.Clock()
        input_box = pg.Rect(300, 250, 140, 32)
        color_inactive = pg.Color(GREEN)
        color_active = pg.Color(RED)
        color = color_inactive
        active = False
        text = ''

        done = False
        while not done:
            caption = font.render('Who are you?', True, RED)
            screen.blit(caption, (320, 200))
            pg.display.update()
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            done = True
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill(BLACK)
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pg.draw.rect(screen, color, input_box, 2)

            pg.display.flip()
            clock.tick(160)
        DB.login = text
        score = DB.authorisation()
        return score

    @staticmethod
    def update_score(win):
        DB.cursor.execute(f"SELECT * FROM users WHERE name = '{DB.login}'")
        info = DB.cursor.fetchall()[0]
        score = info[1]
        if win > score:
            DB.cursor.execute(f"Update users set result = '{win}' where name = '{DB.login}'")
        DB.connection.commit()
        return score
