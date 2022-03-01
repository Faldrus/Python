import turtle
import winsound
import random

def random_number(start, stop):
    return random.uniform(start,stop)

wn=turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")                                     #colore finestra
wn.setup(width=800, height=600)                         #dimensione scheda
wn.tracer(0)                                            #blocca la finestra dall'aggiornarsi, così aggiorniamo noi 

#punteggi
score_a=0
score_b=0

#Racchetta A
paddle_a=turtle.Turtle()                                #oggetto di Turtle(classe) del modello turtle
paddle_a.speed(0)                                       #velocità dell'animazione
paddle_a.shape("square")                                #forma della racchetta
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)        #cambia la forma 
paddle_a.penup()                                        #i turtler creano una scia, con questo metodo non faccio la scia
paddle_a.goto(-350, 0)                                  #coordinata di partenza

#Racchetta B
paddle_b=turtle.Turtle()                                #oggetto di Turtle(classe) del modello turtle
paddle_b.speed(0)                                       #velocità dell'animazione
paddle_b.shape("square")                                #forma della racchetta
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)        #cambia la forma 
paddle_b.penup()                                        #i turtler creano una scia, con questo metodo non faccio la scia
paddle_b.goto(350, 0)                                   #coordinata di partenza

#Palla
ball=turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0,0)
ball.dx=random_number(-1,1)                             #velocità x (dx è la derivata x)
ball.dy=random_number(-1,1)                             #velocità y (dy è la derivata y)  così la palla si muove verso l'altro e verso destra di 2

#Pen(è solo un turtle)
pen=turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

#Movimenti racchetta
def paddle_a_up():
    y=paddle_a.ycor()                                   #mette la coordinata y della racchetta in y
    if y+10<300:                                      
        y+=20                                           #aggiungo 20 pixel a y
        paddle_a.sety(y)

def paddle_a_down():
    y=paddle_a.ycor()                                   #mette la coordinata y della racchetta in y
    if y-10>-280:
        y-=20                                           #tolgo 20 pixel a y
        paddle_a.sety(y)

def paddle_b_up():
    y=paddle_b.ycor()                                   #mette la coordinata y della racchetta in y
    if y-10<280:
        y+=20                                           #aggiungo 20 pixel a y
        paddle_b.sety(y)

def paddle_b_down():
    y=paddle_b.ycor()                                   #mette la coordinata y della racchetta in y
    if y-10>-280:
        y-=20                                           #tolgo 20 pixel a y
        paddle_b.sety(y)

#Key bindings
wn.listen()                                             #wn windows, ascolta gli input
wn.onkeypress(paddle_a_up, "w")                         #alla pressione di w, invoca il metodo paddle_a_up               
wn.onkeypress(paddle_a_down, "s")                       #alla pressione di s, invoca il metodo paddle_a_down 
wn.onkeypress(paddle_b_up, "Up")                        #alla pressione di up, invoca il metodo paddle_b_up               
wn.onkeypress(paddle_b_down, "Down")                    #alla pressione di down, invoca il metodo paddle_b_down 

#Main loop
while True:
    wn.update()                                         #aggiorno al finestra in loop

    #Movimento palla
    ball.setx(ball.xcor()+ball.dx)                      #ad ogni loop la coordinata x si aggiorna e aumenta di dx
    ball.sety(ball.ycor()+ball.dy)                      #ad ogni loop la coordinata y si aggiorna e aumenta di dy

    #Controllo bordi
    if ball.ycor()>290:
        ball.sety(290)                                  #se raggiungo il bordo superiore, cambio la direzione verso il basso
        ball.dy*=-1
        winsound.PlaySound("bruh.wav", winsound.SND_ASYNC)                     
    
    if ball.ycor()<-290:
        ball.sety(-290)                                 #se raggiungo il bordo inferiore, cambio la direzione verso l'alto
        ball.dy*=-1     
        winsound.PlaySound("bruh.wav", winsound.SND_ASYNC)                                
    
    if ball.xcor()>390:
        ball.goto(0,0)                                  #se tocco il bordo, riporto la palla al centro e la faccio andare dall'altra parte
        ball.dx*=-1
        ball.dy=random_number(-1,1)
        score_a+=1                                      #se tocco il bordo a destra, giocatore A riceve un punto
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        winsound.PlaySound("bruh.wav", winsound.SND_ASYNC)

    if ball.xcor()<-390:
        ball.goto(0,0)                                  #se tocco il bordo, riporto la palla al centro e la faccio andare dall'altra parte
        ball.dx*=-1
        ball.dy=random_number(-1,1)
        score_b+=1                                      #se tocco il bordo a sinistra, giocatore B riceve un punto
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        winsound.PlaySound("bruh.wav", winsound.SND_ASYNC)
        
    #collisione racchetta A e palla
    if ball.xcor()<-340 and ball.xcor()>-350 and ball.ycor()<paddle_a.ycor()+50 and ball.ycor()>paddle_a.ycor()-50:
        ball.setx(-340)
        ball.dx*=-1
        winsound.PlaySound("earrape moan.wav", winsound.SND_ASYNC)  #quando la racchetta colpisce la palla, faccio partire il suono

    #collisione racchetta B e palla
    if ball.xcor()>340 and ball.xcor()<350 and ball.ycor()<paddle_b.ycor()+50 and ball.ycor()>paddle_b.ycor()-50:
        ball.setx(340)
        ball.dx*=-1
        winsound.PlaySound("earrape moan.wav", winsound.SND_ASYNC)  #quando la racchetta colpisce la palla, faccio partire il suono

    