import sys
import math

from vector import Vector


def translate(vec, matrix):

    for row in range(len(matrix)):

        for cell in range(len(matrix[row])):

            matrix[row][cell] = matrix[row][cell] + vec

def scale(vec, matrix):

    for row in range(len(matrix)):

        for cell in range(len(matrix[row])):

            matrix[row][cell] = Vector(matrix[row][cell].x * vec.x,
                                       matrix[row][cell].y * vec.y,
                                       matrix[row][cell].z * vec.z)

def to_honeycomb(f, matrix):

    for row in range(len(matrix)):

        for cell in range(len(matrix[row])):

            matrix[row][cell] = matrix[row][cell].mapX(f)

    scale(Vector(x_offset, x_offset), matrix)
    shift_odd_row_X(lambda x: x + (twice_x_offset + x_offset) * math.cos(math.pi / 3), matrix)

def shift_odd_row_X(f, matrix):

    for row in range(len(matrix)):

        for cell in range(len(matrix[row])):

            if row % 2 == 1:

                matrix[row][cell] = matrix[row][cell].mapX(f)

def grid_relation(relations, x, y, k):

    for j in range(y):

        for i in range(x):

            if 0 < i < x and 0 < j < y:

                relations.append('String %d %d %d\n' % (x * j + i, x * j + i - 1, k))
                relations.append('String %d %d %d\n' % (x * j + i, x * (j - 1) + i, k))

            if i == 0 and 0 < j:

                relations.append('String %d %d %d\n' % (x * j, x * (j - 1), k))

            if j == 0 and 0 < i:

                relations.append('String %d %d %d\n' % (i, i - 1, k))

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

    if structure == 0:
        # QUADRATIC GRID
        scale(Vector(x_offset, y_offset), bodies)
        translate(Vector(init_offset, init_offset), bodies)

        grid_relation(relations, nx, ny, k)

    with open(file_name, 'w') as output:

        for j in range(ny):

            for i in range(nx):

                output.write('Body %d %d %d\n' % (bodies[j][i].x,
                                                  bodies[j][i].y,
                                                  weights[j][i]))

        for string in relations:

            output.write(string)
