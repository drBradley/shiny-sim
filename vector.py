class Vector(object):

    def __init__(self, x=0, y=0, z=0):

        self.x = x
        self.y = y
        self.z = z

    def get_direction(start, end):

        return Vector(end.x - start.x,
                      end.y - start.y,
                      end.z - start.y)

    def mapX(self, a):

        return Vector(a(self.x), self.y, self.z)

    def __mul__(vec, a):

        if isinstance(a, (int, float)):

            return Vector(vec.x * a, vec.y * a, vec.z * a)

    def __rmul__(vec, a):

        if isinstance(a, (int, float)):

            return Vector(vec.x * a, vec.y * a, vec.z * a)

    def __div__(vec, a):

        if isinstance(a, (int, float)):

            return Vector(vec.x / a, vec.y / a, vec.z / a)

    def __rdiv__(vec, a):

        if isinstance(a, (int, float)):

            return Vector(vec.x / a, vec.y / a, vec.z / a)

    def __add__(vec_a, vec_b):

        if isinstance(vec_a, Vector):

            return Vector(vec_a.x + vec_b.x,
                          vec_a.y + vec_b.y,
                          vec_a.z + vec_b.z)

        else:

            print "Dunno what to do"

    def __sub__(vec_a, vec_b):

        if isinstance(vec_a, Vector):

            return Vector(vec_a.x - vec_b.x,
                          vec_a.y - vec_b.y,
                          vec_a.z - vec_b.z)

        else:

            print "Dunno what to do"

    def __neg__(vec):

        return -1 * vec

    def show(self):

        s =  "[" +  str(self.x) +  ", " + str(self.y) + ", " + str(self.z) + "]"

        return s
