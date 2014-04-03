import sys
import math

from vector import Vector


if __name__ == '__main__':

    nx = int(sys.argv[1])
    ny = int(sys.argv[2])

    file_name = sys.argv[3]
    structure = int(sys.argv[4])
    print structure

    solid_frame = True

    init_offset = 50
    x_offset = int(500.0 / nx)
    y_offset = int(500.0 / ny)

    k = 1
    body_mass = 1
    frame_ratio = 1

    bodies = []
    relations = []
    weights = []

    for j in range(ny):

        bodies.append([])
        for i in range(nx):

            bodies[j].append(Vector(i, j, 0))
