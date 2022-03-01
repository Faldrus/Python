
import numpy as np

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
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+2]==piece:
                return True

    #controllo le diagonali "negative"
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):           #inizia dalla riga 3 al massimo       
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+2]==piece:
                return True

board=create_board()                            #creo la tabella
print(board)
game_over=False                                 #variabile che indica la fine della partita
turn=0                                          #variabile che tiene conta di chi è il turno

while not game_over:
    #turno giocatore 1
    if turn==0:
        col=int(input("È il turno del giocatore 1 (0-6): "))

        if is_valid_location(board,col):        #se la scelta è valida inserisco nella riga libera
            row=get_next_open_row(board,col)
            drop_piece(board,row,col,1)

            if winning_move(board, 1):
                print("Giocatore 1 ha vinto!")
                game_over=True
                break

    #turno giocatore 2
    else:
        col=int(input("È il turno del giocatore 2 (0-6): "))

        if is_valid_location(board,col):
            row=get_next_open_row(board,col)
            drop_piece(board,row,col,2)

            if winning_move(board, 2):
                print("Giocatore 2 ha vinto!")
                game_over=True
                break

    print_board(board)

    turn+=1                                     #passo il turno
    turn=turn%2                                 #divido per 2 così da avere un turno circolare

