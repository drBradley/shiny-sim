import math
import sys

from PyQt4 import QtGui, QtCore

class Particle(object):

    def __init__(self, extension, old_extension, m, k):

        self.neighbours = []

        self.extension = extension
        self.old_extension = old_extension

        self.velocity = 0

        self.mass = m
        self.k = k
        self.omega2 = self.k / self.mass

        self.size = 20

    def verlet(self, dt):

        self.acceleration = self.compute_acceleration()
        self.new_extension = 2 * self.extension - self.old_extension - self.acceleration * dt * dt

        self.velocity = (self.new_extension  - self.old_extension) / (2.0 * dt);

        self.old_extension = self.extension;
        self.extension = self.new_extension;

    def attach(self, particle):

        if not particle in self.neighbours:

            self.neighbours.append(particle)
            particle.add(self)

    def add(self, particle):

        if not particle in self.neighbours:

            self.neighbours.append(particle)

    def compute_acceleration(self):

        acc = 0
        for neighbour in self.neighbours:

            acc += self.k / self.mass *(self.extension - neighbour.extension)

        return acc

    def is_wall(self):

        return self.fixed

    def get_extension(self):

        return self.extension

    def get_init_extension(self):

        return self.init_extension

    def show(self):

        return str(self.extension) + "\t" + str(self.velocity)

    def draw(self, painter, x):

        painter.drawEllipse(x + self.extension - self.size, 200, self.size, self.size)


class Spring(object):

    def __init__(self, k):

        self.k = k;

    def connect_left_end(self, p):

        self.left = p

    def connect_right_end(self, p):

        self.right = p


