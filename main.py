import tkinter
import figures
import sets
import score_line


def main():
    # Initializing root window and setting its size
    root = tkinter.Tk()
    root.title("Ball Shooter")

    menu(root)
    root.mainloop()


def menu(root):
    def start(root):
        root.destroy()
        root = tkinter.Tk()
        root.title("Ball Shooter")

        enter_name_label = tkinter.Label(root, text='Enter your name')
        name = tkinter.StringVar()
        name_entry = tkinter.Entry(root, textvariable=name)
        submit_button = tkinter.Button(root, text='Submit',
                                       command=lambda: game_start(root, name))

        enter_name_label.pack()
        name_entry.pack()
        submit_button.pack()

    title = tkinter.Label(root, text="Ball Shoot", font=("Arial", 18),
                          anchor=tkinter.CENTER)
    button_start = tkinter.Button(root, text="Start Game",
                                  command=lambda: start(root))
    button_exit = tkinter.Button(root, text="Exit", command=lambda: exit())

    title.grid(column=1, row=1)
    button_start.grid(column=1, row=2)
    button_exit.grid(column=1, row=4)


def game_start(root, name):
    root.destroy()

    root = tkinter.Tk()
    root.title("Ball Shooter")
    # Initializing canvas and score label
    canvas = tkinter.Canvas(root, bg='white', width=800, height=600)
    labels_frame = tkinter.Frame(root)
    time_label = tkinter.Label(labels_frame, text='Time remains: 6s')
    score_label = tkinter.Label(labels_frame, text='Score: 0')

    # packing objects
    canvas.pack(fill=tkinter.BOTH, expand=1)
    labels_frame.pack(anchor=tkinter.W, fill=tkinter.BOTH, expand=1)
    time_label.grid(row=1, column=2, sticky=tkinter.E)
    score_label.grid(row=1, column=1, sticky=tkinter.W)

    canvas.update()

    # score init
    global score
    score = 0

    ball_number = 5
    tricky_ball_number = 2

    # initialization of ball list
    ball_set = sets.FigureSet(canvas)

    for i in range(ball_number):
        ball_set.add_object(figures.Ball(canvas))

    for i in range(tricky_ball_number):
        ball_set.add_object(figures.TrickyBall(canvas))

    tick(root, canvas, ball_set)
    canvas.bind('<Button-1>', lambda e: click(ball_set, score_label, e))
    root.after(1000, lambda: timer_decrease(root, time_label, name))


def timer_decrease(root, time_label, name):
    current_time = int(time_label['text'].split(' ')[2][0:-1])
    current_time -= 1
    time_label['text'] = 'Time remains: ' + str(current_time) + 's'

    if current_time <= 0:
        end_game(root, name)
    else:
        root.after(1000, lambda: timer_decrease(root, time_label, name))


def end_game(root, name):
    with open('score.txt', 'r') as file:
        scores = score_line.Scores(file)

        result = '{place:>5}|{nick:<16}|{score:>8}'.format(place='1',
                                                           nick=name.get(),
                                                           score=score)
        scores.add_line(result)
    with open('score.txt', 'w') as file:
        scores.write_to_file(file)

    root.destroy()
    main()


def tick(root, canvas, ball_set):
    ball_set.evolute(50, 0, canvas.winfo_width(), 0, canvas.winfo_height())
    root.after(20, lambda: tick(root, canvas, ball_set))


def click(ball_set, score_label, event):
    global score
    score += ball_set.shoot(event.x, event.y)
    score_label['text'] = 'Score: ' + str(score)
    return True


if __name__ == "__main__":
    score = 0
    main()

