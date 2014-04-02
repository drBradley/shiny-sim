from cartesian import Vector

class String(object):

    def __init__(self, right, left, k):

        self.right = right
        self.left = left
        self.k = k

        self.length = Vector.get_direction(self.right, self.left)

    def update_extension(self):

        self.extension = Vector.get_direction(self.right, self.left) - self.length

    def update_force(self):

        self.force = self.k * self.extension

    def apply_force(self):

        self.right.apply(self.force)
        self.left.apply(self.force)
