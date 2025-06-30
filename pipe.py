import pygame as pg
import random

LIM_UP, LIM_DOWN = 500, 280

class Pipe:
    def __init__(self, speed):
        # Load original images
        original_img_down = pg.image.load("flappy bird/pillar.png").convert_alpha()
        original_img_up = pg.image.load("flappy bird/pillar.png").convert_alpha()

        scale_factor = 0.7
        new_size = (
            int(original_img_down.get_width() * scale_factor),
            int(original_img_down.get_height() * scale_factor)
        )

        self.imgDown = pg.transform.scale(original_img_down, new_size)
        self.imgUp = pg.transform.scale(original_img_up, new_size)

        # Set up rectangles
        self.rectUp = self.imgUp.get_rect()
        self.rectDown = self.imgDown.get_rect()
        self.pipeDist = 200

        self.rectUp.y = random.randint(LIM_DOWN, LIM_UP)
        self.rectDown.y = self.rectUp.y - self.pipeDist - self.rectDown.height
        self.rectDown.x = self.rectUp.x = 550

        self.movingSpeed = speed

    def drawPipe(self, win):
        win.blit(self.imgUp, self.rectUp)
        win.blit(self.imgDown, self.rectDown)

    def update(self, dt):
        self.rectUp.x -= self.movingSpeed * dt
        self.rectDown.x -= self.movingSpeed * dt
