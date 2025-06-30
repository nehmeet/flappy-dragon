import pygame as pg
import sys,time
from dragon import Dragon
from pipe import Pipe

HEIGHT,WHIDTH=768,512
PIPE_SPEED=50
SPEED=90
pg.init()

class Game:
    def __init__(self):
        self.width=WHIDTH
        self.height=HEIGHT
        self.speed=SPEED
        self.win=pg.display.set_mode((self.width,self.height))
        self.bg_img=pg.image.load("flappy bird/bg.jpeg").convert()
        self.clock=pg.time.Clock()
        self.isEnterPressed=False
        self.bird=Dragon()
        self.score = 0
        self.font = pg.font.SysFont("Arial", 40, bold=True)
        self.pipes=[]
        self.pipecounter=275
        self.game_over = False
        self.replay_button_rect = pg.Rect(self.width // 2 - 75, self.height // 2 + 50, 150, 50)

        self.setupBG()
        self.gameLoop()

    def reset(self):
        self.bird = Dragon()
        self.pipes = []
        self.score = 0
        self.pipecounter = 275
        self.isEnterPressed = False
        self.game_over = False


    def gameLoop(self):
        last_time=time.time()
        while True:
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_RETURN:
                        self.isEnterPressed=True
                    
                    if event.key==pg.K_SPACE:
                        self.bird.fly(dt)


            self.draw()
            self.update(dt)
            if event.type == pg.MOUSEBUTTONDOWN and self.game_over:
                if self.replay_button_rect.collidepoint(event.pos):
                    self.reset()

            pg.display.update()
            self.clock.tick(60)

    def update(self, dt):
        if self.isEnterPressed:
            self.gimg1_rect.x -= self.speed * dt
            self.gimg2_rect.x -= self.speed * dt

            if self.gimg1_rect.x + self.gimg1_rect.width < 0:
                self.gimg1_rect.x = self.gimg2_rect.x + self.gimg2_rect.width

            if self.gimg2_rect.x+ self.gimg2_rect.width < 0:
                self.gimg2_rect.x = self.gimg1_rect.x + self.gimg1_rect.width

            if self.pipecounter==275:
                self.pipes.append(Pipe(PIPE_SPEED))
                self.pipecounter=0
            
            if len(self.pipes) !=0:
                if self.pipes[0].rectUp.right<0:
                    self.pipes.pop(0)

            self.pipecounter+=1
            
            for pipe in self.pipes:
                pipe.update(dt)
                if not hasattr(pipe, "scored") and pipe.rectUp.right < self.bird.rect.left:
                    self.score += 1
                    pipe.scored = True

            self.gimg1_rect.x = int(self.gimg1_rect.x)
            self.gimg2_rect.x = int(self.gimg2_rect.x)
            self.bird.updateDragon(dt)
        
        self.checkCollision()

        

    def draw(self):
        self.win.blit(self.bg_img, (0, 0))

        for pipe in self.pipes:
            pipe.drawPipe(self.win)

        self.win.blit(self.gimg1, self.gimg1_rect)
        self.win.blit(self.gimg2, self.gimg2_rect)
        self.win.blit(self.bird.img, self.bird.rect)

        # Score
        score_surf = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.win.blit(score_surf, (20, 20))

        # Instructions if game not started
        if not self.isEnterPressed and not self.game_over:
            msg1 = self.font.render("Press ENTER to start", True, (255, 255, 0))
            msg2 = self.font.render("Press SPACE to fly", True, (255, 255, 0))
            self.win.blit(msg1, (self.width // 2 - msg1.get_width() // 2, self.height // 2 - 60))
            self.win.blit(msg2, (self.width // 2 - msg2.get_width() // 2, self.height // 2 - 20))

        # Game Over screen
        if self.game_over:
            over_msg = self.font.render("Game Over!", True, (255, 0, 0))
            self.win.blit(over_msg, (self.width // 2 - over_msg.get_width() // 2, self.height // 2 - 100))

            pg.draw.rect(self.win, (0, 200, 0), self.replay_button_rect)
            replay_text = self.font.render("Replay", True, (255, 255, 255))
            self.win.blit(
                replay_text,
                (self.replay_button_rect.centerx - replay_text.get_width() // 2,
                self.replay_button_rect.centery - replay_text.get_height() // 2)
            )



    def setupBG(self):
        self.gimg1=pg.image.load('flappy bird/ground-removebg-preview.png').convert_alpha()
        self.gimg2=pg.image.load('flappy bird/ground-removebg-preview.png').convert_alpha()

        self.gimg1 = pg.transform.scale(self.gimg1, (600, 220))  # (width, height)

        self.gimg2 = pg.transform.scale(self.gimg2, (600, 220))

        self.gimg1_rect=self.gimg1.get_rect()
        self.gimg2_rect=self.gimg1.get_rect()
        
        self.gimg1_rect.x=0
        self.gimg2_rect.x=self.gimg1_rect.right
        self.gimg1_rect.y=575
        self.gimg2_rect.y=575


    def checkCollision(self):
        if len(self.pipes):
            pipe_up = self.pipes[0].rectUp
            pipe_down = self.pipes[0].rectDown

            # Buffer values (you can tweak these)
            pipe_buffer_x = 75   # pipe horizontal buffer
            pipe_buffer_y = 175  # pipe vertical buffer
            bird_buffer = 50     # bird buffer on all sides

            # Shrink the UP pipe's collision box
            shrunk_up_rect = pg.Rect(
                pipe_up.x + pipe_buffer_x,
                pipe_up.y,
                pipe_up.width - 2 * pipe_buffer_x,
                pipe_up.height - pipe_buffer_y
            )

            # Shrink the DOWN pipe's collision box
            shrunk_down_rect = pg.Rect(
                pipe_down.x + pipe_buffer_x,
                pipe_down.y + pipe_buffer_y,
                pipe_down.width - 2 * pipe_buffer_x,
                pipe_down.height - pipe_buffer_y
            )

            # Shrink bird’s rect
            bird_collision_rect = self.bird.rect.inflate(-bird_buffer, -bird_buffer)

            # Check for collision
            if (bird_collision_rect.colliderect(shrunk_up_rect) or
                bird_collision_rect.colliderect(shrunk_down_rect)):
                self.isEnterPressed = False
                self.game_over = True

        # Ground collision
        if self.bird.rect.bottom >= 675:
            self.bird.rect.bottom = 675
            self.isEnterPressed = False
            self.game_over = True




        

mygame=Game()