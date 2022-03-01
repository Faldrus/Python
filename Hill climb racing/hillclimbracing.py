from email.quoprimime import body_check
from lib2to3.pytree import convert
import pygame
import pymunk
import random

WIDTH=800
HEIGHT=800
RED=(255,0,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)

pygame.init()                                                       #devo inizializzare pygame

display=pygame.display.set_mode((WIDTH,HEIGHT))                     #creo una finestra 800x800
clock=pygame.time.Clock()                                           #oggetto clock
space=pymunk.Space()                                                #l'oggetto che contiene tutto quello che riguarda la fisica
space.gravity=(0, -1000)
FPS=60

def convert_coordinates(point):                                     #funzione per convertire le coordinate da pymunk a pygame
    return int(point[0]), HEIGHT-int(point[1])


ball_radius=10
class Ball():
    def __init__(self, x=WIDTH/2, y=100):
        self.body=pymunk.Body()
        self.body.position=(x,y)
        self.shape=pymunk.Circle(self.body, ball_radius)
        self.shape.density=1
        self.shape.elasticity=1
        space.add(self.body, self.shape)
    
    def draw(self, x=WIDTH/2, y=100):
        x,y=convert_coordinates(self.body.position)
        pygame.draw.circle(display, RED, (x, y), ball_radius)

class Floor():
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape=pymunk.Segment(self.body, x, y, 5)
        self.shape.elasticity=0.5
        space.add(self.body, self.shape)
        
    def draw(self):
        pygame.draw.line(display, BLACK, convert_coordinates(self.x), convert_coordinates(self.y), 5)
        

def game():
    floor=Floor((0,50),(800,50))
    ball=Ball()
    
    while True:                                                     #qui dentro farò tutto quello che voglio
        for event in pygame.event.get():                            #controllo tutti gli eventi
            if event.type==pygame.QUIT:
                return                                              #chiudo la finestra

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==ord('a'):
                    ball.draw(ball.x+1, ball.y)
        
        
        display.fill(WHITE)

        floor.draw()
        ball.draw()

        pygame.display.update()                                     #aggiorno la finestra
        clock.tick(FPS)                                             #frequenza di aggiornamento
        space.step(1/FPS)                                           #il tempo nello spazio

game()
pygame.quit()   