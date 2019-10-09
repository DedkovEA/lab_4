import tkinter


class Ball:
    def __init__(self, canvas, x, y, r, color, lifespan):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.canvas = canvas
        self.lifespan = lifespan
        self.lifetime = 0
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r,
                                     fill=color, width=0)

    def move(self, dx, dy):
        """Moves ball on dx, dy"""
        self.canvas.move(self.id, dx, dy)
        self.x += dx
        self.y += dy
        return True

    def includes_point(self, *argv):
        """Returns True if point is in circle"""
        return (self.x - argv[0])**2 + (self.y - argv[1])**2 <= self.r**2

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
        """Delete ball"""
        self.canvas.delete(self.id)
        return True
