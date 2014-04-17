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

        self.length = abs(Vector.get_direction(self.right.position, self.left.position))

    def compute(self):

        self.update()
        self.apply()

    def update(self):

        self.extension = Vector.get_direction(self.right.position, self.left.position)
        extension_length = abs(self.extension)
        self.extension = self.extension / abs(self.extension)
        self.extension = self.extension * (extension_length - self.length)

        self.force = self.k * self.extension
        self.potential_energy = self.k * abs(self.extension) * abs(self.extension) / 2

    def apply(self):

        self.right.force += -self.force
        self.left.force += self.force

        self.right.potential_energy += self.potential_energy
        self.left.potential_energy += self.potential_energy

    def show(self):

        return String.name + " force [" + self.right.show() + " -> " + self.left.show() + "] " + str(self.k)
