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

                relations.append('String %d %d %f\n' % (x * j + i, x * j + i - 1, k))
                relations.append('String %d %d %f\n' % (x * j + i, x * (j - 1) + i, k))

            if i == 0 and 0 < j:

                relations.append('String %d %d %f\n' % (x * j, x * (j - 1), k))

            if j == 0 and 0 < i:

                relations.append('String %d %d %f\n' % (i, i - 1, k))

def honeycomb_relations(relations, nx, ny, k):

    for j in range(ny):

        for i in range(nx):

            if i < nx - 1 and i % 2 == 0:

                relations.append('String %d %d %f\n' % (j * nx + i, j * nx + i + 1, k))

            if j < ny - 1 and 0 < i and j % 2 == 0:

                relations.append('String %d %d %f\n' % (j * nx + i, (j + 1) * nx + i - 1, k))

            if j < ny - 1 and i < nx - 1 and j % 2 == 1:

                relations.append('String %d %d %f\n' % (j * nx + i, (j + 1) * nx + i + 1, k))

def honeycomb_extended_relations(relations, nx, ny, k):

    for j in range(ny):

        for i in range(nx):

            if i < nx - 1:

                if i % 2 == 0:

                    relations.append('String %d %d %f\n' % (j * nx + i, j * nx + i + 1, k))

                if i % 2 == 1 and 0 < j < ny - 1:

                    relations.append('String %d %d %f\n' % (j * nx + i, j * nx + i + 1, k / 2))

            if j < ny - 1 and 0 < i and j % 2 == 0:

                relations.append('String %d %d %f\n' % (j * nx + i, (j + 1) * nx + i - 1, k))

            if j < ny - 1 and i < nx - 1 and j % 2 == 1:

                relations.append('String %d %d %f\n' % (j * nx + i, (j + 1) * nx + i + 1, k))

            if j < ny - 1 and 0 < i < nx - 1:

                if not ((i % 2 == 1 and j == 0) or (j == ny - 2 and i % 2 == 0)) :

                    relations.append('String %d %d %f\n' % (j * nx + i, (j + 1) * nx + i, k / 1.71))

            if i % 2 == 0 and j < ny - 1:

                if j % 2 == 0 and 0 < i and j < ny - 2:

                    relations.append('String %d %d %f\n' % (j * nx + i + 1, (j + 1) * nx + i - 1, k / 1.71))

                if j % 2 == 1:

                    if 0 < i:

                        relations.append('String %d %d %f\n' % (j * nx + i - 1, (j + 1) * nx + i + 1, k / 1.71))

                    if i < nx - 2:

                        relations.append('String %d %d %f\n' % (j * nx + i, (j + 1) * nx + i + 2, k / 1.71))
                        relations.append('String %d %d %f\n' % ((j + 1) * nx + i + 2, (j + 2) * nx + i, k / 1.71))

            if i < nx - 1 and i % 2 == 0 and j < ny - 2:

                if not ((i == 0 and j % 2 == 0) or (i == nx - 2 and j % 2 == 1)):

                    relations.append('String %d %d %f\n' % (j * nx + i, (j + 2) * nx + i + 1, k / 2))

            if i < nx - 1 and i % 2 == 0 and j < ny - 2:

                if not ((i == 0 and j % 2 == 0) or (i == nx - 2 and j % 2 == 1)):

                    relations.append('String %d %d %f\n' % (j * nx + i + 1, (j + 2) * nx + i, k / 1.71))


            if j < ny - 2:

                if not((i == 1 and j % 2 == 0) or (i == 0 and j % 2 == 0) or (i > nx - 3 and j % 2 == 1)):

                    relations.append('String %d %d %f\n' % (j * nx + i, (j + 2) * nx + i, k / 1.71))


def get_weights(weights, nx, ny):

    for j in range(ny):

        weights.append([])
        for i in range(nx):

            if i == 0 or i == nx - 1 or j == 0 or j == ny - 1:

                weights[j].append(frame_ratio / float(body_mass))

            else:

                weights[j].append(body_mass)

    if structure == 1 or structure == 2:

        for j in range(ny):

            for i in range(nx):

                if (j % 2 == 1 and i == 0) and not (j == ny - 1):

                    weights[j][i] = body_mass

                if (j % 2 == 0 and i == nx - 1) and not (j == 0 or j == ny - 1):

                    weights[j][i] = body_mass


if __name__ == '__main__':

    nx = int(sys.argv[1])
    ny = int(sys.argv[2])

    file_name = sys.argv[3]
    structure = int(sys.argv[4])

    solid_frame = True

    init_offset = 50
    x_offset = 26
    y_offset = 26

    k = 10
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
        print 'Plain grid READY !'

    if structure == 1:
        # # HONEYCOMB GRID
        twice_x_offset = x_offset * 2
        to_honeycomb(lambda x: x + x / 2, bodies)
        translate(Vector(init_offset, init_offset), bodies)

        honeycomb_relations(relations, nx, ny, k)
        print 'Honeycomb structure READY !'

    if structure == 2:

        # # HONEYCOMB GRID ex
        twice_x_offset = x_offset * 2
        to_honeycomb(lambda x: x + x / 2, bodies)
        translate(Vector(init_offset, init_offset), bodies)

        honeycomb_extended_relations(relations, nx, ny, k)
        print 'Honeycomb structure ex READY !'

    if solid_frame:

        frame_ratio = 10000

    get_weights(weights, nx, ny)

    with open(file_name, 'w') as output:

        for j in range(ny):

            for i in range(nx):

                output.write('Body %d %d %d %d\n' % (bodies[j][i].x,
                                                  bodies[j][i].y,
                                                  bodies[j][i].z,
                                                  weights[j][i]))

        for string in relations:

            output.write(string)
