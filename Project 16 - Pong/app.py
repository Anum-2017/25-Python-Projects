import turtle
import random
import winsound  

# Set up the screen
win = turtle.Screen()
win.title("Pong Game by Anum 🎮")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("deep pink")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("cyan")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = random.choice([-4, 4])
ball.dy = random.choice([-4, 4])

# Divider line
divider = turtle.Turtle()
divider.color("white")
divider.hideturtle()
divider.penup()
divider.goto(0, -300)
divider.setheading(90)
divider.pensize(2)
for _ in range(30):
    divider.pendown()
    divider.forward(10)
    divider.penup()
    divider.forward(10)

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0    Player B: 0", align="center", font=("Courier", 24, "normal"))

# Paddle movement functions
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:
        paddle_a.sety(y + 30)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 30)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        paddle_b.sety(y + 30)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        paddle_b.sety(y - 30)

# Keyboard bindings
win.listen()
win.onkeypress(paddle_a_up, "w")
win.onkeypress(paddle_a_down, "s")
win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

# Game loop
def game_loop():
    global score_a, score_b

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border collision (top/bottom)
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    # Right wall – Player A scores
    if ball.xcor() > 390:
        score_a += 1
        update_score()
        reset_ball()

    # Left wall – Player B scores
    if ball.xcor() < -390:
        score_b += 1
        update_score()
        reset_ball()

    # Paddle collisions
    if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1.1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1.1
        winsound.PlaySound("bounce.wav", winsound.SND_ASYNC)

    # Win condition
    if score_a == 5 or score_b == 5:
        winner = "Player A" if score_a == 5 else "Player B"
        pen.goto(0, 0)
        pen.write(f"{winner} Wins! 🏆", align="center", font=("Courier", 30, "bold"))
        return

    win.update()
    win.ontimer(game_loop, 20)

# Score and ball reset helpers
def update_score():
    pen.clear()
    pen.goto(0, 260)
    pen.write(f"Player A: {score_a}    Player B: {score_b}", align="center", font=("Courier", 24, "normal"))

def reset_ball():
    ball.goto(0, 0)
    ball.dx = random.choice([-4, 4])
    ball.dy = random.choice([-4, 4])

# Start game loop
game_loop()
win.mainloop()
