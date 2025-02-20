import pygame
import random

WIDTH = 1000
HEIGHT = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
bg = pygame.image.load("sky.png")
bg = pygame.transform.scale(bg, (1000,800))
ground = pygame.image.load("ground.png")
ground = pygame.transform.scale(ground, (2000,168))
ground_x = 0
bird1 = pygame.image.load("bird1.png")
bird2 = pygame.image.load("bird2.png")
bird3 = pygame.image.load("bird3.png")
flying = True
game = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
class pipe(pygame.sprite.Sprite):
    def __init__ (self, x,y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect() 
        if dir == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = x,y - (pipe_gap/2)
        if dir == -1 :
            self.rect.topleft = x,y + (pipe_gap/2)
    def update (self):
        self.rect.x -= 5
        if self.rect.right < 0:
           self.kill()
class Bird(pygame.sprite.Sprite):
    def __init__ (self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [bird1, bird2, bird3]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.velocity = 0
        self.clicked = False
    def update(self):
        if flying == True:
            self.velocity += 0.3
            if self.velocity >8:
                self.velocity = 8
            if self.rect.bottom <750:
                self.rect.y += self.velocity    
        if game == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False :
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index += 1
                if self.index >= 3:
                    self.index = 0
            self.image = self.images[self.index] 
bird_group = pygame.sprite.Group()              
flappy = Bird(50,400) 
bird_group.add (flappy)
pipe_group = pygame.sprite.Group()

run = True 
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game == False :
            flying = True
    clock.tick(60)
    screen.fill("sky blue")
    screen.blit(bg, (0,0))
    screen.blit(ground, (ground_x,650))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    if flappy.rect.bottom > 950:
        game = True 
        flying = False
    if game == False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint( -100,100)
            bottom_pipe = pipe(WIDTH,HEIGHT/2+pipe_height, -1)
            top_pipe = pipe(WIDTH,HEIGHT/2+pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        ground_x -= 2
        if abs(ground_x) > 50:
            ground_x = 0
        pipe_group.update()
    pygame.display.update()
    
