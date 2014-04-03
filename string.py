from abc import ABCMeta, abstractmethod

from vector import Vector


class Interaction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute(self):

        pass

class String(Interaction):

    name = "String"

    def __init__(self, right, left, k):

        self.right = right
        self.left = left
        self.k = k

        self.length = Vector.get_direction(self.right.position, self.left.position)

    def compute(self):

        self.update_extension()
        self.update_force()
        self.apply_force()

    def update_extension(self):

        self.extension = Vector.get_direction(self.right.position, self.left.position) - self.length

    def update_force(self):

        self.force = self.k * self.extension

    def apply_force(self):

        self.right.apply(-self.force)
        self.left.apply(self.force)

    def show(self):

        return String.name + " force [" + self.right.show() + " -> " + self.left.show() + "] " + str(self.k)

    def draw(self, painter):

        painter.drawLine(self.left.position.x, self.left.position.y,
                         self.right.position.x, self.right.position.y)
