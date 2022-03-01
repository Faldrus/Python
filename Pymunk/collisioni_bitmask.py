import pygame
import pymunk
import random
import winsound

WIDTH=600
HEIGHT=600

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
ORANGE=(255,165,0)
BLACK=(0,0,0)
WHITE=(255,255,255)

pygame.init()                                                       #devo inizializzare pygame

display=pygame.display.set_mode((WIDTH,HEIGHT))                     #creo una finestra 800x800
clock=pygame.time.Clock()                                           #oggetto clock
space=pymunk.Space()                                                #l'oggetto che contiene tutto quello che riguarda la fisica
FPS=80

def convert_coordinates(point):                                     #funzione per convertire le coordinate da pymunk a pygame
    return int(point[0]), HEIGHT-int(point[1])

class Ball():
    def __init__(self, x, color, category, mask, velocity):
        self.color=color
        self.body=pymunk.Body()
        self.body.position=(x, 500)
        self.body.velocity=velocity
        self.shape=pymunk.Circle(self.body, 15)
        self.shape.density=1
        self.shape.elasticity=1
        self.shape.filter=pymunk.ShapeFilter(categories=category, mask=mask)
        space.add(self.body, self.shape)

    def draw(self):
        pos=self.body.position
        pygame.draw.circle(display, self.color, convert_coordinates(pos), 15)

class Platform():
    def __init__(self, y, color, category):
        self.color=color
        self.y=y
        self.body=pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position=(0, y)
        self.shape=pymunk.Segment(self.body, (0, 0), (600, 0), 10)
        self.shape.density=1
        self.shape.elasticity=1
        self.shape.filter=pymunk.ShapeFilter(categories=category)       #gli oggetti dello stesso gruppo non interagiscono tra di loro
        space.add(self.body, self.shape)
    
    def draw(self):
        a=convert_coordinates(self.body.local_to_world(self.shape.a))
        b=convert_coordinates(self.body.local_to_world(self.shape.b))
        pygame.draw.line(display, self.color, a, b, 10)

def game():
    ball_1=Ball(150, RED, 1, 21, (100, 0))
    ball_2=Ball(300, GREEN, 2, 22, (10, 0))
    ball_3=Ball(450, BLUE, 4, 31, (0,0))
    platform1=Platform(300, BLACK, 8)
    platform2=Platform(100, ORANGE, 16)

    while True:                                                     #qui dentro farò tutto quello che voglio
        for event in pygame.event.get():                            #controllo tutti gli eventi
            if event.type==pygame.QUIT:
                return                                              #chiudo la finestra
        display.fill(WHITE)

        ball_1.draw()
        ball_2.draw()
        ball_3.draw()
        platform1.draw()
        platform2.draw()

        pygame.display.update()                                     #aggiorno la finestra
        clock.tick(FPS)                                             #frequenza di aggiornamento
        space.step(1/FPS)                                           #il tempo nello spazio

game()
pygame.quit()                                                       #devo chiudere pygame

"""
ESEMPIO BITMASK
Oggetto        |Bit per categoria |Numero corrispondente |Con chi può collidere?                                |Bit    |Numero |
---------------------------------------------------------------------------------------------------------------------------------
Red ball       |           00001  |                    1 |Blue ball, orange platform                            | 10101 |    21 |
Green ball     |           00010  |                    2 |Blue ball, orange platform                            | 10110 |    22 |
Blue ball      |           00100  |                    4 |Orange platform, black platform, green ball, red ball | 11111 |    31 |
Black platform |           01000  |                    8 |                                                      | 11111 |    31 |
Orange platform|           10000  |                   16 |                                                      | 11111 |    31 |
                                    ^ Numero categoria                                                                   ^ Numero maschera
"""