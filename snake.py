from turtle import Turtle, Screen
import random
import time

segments = []
end = False
count = 0
WIDTH = 500
CURSOR_SIZE = 20
MINIMUM = CURSOR_SIZE / 2 - WIDTH / 2
MAXIMUM = WIDTH / 2 - CURSOR_SIZE / 2

# Set up border
def setup(turtle):
    turtle.penup()
    turtle.speed(0)
    turtle.goto(-WIDTH / 2, WIDTH / 2)
    turtle.pendown()
    turtle.color('grey')
    for _ in range(4):
        turtle.forward(WIDTH)
        turtle.right(90)

border_pen = Turtle(visible=False)
setup(border_pen)

# Snake head
head = Turtle()
head.speed(0)
head.shape("square")
head.color("red")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Original tail
for i in range(5):
    new_segment = Turtle()
    new_segment.hideturtle()
    new_segment.penup()
    new_segment.shape("square")
    new_segment.color("blue", "black")
    new_segment.speed(0)
    segments.append(new_segment)         

# Monster
monster = Turtle()
monster.hideturtle()
monster.penup()
monster.shape("square")
monster.color("purple")
monster.goto(random.randint(MINIMUM,MAXIMUM),random.randint(MINIMUM,MAXIMUM))
while monster.distance(head)<=150:  # Make the monster far enough
    monster.goto(random.randint(MINIMUM,MAXIMUM),random.randint(MINIMUM,MAXIMUM))
monster.showturtle()

# Pause or un-pause
def pause():
    global game_status
    if game_status == 'play':
        game_status = 'pause'
    elif game_status == 'pause':
        game_status = 'play'

# Food coordinates
numbers = []
for i in range(9):
    x = random.randint(MINIMUM,MAXIMUM)
    y = random.randint(MINIMUM,MAXIMUM)
    numbers.append([x, y])
food = [None] * 10
check = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Snake food
for i in range(1,10):  # Food range 1 ~ 9
    food[i] = Turtle()
    food[i].speed(0)
    food[i].penup()
    food[i].goto(numbers[i-1][0], numbers[i-1][1])
    food[i].hideturtle()

# Pen
pen = Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0,100)
pen.write("Welcome to Kinley's version of snake...\n\nYou are going to use the 4 arrow keys to move the snake\naround the screen,trying to consume all the food items\nbefore the monster catches you...\n\nClick anywhere on the screen to start the game, have fun!!", align="center", font=("Courier", 10, "normal"))

# Game startup
start, game_status = False, 'pause'
def startup(x,y):
    global game_status, start
    if game_status=='pause' and start==False:
        game_status='play'       
    if game_status=='play' and start==False:
        pen.clear()
        start = True       
        for i in range(1,10):  # Show the food   
            food[i].write(i, align="center", font=("Courier", 10, "normal"))
       
    pen.color("red")
    pen.penup()

screen = Screen()
screen.title("Snake")
screen.onscreenclick(startup)  
time_start = time.time()

def monster_move():
    global start
    if start == True:
        global end, count, segments
        x1, y1 = head.xcor(), head.ycor()
        x2, y2 = monster.xcor(), monster.ycor()
        if x1 >= x2 and y1 >= y2:
            if (x1 - x2) > (y1 - y2): monster.setx(x2 + 20)
            else: monster.sety(y2 + 20)
        elif x1 <= x2 and y1 >= y2:
            if (x2 - x1) > (y1 - y2): monster.setx(x2 - 0)
            else: monster.sety(y2 + 20)
        elif x1 <= x2 and y1 <= y2:
            if (x2 - x1) > (y2 - y1): monster.setx(x2 - 20)
            else: monster.sety(y2 - 20)
        elif x1 >= x2 and y1 <= y2:
            if (x1 - x2) > (y2 - y1): monster.setx(x2 + 20)
            else: monster.sety(y2 - 20)
               
        # Check body collision
        for segment in segments:
            if segment.distance(monster) < 20:
                count+=1

        # Check game termination
        if monster.distance(head) < 18:
            end=True 
            pen.goto(head.xcor(), head.ycor())       
            pen.write("Game Over!!!!!",font=("Courier", 15, "normal"))

        global time_start
        time_end = time.time()
        screen.title("Snake: Contacted:{x}, Time:{y}".format(x=count, y=int(time_end-time_start)))
        screen.update()
        if end == True: 
            return 
    screen.ontimer(monster_move, random.randrange(350, 700, 50))

# Keybind functions
def down():
    if head.ycor() <= MINIMUM:
        head.direction = "stop"
    else:
        head.direction = "down"

def up():
    if head.ycor() >= MAXIMUM:
        head.direction = "stop"
    else:
        head.direction = "up"

def left():
    if head.xcor() <= MINIMUM:
        head.direction = "stop"
    else:
        head.direction = "left"

def right():
    if head.xcor() >= MAXIMUM:
        head.direction = "stop"
    else:
        head.direction = "right"

def head_move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

t = 0   # Times that the snake move slower beacause of its tail expansion
def snake_move():
    global end, game_status
    if end == True:
        return 
    if (head.ycor() <= MINIMUM and head.direction == 'down') or (head.ycor() >= MAXIMUM and head.direction == 'up') or (head.xcor() <= MINIMUM and head.direction == 'left') or (head.xcor() >= MAXIMUM and head.direction == 'right'):
        head.direction = 'stop'

    global t
    if MINIMUM <= head.ycor() <= MAXIMUM and MINIMUM <= head.xcor() <= MAXIMUM and head.direction!="stop" and game_status=='play':
                         
        # Check for a collision with the food
        for i in range(1, 10):
            if head.distance(food[i]) <= 15: 
                t += i
                food[i].clear()
                check[i] = 0            
                for _ in range(i):
                    new_segment = Turtle()
                    new_segment.hideturtle()
                    new_segment.penup()
                    new_segment.speed(0)
                    new_segment.shape("square")
                    new_segment.color("blue", "black")
                    new_segment.goto(segments[-1].xcor(), segments[-1].ycor())
                    segments.append(new_segment)  
 
        # Move the end segments first in reverse order
        for i in range(len(segments) - 1, 0, -1):
            segments[i].showturtle()
            segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())

        # Move segment 0 to the head        
        segments[0].showturtle()
        segments[0].goto(head.xcor(), head.ycor())

        head_move()
        screen.update()
        
        # Check for victory
        if check.count(0)==10:  
            pen.goto(head.xcor(), head.ycor())
            pen.write("Winner!!!!!", font=("Courier", 15, "normal"))
            end = True

    if t > 0: 
        screen.ontimer(snake_move, 500)
        t -= 1
    else: screen.ontimer(snake_move, 400)  
    if end==True: return 
    
screen.onkey(up, 'Up')
screen.onkey(down, 'Down')
screen.onkey(left, 'Left')
screen.onkey(right, 'Right')
screen.onkey(pause, 'space')
screen.tracer(0)
 
monster_move()
snake_move()

screen.listen()
screen.mainloop()
