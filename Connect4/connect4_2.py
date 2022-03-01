from tkinter.tix import COLUMN
import numpy as np
import pygame
import sys
import math

BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

ROW_COUNT=6
COLUMN_COUNT=7

def create_board():
    board=np.zeros((ROW_COUNT,COLUMN_COUNT))                       #creo una tabell 6 righe x 7 colonne piene di 0
    return board

def drop_piece(drop, row, col, piece):
    board[row][col]=piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0                   #posso inserire se la colonna non è piena

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):                  #controllo tutte le righe di uan colonna 
        if board[r][col]==0:                    #se la riga della colonna è vuota, ritorno la riga trovata
            return r

def print_board(board):                         #stampa la tabella al contrario(numpy considera 0,0 in alto a sinistra)
    print(np.flip(board, 0))                    #flippo la tabella rispetto all'asse x(0)

def winning_move(board, piece):                 #implemento la condizione di vittoria
    #controllo le vittorie orizzontali
    for c in range(COLUMN_COUNT-3):             #tolgo le ultime 3 colonne perché non mi permettono di vincere, quindi non le controllo
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True

    #controllo le vittorie verticali
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):       
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True

    #controllo le diagonali "positive"
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):       
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True

    #controllo le diagonali "negative"
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):           #inizia dalla riga 3 al massimo       
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))   #disegno un rettangolo blu sulla finestra posizionato in c,r*SQUARESIZE con dimensione SQUARESIZExSQUARSIZE
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c]==1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board=create_board()                            #creo la tabella
print_board(board)
game_over=False                                 #variabile che indica la fine della partita
turn=0                                          #variabile che tiene conta di chi è il turno

pygame.init()                                   #pygame va sempre inizializzato

SQUARESIZE=100                                  #dimensione di un quadrato a 100pixel
width=COLUMN_COUNT*SQUARESIZE                   #la larghezza è il numero di colonne per la dimensione
height=(ROW_COUNT+1)*SQUARESIZE                 #l'altezza è il numero di righe per la dimensione, con una riga in più per l'inserimento

size=(width, height)                            #dimensione della finestra

RADIUS=int(SQUARESIZE/2-5)                        #dimensione dei cerchi

screen=pygame.display.set_mode(size)            #imposto la finestra con le dimensioni stabilite
draw_board(board)
pygame.display.update()                         #aggiorno la finestra

myfont=pygame.font.SysFont("monospace", 47)

while not game_over:
    for event in pygame.event.get():            #pygame funziona con gli eventi
        if event.type==pygame.QUIT:             #va sempre fatto per gestire l'uscita dal gioco alla chiusura
            sys.exit()                          #chiudo la finestra

        if event.type==pygame.MOUSEMOTION:      #evento quando il mouse si muove, si aggiorna sempre 
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx=event.pos[0]
            if turn==0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:  #la selezione è decisa in base a dove clicchiamo adesso
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            #turno giocatore 1
            if turn==0:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board,col):        #se la scelta è valida inserisco nella riga libera
                    row=get_next_open_row(board,col)
                    drop_piece(board,row,col,1)

                    if winning_move(board, 1):
                        label=myfont.render("GIOCATORE 1 HA VINTO!!", 1, RED)
                        screen.blit(label, (40,10))              #non aggiorna tutta la finestra ma solo una parte
                        game_over=True

            #turno giocatore 2
            else:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,row,col,2)

                    if winning_move(board, 2):
                        label=myfont.render("GIOCATORE 2 HA VINTO!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over=True
            
            print_board(board)
            draw_board(board)

            turn+=1                                     #passo il turno
            turn=turn%2                                 #divido per 2 così da avere un turno circolare

            if game_over:
                pygame.time.wait(3000)                  #aspetta 3000ms prima di chiudere