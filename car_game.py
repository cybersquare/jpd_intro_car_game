import pygame
from pygame.locals import *
import random, time

#Initializing
pygame.init()

collided = False
score = 0

#Setting up FPS to limit the number of executions per second
FPS = 60 # Execute the loop 60 times a second
FramePerSec = pygame.time.Clock()

#Creating colors 
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

#Create a white screen  
screen = pygame.display.set_mode((400,600))
SCREEN_WIDTH = 600
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite): # Enemy car(Red)
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.png")
        self.surf = pygame.Surface((50, 80))
        self.rect = self.surf.get_rect(center = (random.randint(40, 360),0))     
 
    def move(self):
        global collided
        global score
        if collided: # Pause the game for 2 second if collided
            time.sleep(2)
        self.rect.move_ip(0,10)
        # Start a new enemy if collided or crosses the window
        if self.rect.bottom > 600 or collided: 
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
            collided = False
            score += 1
        
    def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Player(pygame.sprite.Sprite): # Player car(Blue)
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.surf = pygame.Surface((50, 100))
        self.rect = self.surf.get_rect(center = (150, 500))

    def update(self): # Move player on keypress
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     
 
#Setting up Sprites        
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

while True:     
    # Quit game on pressing the close button
    for event in pygame.event.get():              
        if event.type == pygame.QUIT:
            pygame.quit()

    P1.update()
    E1.move()
    screen.fill(WHITE)
    
    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        screen.fill(RED)
        collided = True
        score = 0
        
    P1.draw(screen)
    E1.draw(screen)
    
    # Display score
    font = pygame.font.Font(None, 24)
    scoretext = font.render('Score: '+str(score), True, (0,0,0))
    textRect = scoretext.get_rect()
    textRect.topleft=[20,10]
    screen.blit(scoretext, textRect)

    pygame.display.update()
    FramePerSec.tick(FPS) 
