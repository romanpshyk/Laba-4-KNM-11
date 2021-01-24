# Ping-Pong game with turtle module.
# Done by Sri Manikanta Palakollu.
# Version - 3.7.0

import turtle as t
import json
import socket

ball_xy = [0, 0]
rpos = 'l'

win = t.Screen()    # creating a window
win.title("Ping-Pong Game") # Giving name to the game.
win.bgcolor('black')    # providing color to the HomeScreen
win.setup(width=1920, height=1080) # Size of the game panel
win.tracer(0)   # which speed up's the game.

# Creating a right paddle for the game

paddle_right = t.Turtle()
paddle_right.speed(0)
paddle_right.shape('square')
paddle_right.shapesize(stretch_wid=5,stretch_len=1)
paddle_right.color('red')
paddle_right.penup()
paddle_right.goto(900, 0)

# Creating a pong ball for the game

ball = t.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('yellow')
ball.penup()
ball.goto(1000, 1000)
ball_dx = 0  # Setting up the pixels for the ball movement.
ball_dy = 0



def paddle_right_up():
    y = paddle_right.ycor()
    y = y + 15
    paddle_right.sety(y)

# Moving right paddle down

def paddle_right_down():
    y = paddle_right.ycor()
    y = y - 15
    paddle_right.sety(y)


win.onkeypress(paddle_right_up,"Up")
win.onkeypress(paddle_right_down,"Down")




# Main Game Loop

while True:
    win.update() # This methods is mandatory to run any game

    # Moving the ball
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    # setting up the border

    if ball.ycor() > 540:   # Right top paddle Border
        ball.sety(540)
        ball_dy = ball_dy * -1


    if ball.ycor() < -540:  # Left top paddle Border
        ball.sety(-540)
        ball_dy = ball_dy * -1

    if ball.xcor() < -960:
        ball.setx(-960)
        ball_dx = ball_dx * -1


    # Handling the collisions with paddles.

    if(ball.xcor() > 890) and (ball.xcor() < 900) and (ball.ycor() < paddle_right.ycor() + 40 and ball.ycor() > paddle_right.ycor() - 40):
        ball.setx(890)
        ball_dx = ball_dx * -1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.63", 10082))
    ball_xy = [ball.xcor(), ball.ycor()]
    ready_data = json.dumps(ball_xy)
    s.send(ready_data.encode())
    pos = s.recv(10)
    ball_xy = [0, 0]
    ready_data = ''

    if rpos != pos.decode():
        rpos = pos.decode()
        if rpos == 'l':
            ball.setx(1000)
            ball.sety(1000)
            ball_dx = 0
            ball_dy = 0
            s.close()
        elif rpos == 'r':
            cords = s.recv(1024)
            rcords = cords.decode()
            rcords = json.loads(cords.decode())
            ball.setx = -rcords[0]
            ball.sety = rcords[1]
            ball_dx = rcords[2]
            ball_dy = rcords[3]
            s.close()
