import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

def drawGrid(w, rows, surface):
    sizeBtwn=w//rows                                                #dimensione tra una riga e un'altra
    x=0
    y=0

    for l in range(rows):
        x+=sizeBtwn
        y+=sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x,0), (x,w))    #disegna una linea bianca da (x,0) a (x,w) ed è orizzontale su surface
        pygame.draw.line(surface, (255, 255, 255), (0,y), (w,y))    #disegna una linea bianca da (0,y) a (w,y) ed è verticale su surface

def redrawWindows(surface):
    global rows, width
    surface.fill((0,0,0))                                               #coloro la finestra di nero
    drawGrid(width, rows, surface)
    pygame.display.update()                                         #aggiorna la finestra


#main loop
def main():
    global width,rows
    width=500                                                       #dimensione finestra
    heigth=500
    rows=20                                                         #righe e colonne
    win=pygame.display.set_mode((width, heigth))
    s=snake((255,0,0), (10,10))                                     #serpente colore HEX e posizione iniziale in righe
    
    clock=pygame.time.Clock()
    flag=True
    while flag:
        pygame.time.delay(50)                                       #delay per non aggiornare troppo, delay e tick sono inversamente proporzionali
        clock.tick(10)                                              #limita i tick del gioco così il serpente non si muove troppo velocemente

        redrawWindow(win)
