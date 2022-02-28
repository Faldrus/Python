import pygame
import pickle       #mi permette di caricare dati da un file
import sys
from pygame import mixer
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)               #pre configurazione di default
mixer.init()
pygame.init()

WIDTH=1000
HEIGHT=1000
WHITE=(255, 255, 255)
BLUE=(0,0,255)

clock=pygame.time.Clock()                               #variabile per tenere traccia del tempo
FPS=60

screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer')                #nome della finestra

#definisco il fonte
font_score=pygame.font.SysFont('Bauhaus 93', 30)        #(font, dimensione)
font=pygame.font.SysFont('Bauhaus 93', 70)

#variabili di gioco
tile_size=50
game_over=0
main_menu=True                                          #il gioco inizia nel menù
level=0
max_levels=7
score=0

#carico immagini
sun_img=pygame.image.load('Platform/img/sun.png')
bg_img=pygame.image.load('Platform/img/sky.png')
restart_img=pygame.image.load('Platform/img/restart_btn.png')
start_img=pygame.image.load('Platform/img/start_btn.png')
exit_img=pygame.image.load('Platform/img/exit_btn.png')

#carico i suoni
pygame.mixer.music.load('Platform/img/music.wav')       #canzone di background
pygame.mixer.music.play(-1, 0.0, 5000)                  #do il delay di 5000
coin_fx=pygame.mixer.Sound('Platform/img/coin.wav')
coin_fx.set_volume(0.5)                                 #riduco il volume perché sarebbe troppo forte
jump_fx=pygame.mixer.Sound('Platform/img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx=pygame.mixer.Sound('Platform/img/game_over.wav')
game_over_fx.set_volume(0.5)

#metodo per scrivere sul gioco
def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)               #trasforma il testo in un'immagine
    screen.blit(img, (x,y))

#metodo per resettare i livelli
def reset_level(level):
    player.reset(100, HEIGHT-130)
    blob_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()                                  #devo resettare tutti gli elementi nel gioco altrimenti continuo ad aggiungerne di nuovi
    
    #ricarico il livello
    if path.exists(f'Platform/level{level}_data'):                  #controllo se la path esiste
        pickle_in=open(f'Platform/level{level}_data', 'rb')         #carico il livello {level}                      
        world_data=pickle.load(pickle_in)
    world=World(world_data)
    
    return world

class Button():
    def __init__(self, x, y, image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False                          #controllo se ho già cliccato qualcosa
        
    def draw(self):
        action=False                                #variabile che tiene conto se faccio un'azione o meno
        #guardo dov'è il cursore
        pos=pygame.mouse.get_pos()                  #metodo che mi da dove sta il mio mouse
        
        #controllo gli eventi del mouse
        if self.rect.collidepoint(pos):              #controllo le collisioni tra il rettangolo del bottone e il punto dato dal mio mouse
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:    #controlla quale pulsante dle mouse è stato premuto, crea una lista di 0 e 1 in abse a quello che è stato premuto
                action=True
                self.clicked=True                   #non posso più cliccare il tasto però rimane bloccato così e non posso più ricliccare perché non lo resseto
                
                
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False                      #resetto la variabile clicked
        
        #disegno i pulsanti
        screen.blit(self.image, self.rect)          #l'immagine da aggiornare le coordinate da aggiornare sono nel rettangolo

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x,y)
    
    def update(self, game_over):
        dx=0
        dy=0
        walk_cooldown=5
        col_thresh=20           #offest tra testa e il basso della piattaforma                          
        
        if game_over==0:                                #tutto il gioco avviene solo se game_over==0
            #gestisco gli eventi
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped==False and self.in_air==False:  #se premo spazio e non ho saltato e non sono già in aria
                jump_fx.play()
                self.vel_y=-15                          #gravità sul salto
                self.jumped=True                        #saltato
            if key[pygame.K_SPACE]==False:
                self.jumped=False
            if key[pygame.K_LEFT]:
                dx-=5
                self.counter+=1
                self.direction=-1
            if key[pygame.K_RIGHT]:
                dx+=5
                self.counter+=1
                self.direction=1
            if key[pygame.K_LEFT]==False and key[pygame.K_RIGHT]==False:        #ritorno all'animazione iniziale quando mi fermo
                self.counter=0
                self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction==-1:
                    self.image=self.images_left[self.index]
            
            #gestisco le animazioni del giocatore              
            if self.counter>walk_cooldown:
                self.counter=0
                self.index+=1                                   #scorro tra le animazioni
                if self.index>=len(self.images_right):          #se supero le animazioni, torno all'inizio
                    self.index=0
                if self.direction==1:                           #se sto andando a destra scorro tra le immagini destre
                    self.image=self.images_right[self.index] 
                if self.direction==-1:                          #se sto andando a sinistra scorro tra le immagini sinistre
                    self.image=self.images_left[self.index]
            
            #aggiungo la gravità
            self.vel_y+=1                                       #la gravità aumenta
            if self.vel_y>10:
                self.vel_y=10
            dy+=self.vel_y
            
            #collisioni
            self.in_air=True
            for tile in world.tile_list:
                #controllo le collisioni in x
                if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                    dx=0
                #controllo le collisioni in y
                if tile[1].colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):   #creo una hitbox ulteriore con l'aggiunta di dy, per sapere se il cambiamento andrà a collidere
                    #controllo se collide in basso o in alto
                    if self.vel_y<0:                            #salto(l'asse y è flippato)
                        dy=tile[1].bottom-self.rect.top         #dy diventa la differenza tra il basso del quadrato e la testa dell'hitbox, così da poter avere una collisione più accurata
                        self.vel_y=0                            #se c'è una collisione, la velocità torna a 0
                    elif self.vel_y>=0:    #caduta
                        dy=tile[1].top-self.rect.bottom
                        self.vel_y=0
                        self.in_air=False                       #effettua una collisione col basso, quindi non è più in aria
                        
            #collisioni con nemici
            if pygame.sprite.spritecollide(self, blob_group, False):  #controlla le collisioni tra me, tutti i blob e False è "doKill" e cancella se avviene la collisione
                game_over=-1
                game_over_fx.play()
                
            #collisioni con lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over=-1
                game_over_fx.play()
            
            #collisione con porta
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over=1
            
            #collisioni con le piattaforme
            for platform in platform_group:
                #collisioni in x
                if platform.rect.colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                    dx=0        #non mi posso più muovere lateralmente
                #collisioni in y
                if platform.rect.colliderect(self.rect.x, self.rect.y+dy, self.width, self.height):
                    #controllo se sono sotto la piattaforma
                    if abs((self.rect.top+dy)-platform.rect.bottom)<col_thresh:
                        self.vel_y=0                    #se sbatte la testa si ferma 
                        dy=platform.rect.bottom-self.rect.top
                    #controllo se sono sopra la piattaforma
                    elif abs((self.rect.bottom+dy)-platform.rect.top)<col_thresh:
                        self.rect.bottom=platform.rect.top-1          #semplicemente dico che il basso del giocatore corrisponde all'alto della piattaforma però mi da una collisione costante e quindi non posso muovermi mentre sale
                                                        #per rimediare metto il giocatore 1 pixel più in alto, così non ho una collisione costante
                        self.in_air=False
                        dy=0
                    #movimento orizzontale quando sono su una piattaforma orizzontale(altrimenti cadrebbe e basta in quanto il giocatore rimane fermo ma la piattaforma si muove)
                    if platform.move_x!=0:
                        self.rect.x+=platform.move_direction    #se la piattaforma si muove orizzontalmente, anche la posizione del giocatore si aggiornerà

            #aggiorno le coordinate del giocatore
            self.rect.x+=dx
            self.rect.y+=dy
            
            """#controllo le collisioni
            if self.rect.bottom>HEIGHT:
                self.rect.bottom=HEIGHT
                dy=0                            Non più necessario in quanto controllo le collisioni con le celle
            """
        elif game_over==-1:
            self.image=self.dead_image              #cambio l'immagine dal movimento al personaggio morto
            draw_text('GAME OVER!', font, BLUE, WIDTH//2-200, HEIGHT//2)
            if self.rect.y>200:                     #pongo il limite sennò va su all'infinito
                self.rect.y-=5
        
        #funzione per disegnare il giocatore
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, WHITE, self.rect, 2)      #creo l'hitbox del giocatore

        return game_over
        
    def reset(self, x, y):                          #metodo che resetta il giocare allo stato iniziale
        self.images_right=[]                        #lista di frame di immagini
        self.images_left=[]
        self.index=0    
        self.counter=0                              #variabile per controllare la velocità con cui l'animazione cambia
        for num in range(1,5):
            img_right=pygame.image.load(f'Platform/img/guy{num}.png')
            img_right=pygame.transform.scale(img_right, (40, 80))
            img_left=pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image=pygame.image.load('Platform/img/ghost.png') 
        self.image=self.images_right[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.vel_y=0  #velocità di salto
        self.jumped=False   #variabile per tenere traccia se ha saltato, così da non farlo saltare all'infinito
        self.direction=0    #direzione in cui sta andando il giocatore
        self.in_air=True    #variabile che tiene conto se il giocatore sta saltando o meno
        
class World():
    def __init__(self, data):
        self.tile_list=[]
        
        #load images
        dirt_img=pygame.image.load('Platform/img/dirt.png')
        grass_img=pygame.image.load('Platform/img/grass.png')
        
        row_count=0
        for row in data:
            col_count=0
            for tile in row:
                if tile==1:#terra
                    img=pygame.transform.scale(dirt_img, (tile_size, tile_size))        #ridimensiono l'immagine per farla stare nella cella
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size                                     #devo contare in che posizione sono per poterlo disegnare poi
                    img_rect.y=row_count*tile_size
                    tile=(img, img_rect)
                    self.tile_list.append(tile) #list per tenere traccia degli elementi, trascurando 0
                
                if tile==2:#erba
                    img=pygame.transform.scale(grass_img, (tile_size, tile_size))        #ridimensiono l'immagine per farla stare nella cella
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size                                     #devo contare in che posizione sono per poterlo disegnare poi
                    img_rect.y=row_count*tile_size
                    tile=(img, img_rect)
                    self.tile_list.append(tile) #list per tenere traccia degli elementi, trascurando 0    
                
                if tile==4:#piattaforma mobile orizzontale
                    platform=Platform(col_count*tile_size, row_count*tile_size, 1, 0)
                    platform_group.add(platform)

                if tile==5:#piattaforma mobile verticale
                    platform=Platform(col_count*tile_size, row_count*tile_size, 0, 1)
                    platform_group.add(platform)

                if tile==3:#blob
                    blob=Enemy(col_count*tile_size, row_count*tile_size+15)         #il +15 mi serve per centrarli e farli appoggiare sulla piattaforma
                    blob_group.add(blob)
                    
                if tile==6:#lava
                    lava=Lava(col_count*tile_size, row_count*tile_size+(tile_size//2))  #devo alzarlo di metà tile per farlo stare nella metà inferiore
                    lava_group.add(lava)
                    
                if tile==7:#monete
                    coin=Coin(col_count*tile_size+(tile_size//2), row_count*tile_size+(tile_size//2))
                    coin_group.add(coin)
                    
                if tile==8:#porta
                    exit=Exit(col_count*tile_size, row_count*tile_size-(tile_size//2))  #devo alzarlo di metà 
                    exit_group.add(exit)
                    
                col_count+=1
            row_count+=1
    
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, WHITE, tile[1], 2)
          
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('Platform/img/blob.png')
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_direction=1                               #tengo conto in che direzione vanno
        self.move_counter=0                                 #tengo conto di quanto si sono spostati
           
    def update(self):                                       #metodo per far muovere i blob
        self.rect.x+=self.move_direction
        self.move_counter+=1                                #continuo ad aggiornare la variabile spostamento
        if abs(self.move_counter)>50:                            #se supero 50, cambio direzione "resetto" la variabile che tiene conto degli spostamenti
            self.move_direction*=-1
            self.move_counter*=-1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Platform/img/platform.png')
        self.image=pygame.transform.scale(img, (tile_size, tile_size//2))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_counter=0             #conto quante volte si è spostata la piattaforma
        self.move_direction=1           #direzione in cui va
        self.move_x=move_x              #per differenziare le piattaforme
        self.move_y=move_y              #che si muovono orizzontalmente o verticalmente
    
    def update(self):                                       #uguale al metodo per far muovere i blob
        self.rect.x+=self.move_direction*self.move_x        #moltiplicando per quella variabile, decido in che direzione si muovono le piattaforme
        self.rect.y+=self.move_direction*self.move_y
        self.move_counter+=1                                #continuo ad aggiornare la variabile spostamento
        if abs(self.move_counter)>50:                            #se supero 50, cambio direzione "resetto" la variabile che tiene conto degli spostamenti
            self.move_direction*=-1
            self.move_counter*=-1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Platform/img/lava.png')
        self.image=pygame.transform.scale(img, (tile_size, tile_size//2))   #la lava sarà grande solo metà tile
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Platform/img/coin.png')
        self.image=pygame.transform.scale(img, (tile_size//2, tile_size//2))   #la lava sarà grande solo metà tile
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('Platform/img/exit.png')
        self.image=pygame.transform.scale(img, (tile_size, tile_size*1.5))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

player=Player(100, HEIGHT-130)

blob_group=pygame.sprite.Group()                                        #crea una specie di lista in cui poter creare i nemici
platform_group=pygame.sprite.Group()
lava_group=pygame.sprite.Group()
coin_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()

score_coin=Coin(tile_size//2, tile_size//2)
coin_group.add(score_coin)

#carico i livelli e creo il mondo
if path.exists(f'Platform/level{level}_data'):                          #controllo se la path esiste
    pickle_in=open(f'Platform/level{level}_data', 'rb')                 #carico il livello 1                      
    world_data=pickle.load(pickle_in)
world=World(world_data)

#creo i bottoni
restart_button=Button(WIDTH//2-67, HEIGHT//2+100, restart_img)          #qui lo chiamo ma non lo disegno
start_button=Button(WIDTH//2-350, HEIGHT//2, start_img)
exit_button=Button(WIDTH//2+150, HEIGHT//2, exit_img)

while True:
    
    clock.tick(FPS)
    
    screen.blit(bg_img, (0, 0))                                         #aggiorna una porzione di schermo
    screen.blit(sun_img, (100, 100))                                    #vanno messe in ordine
    
    if main_menu:                                                       #se sono nel menù disegno solo i due bottoni
        if start_button.draw():
            main_menu=False
        if exit_button.draw():                                          #se clicco il bottone exit, chiudo il gioco e fine
            sys.exit()
    else:                                                               #se invece non lo sono, inizia il gioco e tutto il resto
        world.draw()
        
        if game_over==0:                                                #il gioco finisce di aggiornarsi se finisce il gioco
            blob_group.update()                                         #aggiorna tutti i blob
            platform_group.update()
            #aggiorno il punteggio controllando se la moneta è stata presa
            if pygame.sprite.spritecollide(player, coin_group, True):   #metto true perché voglio che una volta che la moneta viene presa, la elimino
                score+=1
                coin_fx.play()
            draw_text('X '+str(score), font_score, WHITE, tile_size-10, 10)
        
        blob_group.draw(screen)                                         #le classi sprite non hanno bisogno di un draw implementato
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        
        game_over=player.update(game_over)
        
        #se il giocatore muore
        if game_over==-1:                                               #se il gioco finisce, compare il tasto e se effettuo l'azione clicca sul tasto
            if restart_button.draw():                                   #il giocatore torna al punto iniziale e il gioco riprende
                world_data=[]
                world=reset_level(level)
                game_over=0
                score=0

        #se il giocatore ha completato il livello
        if game_over==1:
            level+=1
            if level<=max_levels:           #vado avanti con i livelli se ce ne sono altri
                #resetto il livello
                world_data=[]               #pulisco la lista
                world=reset_level(level)    #metodo che resetta il livello e inizia il livello successivo
                game_over=0                 #il gioco riparte
            else:                           #altrimenti il gioco riparte
                draw_text('YOU WIN', font, BLUE, (WIDTH//2)-147, HEIGHT//2)
                if restart_button.draw():
                    level=0
                    world_data=[]
                    world=reset_level(level)
                    game_over=0
                    score=0
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
           
    pygame.display.update()                                         #serve ad aggiornare tutto il display
pygame.quit()