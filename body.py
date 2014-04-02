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
        self.force = self.compute_force()
        self.new_position = 2 * self.position - self.old_position - self.force * dt**2

        self.old_position = self.position;
        self.position = self.new_position;
        self.acting_forces = []

    def compute_force(self):

        acc = Vector(0, 0, 0)
        for force in self.acting_forces:

            acc = acc + force / self.mass

        return acc

    def apply(self, force):

        self.acting_forces.append(force)

    def move_by(self, shift):

        self.old_position = self.position
        self.position = self.position + shift

    def show(self):

        return "Position " + self.position.show() + " mass " + str(self.mass)
