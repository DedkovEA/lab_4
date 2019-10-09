import tkinter
from random import randrange as rnd, choice
import ball

# Initializing root window and setting its size
root = tkinter.Tk()
root.geometry('800x650')

# Initializing canvas and score label
canvas_frame = tkinter.Frame(root, width=800, height=600)
score_label = tkinter.Label(root, text='Score: 0')
canvas = tkinter.Canvas(canvas_frame, bg='white')

# packing objects
canvas.pack(fill=tkinter.BOTH, expand=1)
canvas_frame.pack(fill=tkinter.BOTH, expand=1)
score_label.pack(anchor=tkinter.W)

# initializing colors
colors = ['red', 'orange', 'yellow', 'green', 'blue']

# score init
score = 0

# initialization of ball list
ball_list = list()


def tick():
    """
    Executed every 50ms
    """
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    t = rnd(400, 1000)
    for current_ball in ball_list:
        if current_ball.lifetime_add(50):
            ball_list.remove(current_ball)
    if len(ball_list) < 2:
        ball_list.append(ball.Ball(canvas, x, y, r, choice(colors), t))
    root.after(50, tick)


def click(event):
    """
    Increment score, if event coordinates are in consisting ball
    :param event: event with x and y properties
    :return: True if score got
    """
    global score
    for current_ball in ball_list:
        if current_ball.includes_point(event.x, event.y):
            score += 1
            current_ball.delete()
            ball_list.remove(current_ball)
            score_label['text'] = 'Score: ' + str(score)
            return True
        else:
            return False


tick()
canvas.bind('<Button-1>', click)
tkinter.mainloop()