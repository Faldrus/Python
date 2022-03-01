from lib2to3.pytree import convert
import pygame
import pymunk
import random
import winsound

WIDTH=600
HEIGHT=600
RED=(255,0,0)
BLUE=(0,0,255)
BLACK=(0,0,0)
WHITE=(255,255,255)

pygame.init()                                                       #devo inizializzare pygame

display=pygame.display.set_mode((WIDTH,HEIGHT))                     #creo una finestra 800x800
clock=pygame.time.Clock()                                           #oggetto clock
space=pymunk.Space()                                                #l'oggetto che contiene tutto quello che riguarda la fisica
space.gravity=0, -1000
FPS=80

def convert_coordinates(point):                                     #funzione per convertire le coordinate da pymunk a pygame
    return int(point[0]), HEIGHT-int(point[1])

ball_radius=10
class Ball():
    def __init__(self, x, y):
        self.body=pymunk.Body()
        self.body.position=(x,y)
        self.shape=pymunk.Circle(self.body, ball_radius)
        self.shape.density=1
        self.shape.elasticity=1
        space.add(self.body, self.shape)
    def draw(self):
        pygame.draw.circle(display, RED, convert_coordinates(self.body.position), ball_radius)

class String():
    def __init__(self, body1, attachment, identifier="body"):
        self.body1=body1

        if identifier=="body":
            self.body2=attachment
        elif identifier=="position":
            self.body2=pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position=attachment

        joint=pymunk.PinJoint(self.body1, self.body2)
        space.add(joint)

    def draw(self):
        pos1=convert_coordinates(self.body1.position)
        pos2=convert_coordinates(self.body2.position)

        pygame.draw.line(display, BLACK, pos1, pos2, 5)

def game():
    ball_1=Ball(450, 450)
    ball_2=Ball(200, 150)

    string_1=String(ball_1.body, (300, 550), "position")
    string_2=String(ball_2.body, ball_1.body)
    while True:                                                     #qui dentro farò tutto quello che voglio
        for event in pygame.event.get():                            #controllo tutti gli eventi
            if event.type==pygame.QUIT:
                return                                              #chiudo la finestra
        display.fill(WHITE)
        
        ball_1.draw()
        ball_2.draw()
        string_1.draw()
        string_2.draw()

        pygame.display.update()                                     #aggiorno la finestra
        clock.tick(FPS)                                             #frequenza di aggiornamento
        space.step(1/FPS)                                           #il tempo nello spazio

game()
pygame.quit()                                                       #devo chiudere pygame