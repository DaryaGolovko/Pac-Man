from draw import *
from view import Menu
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, change_x, change_y):
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        self.image = pygame.image.load("slime.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, horizontal_blocks, vertical_blocks):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

        if self.rect.topleft in self.get_intersection_position():
            direction = random.choice(("left", "right", "up", "down"))
            if direction == "left" and self.change_x == 0:
                self.change_x = -2
                self.change_y = 0
            elif direction == "right" and self.change_x == 0:
                self.change_x = 2
                self.change_y = 0
            elif direction == "up" and self.change_y == 0:
                self.change_x = 0
                self.change_y = -2
            elif direction == "down" and self.change_y == 0:
                self.change_x = 0
                self.change_y = 2

    @staticmethod
    def get_intersection_position():
        items = []
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 3:
                    items.append((j * 32 + 8, i * 32))

        return items

    @staticmethod
    def number_of_enemies():
        enemy = 0
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Settings")
        menu_enemies = Menu(("Noob", "", "Just a man", "", "God"), font_color=(255, 255, 255), font_size=60)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                menu_enemies.event_handler(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if menu_enemies.state == 0:
                            enemy = 4
                        elif menu_enemies.state == 2:
                            enemy = 6
                        elif menu_enemies.state == 4:
                            enemy = 8
                        running = False
                menu_enemies.event_handler(event)

            pygame.display.update()
            menu_enemies.display_frame(screen)
        return enemy

    @staticmethod
    def create_enemies(self, number):
        self.enemies.add(Slime(290, 96, 0, 2))
        self.enemies.add(Slime(290, 320, 0, -2))
        self.enemies.add(Slime(546, 128, 0, 2))
        self.enemies.add(Slime(34, 224, 0, 2))

        if number == 6:
            self.enemies.add(Slime(162, 64, 2, 0))
            self.enemies.add(Slime(450, 64, -2, 0))
        elif number == 8:
            self.enemies.add(Slime(162, 64, 2, 0))
            self.enemies.add(Slime(450, 64, -2, 0))
            self.enemies.add(Slime(642, 448, 2, 0))
            self.enemies.add(Slime(450, 320, 2, 0))
