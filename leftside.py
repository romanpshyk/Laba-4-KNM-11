# Ping-Pong game with turtle module.
# Done by Sri Manikanta Palakollu.
# Version - 3.7.0

import turtle as t
import json
import socket

# Score varibales
ball_xy = [1000, 1000]
rpos = "r"

win = t.Screen()    # creating a window
win.title("Ping-Pong Game") # Giving name to the game.
win.bgcolor('black')    # providing color to the HomeScreen
win.setup(width=1920, height=1080) # Size of the game panel
win.tracer(0)   # which speed up's the game.

# Creating left paddle for the game

paddle_left = t.Turtle()
paddle_left.speed(0)
paddle_left.shape('square')
paddle_left.color('red')
paddle_left.shapesize(stretch_wid=5, stretch_len=1)
paddle_left.penup()
paddle_left.goto(-900, 0)

# Creating a right paddle for the game
# Creating a pong ball for the game

ball = t.Turtle()
ball.speed(0)
ball.shape('circle')
ball.color('yellow')
ball.penup()
ball.goto(0, 0)
ball_dx = 0  # Setting up the pixels for the ball movement.
ball_dy = 0

# Moving the left Paddle using the keyboard


def paddle_left_up():
    y = paddle_left.ycor()
    y = y + 15
    paddle_left.sety(y)

# Moving the left paddle down


def paddle_left_down():
    y = paddle_left.ycor()
    y = y - 15
    paddle_left.sety(y)


# Keyboard binding

win.listen()
win.onkeypress(paddle_left_up,"w")
win.onkeypress(paddle_left_down,"s")

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

    if(ball.xcor()) < -960: # Left width paddle Border
        ball.setx(-960)
        ball_dx = ball_dx * -1
    # Handling the collisions with paddles.

    if(ball.xcor() < -890) and (ball.xcor() > -900) and (ball.ycor() < paddle_left.ycor() + 40 and ball.ycor() > paddle_left.ycor() - 40):
        ball.setx(-890)
        ball_dx = ball_dx * -1

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.63", 10082))
    ball_xy = [ball.xcor(), ball.ycor(), ball_dx, ball_dy]
    ready_data = json.dumps(ball_xy)
    s.send(ready_data.encode())
    ball_xy = [0, 0]
    ready_data = ''

    pos = s.recv(1000)
    if rpos != pos.decode():
        rpos = pos.decode()
        if rpos == 'r':
            ball.setx(1000)
            ball.sety(1000)
            ball_dx = 0
            ball_dy = 0
        elif rpos == 'l':
            cords = s.recv(1024)
            rcords = json.loads(cords.decode())
            ball.setx = -rcords[0]
            ball.sety = rcords[1]
            ball_dx = rcords[2]
            ball_dy = rcords[3]
