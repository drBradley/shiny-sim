class Point(object):

    def __init__(self, x=0, y=0, z=0):

        self.x = x
        self.y = y
        self.z = z

class Vector(object):

    def __init__(self, x=0, y=0, z=0):

        self.x = x
        self.y = y
        self.z = z

    def get_direction(start, end):

        return Vector(end.x - start.x,
                      end.y - start.y,
                      end.z - start.y)

    def __mul__(vec, a):

        if isinstance(a, (int, float)):

            return Vector(vec.x * a, vec.y * a, vec.z * a)

    def __rmul__(vec, a):

        if isinstance(a, (int, float)):

            return Vector(vec.x * a, vec.y * a, vec.z * a)


    def __add__(vec_a, vec_b):

        if isinstance(a, Vector):

            return Vector(vec_a.x + vec_b.x,
                          vec_a.y + vec_b.y,
                          vec_a.z + vec_b.z)

    def __sub__(vec_a, vec_b):

        if isinstance(a, Vector):

            return Vector(vec_a.x - vec_b.x,
                          vec_a.y - vec_b.y,
                          vec_a.z - vec_b.z)

    def show(self):

        print "[", self.x, ", ", self.y, ", ", self.z, "]"
