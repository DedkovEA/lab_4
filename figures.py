from random import random, choice, randrange

max_vel = 7
colors = ['red', 'orange', 'yellow', 'green', 'blue']
t_min = 3000
t_max = 10000
cursor_interaction_constant = 70000000


def generate_figure(obj, canvas):
    if isinstance(obj, Ball):
        return Ball(canvas)
    elif isinstance(obj, TrickyBall):
        return TrickyBall(canvas)
    else:
        return None


class Figure:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = randrange(100, canvas.winfo_width() - 100)
        self.y = randrange(100, canvas.winfo_height() - 100)
        self.r = randrange(30, 50)
        self.vx = max_vel - 2 * max_vel * random()
        self.vy = max_vel - 2 * max_vel * random()
        self.color = choice(colors)
        self.lifespan = randrange(t_min, t_max)
        self.lifetime = 0
        self.mass = 1
        self.score = 0

    def move(self, dx, dy):
        """Moves object on dx, dy"""
        self.x += dx
        self.y += dy
        return True

    def recalculate_position(self, *args):
        """Recalculates position of figure after dt time interval"""
        if self.move(self.vx, self.vy):
            return True
        else:
            return False

    def reflect_from_boundaries(self, *args):
        """
        Recalculates velocity on border [0th arg, 1st arg] [2nd arg, 3nd arg]
        """
        change = False
        if self.x <= args[0]:
            self.vx = abs(self.vx)
            self.vy = (2 * random() - 1) * max_vel
            change = True
        elif self.x >= args[1]:
            self.vx = -abs(self.vx)
            self.vy = (2 * random() - 1) * max_vel
            change = True
        if self.y <= args[2]:
            self.vy = abs(self.vy)
            self.vx = (2 * random() - 1) * max_vel
            change = True
        elif self.y >= args[3]:
            self.vy = -abs(self.vy)
            self.vx = (2 * random() - 1) * max_vel
            change = True
        return change

    def interact(self, other):
        if (self.x - other.x) ** 2 + (self.y - other.y) ** 2 <= \
                (self.r + other.r) ** 2 and (
                (self.vx - other.vx) * (other.x - self.x) + (
                self.vy - other.vy) * (other.y - self.y)) > 0:

            # Recalculating velocities via interaction
            vx_c = (self.vx * self.mass + other.vx * other.mass) / \
                   (self.mass + other.mass)
            vy_c = (self.vy * self.mass + other.vy * other.mass) / \
                   (self.mass + other.mass)
            vx_s1 = self.vx - vx_c
            vy_s1 = self.vy - vy_c
            vx_o1 = other.vx - vx_c
            vy_o1 = other.vy - vy_c
            tg = (self.y - other.y) / (self.x - other.x)
            vx_s2 = vx_s1 - 2 * (vy_s1 * tg + vx_s1) / (1 + tg ** 2)
            vy_s2 = -vy_s1 + 2 * (vy_s1 - vx_s1 * tg) / (1 + tg ** 2)
            vx_o2 = vx_o1 - 2 * (vy_o1 * tg + vx_o1) / (1 + tg ** 2)
            vy_o2 = -vy_o1 + 2 * (vy_o1 - vx_o1 * tg) / (1 + tg ** 2)
            self.vx = vx_s2 + vx_c
            self.vy = vy_s2 + vy_c
            other.vx = vx_o2 + vx_c
            other.vy = vy_o2 + vy_c

            # pushing sticked figures
            #    if (self.x - other.x) ** 2 + (self.y - other.y) ** 2 < \
            #            (self.r + other.r - 3) ** 2:
            #        dr_w = (self.r + other.r - ((self.x - other.x) ** 2 +
            #                                 (self.y - other.y) ** 2)**0.5) / \
            #             (self.mass + other.mass)
            #        self.x, other.x =

            return True
        else:
            return False

    def includes_point(self, *argv):
        """Returns if point in figure"""
        return True

    def lifetime_add(self, t):
        """
        Add lifetime and if it > lifespan then
        return true and delete ball
        """
        self.lifetime += t
        if self.lifetime > self.lifespan:
            self.delete()
            return True
        else:
            return False

    def delete(self):
        """Delete figure"""
        return True


class Ball(Figure):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                     self.x + self.r, self.y + self.r,
                                     fill=self.color, width=0)
        self.mass = 3.1415 * self.r ** 2
        self.score = 1

    def move(self, dx, dy, *args):
        """Moves ball on dx, dy"""
        super().move(dx, dy, *args)
        self.canvas.move(self.id, dx, dy)
        return True

    def reflect_from_boundaries(self, *args):
        """
        Makes ball reflect from borders [args[0], args[1]] [args[2], args[3]]
        """
        return super().reflect_from_boundaries(args[0] + self.r,
                                               args[1] - self.r,
                                               args[2] + self.r,
                                               args[3] - self.r)

    def includes_point(self, *argv):
        """Returns True if point is in circle"""
        return (self.x - argv[0]) ** 2 + (self.y - argv[1]) ** 2 <= self.r ** 2

    def delete(self):
        """Delete ball"""
        if super().delete():
            self.canvas.delete(self.id)
            return True
        else:
            return False


class TrickyBall(Figure):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.id_out = canvas.create_oval(self.x - self.r, self.y - self.r,
                                         self.x + self.r, self.y + self.r,
                                         fill=self.color, width=0)
        self.id_in = canvas.create_oval(self.x - self.r / 2,
                                        self.y - self.r / 2,
                                        self.x + self.r / 2,
                                        self.y + self.r / 2,
                                        fill='black', width=0)
        self.mass = 3.1415 * self.r ** 2
        self.score = int(30000 / self.mass)

    def move(self, dx, dy):
        super().move(dx, dy)
        self.canvas.move(self.id_out, dx, dy)
        self.canvas.move(self.id_in, dx, dy)
        return True

    def includes_point(self, *argv):
        return (self.x - argv[0]) ** 2 + (self.y - argv[1]) ** 2 <= self.r ** 2

    def delete(self):
        if super().delete():
            self.canvas.delete(self.id_in)
            self.canvas.delete(self.id_out)
            return True
        else:
            return False

    def reflect_from_boundaries(self, *args):
        """
        Makes ball reflect from borders [args[0], args[1]] [args[2], args[3]]
        """
        return super().reflect_from_boundaries(args[0] + self.r,
                                               args[1] - self.r,
                                               args[2] + self.r,
                                               args[3] - self.r)

    def recalculate_position(self, *args):
        super().recalculate_position(*args)
        distance = ((self.x - args[0])**2 + (self.y - args[1])**2) ** 0.5
        self.vx += cursor_interaction_constant * (self.x - args[0]) / \
                   distance ** 3 / self.mass
        self.vy += cursor_interaction_constant * (self.y - args[1]) / \
                   distance ** 3 / self.mass
