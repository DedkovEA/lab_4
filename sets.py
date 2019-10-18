import figures


class FigureSet:
    def __init__(self, canvas, *args):
        self.figure_list = list(args)
        self.canvas = canvas
        self.cursor_x = 0
        self.cursor_y = 0
        canvas.bind('<Motion>', self.motion)

    def add_object(self, figure):
        self.figure_list.append(figure)

    def delete_object(self, figure):
        self.figure_list.remove(figure)
        return figure.delete()

    def evolute(self, t, *args):
        for current_figure in self.figure_list:
            current_figure.recalculate_position(self.cursor_x, self.cursor_y)
            if current_figure.lifetime_add(t):
                self.delete_object(current_figure)
                self.add_object(
                    figures.generate_figure(current_figure,
                                            self.canvas))
        for current_figure in self.figure_list:
            current_figure.reflect_from_boundaries(*args)
            for other_figure in range(self.figure_list.index(current_figure)+1,
                                      len(self.figure_list)):
                current_figure.interact(self.figure_list[other_figure])
        return True

    def shoot(self, *args):
        counter = 0
        for current_figure in self.figure_list:
            if current_figure.includes_point(*args):
                counter += current_figure.score
                self.delete_object(current_figure)
                self.add_object(
                        figures.generate_figure(current_figure,
                                                self.canvas))
        return counter

   # def fix_position(self, figure):
   #     for other_figure in self.figure_list:
   #         while (figure.x - other_figure.x)**2 + \
   #               (figure.y - other_figure.y)**2 <= \
   #               (figure.r + other_figure.r + 5)**2:
   #             figure.delete()
   #             figure = figures.generate_figure(figure, self.canvas)
   #     return figure

    def motion(self, event):
        self.cursor_x, self.cursor_y = event.x, event.y
        return True
