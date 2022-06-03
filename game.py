from player import Player
from enemies import *
from view import Menu
from database import DB

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 250, 64)


class Game(object):
    enemy = 6

    def __init__(self):
        self.game_over = True
        self.score = 0
        self.font = pygame.font.Font(None, 50)
        self.menu = Menu(("Start", "Enemies", "Exit"), font_color=WHITE, font_size=60)
        self.menu_enemies = Menu(("Noob", "Just a man", "God"), font_color=WHITE, font_size=60)
        self.player = Player(32, 128, "player.png")
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        self.dots_group = pygame.sprite.Group()

        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8, i*32+8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8, i*32+8, BLACK, 16, 16))

        self.enemies = pygame.sprite.Group()
        Slime.create_enemies(self, Game.enemy)

        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12, i*32+12, WHITE, 8, 8))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DB.update_score(self.score)
                return False
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over:
                        if self.menu.state == 0:
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            Game.enemy = Slime.number_of_enemies()
                            Slime.create_enemies(self, Game.enemy)
                        elif self.menu.state == 2:
                            DB.update_score(self.score)
                            return False

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True

        return True

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)

            if len(block_hit_list) > 0:
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)

            if len(block_hit_list) > 0:
                self.player.explosion = True
            self.game_over = self.player.game_over
            DB.update_score(self.score)
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks)

    def display_frame(self, screen):
        screen.fill(BLACK)

        if self.game_over:
            self.menu.display_frame(screen)
            caption = self.font.render('Your score is: ' + str(DB.update_score(self.score)), True, GREEN)
            screen.blit(caption, (280, 80))
            pygame.display.update()
            pygame.display.flip()
        else:
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            text = self.font.render("Score: " + str(self.score), True, GREEN)
            screen.blit(text, [120, 20])
            pygame.display.flip()
