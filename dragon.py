import pygame as pg
MAX_FALL_SPEED = 200  # px/s

class Dragon(pg.sprite.Sprite):
    def __init__(self, ):
        super(Dragon,self).__init__()
        img1_raw = pg.image.load("flappy bird/d1.png").convert_alpha()
        img2_raw = pg.image.load("flappy bird/d2.png").convert_alpha()

        # Scale images to 0.1 of original size
        scale_factor = 0.1
        self.img1 = pg.transform.rotozoom(img1_raw, 0, 0.09*1.14)
        self.img2 = pg.transform.rotozoom(img2_raw, 0,0.1*1.14)

        # Set initial image
        self.img = self.img1
        self.rect = self.img.get_rect(center=(125, 200))

        self.gravity=9
        self.V=0#initial velocity in y direction
        self.flapV=200

        self.animation_time = 0.2  # seconds per frame
        self.time_since_last_frame = 0
        self.current_frame = 0  # 0 → img1, 1 → img2


    def updateDragon(self,dt):
        self.applyGravity(dt)
        self.animate(dt)
        if self.rect.y<=0:
            self.rect.y=1
            self.V=0

    def applyGravity(self,dt):
        self.V += self.gravity * dt
        if self.V > MAX_FALL_SPEED:
            self.V = MAX_FALL_SPEED

        self.rect.y += self.V

    
    def fly(self,dt):
        self.V-=self.flapV*dt

    def animate(self, dt):
        # Update timer
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_time:
            self.time_since_last_frame = 0

            # Toggle frame
            if self.current_frame == 0:
                self.img = self.img2
                self.current_frame = 1
            else:
                self.img = self.img1
                self.current_frame = 0
        