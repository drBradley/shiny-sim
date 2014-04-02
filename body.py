import math
import sys

from PyQt4 import QtGui, QtCore

from cartesian import Vector


class Body(object):

    def __init__(self, position, m):

        self.acting_forces = []

        self.position = position
        self.old_position = position
        self.mass = m
        self.acceleration = Vector(0, 0, 0)

        self.size = 20

    def calculate(self, dt):
        # calculate new position using Verlet algorith
        self.acceleration = self.compute_acceleration()
        self.new_position = 2 * self.position - self.old_position - self.acceleration * dt**2

        self.old_position = self.position;
        self.position = self.new_position;
        self.acting_forces = []

    def compute_acceleration(self):

        acc = Vector(0, 0, 0)
        for force in self.acting_forces:

            acc = acc + force / self.mass

        return acc

    def apply(self, force):

        self.acting_forces.append(force)

    def show(self):

        return "Position " + self.position.show() + " mass " + str(self.mass)
