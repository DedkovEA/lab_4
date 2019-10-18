import tkinter
from random import randrange as rnd, choice, random
import figures
import sets

# Initializing root window and setting its size
root = tkinter.Tk()

# Initializing canvas and score label
score_label = tkinter.Label(root, text='Score: 0')
canvas = tkinter.Canvas(root, bg='white', width=800, height=600)

# packing objects
canvas.pack(fill=tkinter.BOTH, expand=1)
score_label.pack(anchor=tkinter.W, fill=tkinter.Y, expand=0)

canvas.update()
width = canvas.winfo_width()
height = canvas.winfo_height()

# initializing colors
# colors = ['red', 'orange', 'yellow', 'green', 'blue']

# score init
score = 0

ball_number = 5
tricky_ball_number = 2
# initialization of ball list
# ball_list = list()

def tick2():
    ball_set.evolute(50, 0, canvas.winfo_width(), 0, canvas.winfo_height())
    root.after(20, tick2)

def click2(event):
    global score
    score += ball_set.shoot(event.x, event.y)
    score_label['text'] = 'Score: ' + str(score)
    return True

def tick():
    """
    Executed every 50ms
    """
    global ball_list
    for current_ball in ball_list:
        if current_ball.lifetime_add(50):
            ball_list.remove(current_ball)
        current_ball.recalculate_position()
        current_ball.reflect_from_boundaries(0, canvas.winfo_width(), 0, height)
    if len(ball_list) < 2:
        x = rnd(100, canvas.winfo_width() - 100)
        y = rnd(100, height - 100)
        r = rnd(30, 50)
        t = rnd(1900, 112000)
        vx = 15 - 30 * random()
        vy = 15 - 30 * random()
        ball_list.append(figures.Ball(canvas, x, y, r,
                                      choice(colors), t, vx, vy))
    root.after(50, tick)


def click(event):
    """
    Increment score, if event coordinates are in consisting ball
    :param event: event with x and y properties
    :return: True if score got
    """
    global score
    success = False
    for current_ball in ball_list:
        if current_ball.includes_point(event.x, event.y):
            score += 1
            current_ball.delete()
            ball_list.remove(current_ball)
            score_label['text'] = 'Score: ' + str(score)
            success = True
    return success

ball_set = sets.FigureSet(canvas)

for i in range(ball_number):
    ball_set.add_object(figures.Ball(canvas))

for i in range(tricky_ball_number):
    ball_set.add_object(figures.TrickyBall(canvas))

tick2()
canvas.bind('<Button-1>', click2)
tkinter.mainloop()
