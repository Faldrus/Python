import pygame
import pymunk

WIDTH=800
HEIGHT=800

pygame.init()                                                       #devo inizializzare pygame

display=pygame.display.set_mode((WIDTH, HEIGHT))                     #creo una finestra 800x800
clock=pygame.time.Clock()                                           #oggetto clock
space=pymunk.Space()                                                #l'oggetto che contiene tutto quello che riguarda la fisica
space.gravity=(0, -1000)                                            #imposto la gravità (gravità su x, gravità su y)
FPS=80

def convert_coordinates(point):                                     #funzione per convertire le coordinate da pymunk a pygame
    return point[0], HEIGHT-point[1]

ball_radius=10
#image=pygame.image.load("nomeimmagine.png")                    per inserire un'immagine al posto della palla
#image=pygame.transform.scale(image,(ball_radius*2, ball_radius*2)) converto l'immagine e la faccio più piccola e la trasformo da quadrato a cerchio

class Ball():                                                       #classe palla
    def __init__(self, x=400):                                             #costruttore, self. indica attributi della classe
        self.body=pymunk.Body()                                     #creo un corpo puntiforme(non ha massa nè densità)
        self.body.position=(x,600)                                #lo metto la centro, (0,0) è l'angolo in basso a sinistra, pymunk vuole dei float
        #devo impostare una massa e una densità perché pymunk lo richiede
        self.shape=pymunk.Circle(self.body, ball_radius)            #definisco il corpo
        self.shape.density=1
        self.shape.elasticity=1                                     #imposto l'elasticità della palla
        space.add(self.body, self.shape)                            #li aggiungo allo spazio
    
    def draw(self):
        x,y=convert_coordinates(self.body.position)
        pygame.draw.circle(display, (255,0,0), (int(x), int(y)), ball_radius)
                                                                    #mentre qui pygame vuole degli interi, se cambio le coordinate non saranno come le aspetto
                                                                    #perché per pygame (0,0) è l'angolo in alto a sinistra
        #display.blit(image,(int(x)-ball_radius,int(y)-ball_radius))#aggiorno solo lo schermo intorno alla palla

class Floor():
    def __init__(self):
        self.body=pymunk.Body(body_type=pymunk.Body.STATIC)         #creo un corpo statico
        self.shape=pymunk.Segment(self.body, (0,250), (800,50), 5)  #definisco il segmento che va da (0,50) a (800,50) con spessore 5
        self.shape.elasticity=1                                     #imposto l'elasticità della base
        space.add(self.body, self.shape)                          

    def draw(self):
        pygame.draw.line(display,(0,0,0), (0,550), (800,750),5)     #pygame fa lo spessore 5 in alto e 5 in basso



def game():
    ball=Ball()
    ball_2=Ball(200)
    floor=Floor()
    while True:                                                     #qui dentro farò tutto quello che voglio
        for event in pygame.event.get():                            #controllo tutti gli eventi
            if event.type==pygame.QUIT:
                return                                              #chiudo la finestra
        display.fill((255,255,255))                                 #ogni loop ridisegno lo sfondo
        
        ball.draw()
        ball_2.draw()
        floor.draw()

        pygame.display.update()                                     #aggiorno la finestra
        clock.tick(FPS)                                             #frequenza di aggiornamento
        space.step(1/FPS)                                           #il tempo nello spazio

game()
pygame.quit()                                                       #devo chiudere pygame