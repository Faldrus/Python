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
FPS=80

def convert_coordinates(point):                                     #funzione per convertire le coordinate da pymunk a pygame
    return int(point[0]), HEIGHT-int(point[1])

ball_radius=10
class Ball():
    def __init__(self, x, y, collision_type, up=1):
        self.body=pymunk.Body()
        self.body.position=(x,y)
        self.body.velocity=(random.uniform(-50, 50), random.uniform(-50, 50))
        #self.body.velocity=(0, up*100)
        self.shape=pymunk.Circle(self.body, ball_radius)
        self.shape.elasticity=1
        self.shape.density=1
        self.shape.collision_type=collision_type
        space.add(self.body, self.shape)
    
    def draw(self):
        if self.shape.collision_type!=2:
            pygame.draw.circle(display, RED, convert_coordinates(self.body.position), ball_radius)
        else:
            pygame.draw.circle(display, BLUE, convert_coordinates(self.body.position), ball_radius)
    
    def change_to_blue(self, arbiter, space, data):
        self.shape.collision_type=2
        winsound.PlaySound("Pymunk/boii.wav", winsound.SND_ASYNC)

def collide(arbiter, space, data):                                  #argomenti che richiede pymunk
    #winsound.PlaySound("Boii.wav", winsound.SND_ASYNC)
    print("hello")                                                  #farà qquesto quando collidono
    return True

def game():
    balls=[Ball(random.randint(0,WIDTH), random.randint(0,HEIGHT), i+3) for i in range(100)]
    balls.append(Ball(400,400, 2))

    handlers=[space.add_collision_handler(2,i+3) for i in range(100)]
    for i, handler in enumerate(handlers):
        handler.separate=balls[i].change_to_blue

    while True:                                                     #qui dentro farò tutto quello che voglio
        for event in pygame.event.get():                            #controllo tutti gli eventi
            if event.type==pygame.QUIT:
                return                                              #chiudo la finestra
        display.fill(WHITE)
        
        [ball.draw() for ball in balls]
        
        pygame.display.update()                                     #aggiorno la finestra
        clock.tick(FPS)                                             #frequenza di aggiornamento
        space.step(1/FPS)                                           #il tempo nello spazio

game()
pygame.quit()                                                       #devo chiudere pygame