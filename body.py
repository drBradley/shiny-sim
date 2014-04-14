import math
import sys
from abc import ABCMeta, abstractmethod

from PyQt4 import QtGui, QtCore

from vector import Vector


class PhysicalBody:
    __metaclass__ = ABCMeta

    @abstractmethod
    def apply(self):

        pass

    def calculate(self):

        pass

    def move_by(self):

        pass


class Body(PhysicalBody):

    def __init__(self, position, m):

        self.force = Vector(0, 0, 0)
        self.potential_energy = 0

        self.position = position
        self.old_position = position
        self.mass = m
        self.acceleration = Vector(0, 0, 0)
        self.size = 20
        self.potential_energy = 0
        self.kinetic_energy = 0
        self.total_energy = 0

    def calculate(self, dt):
        # calculate new position using Verlet algorithm

        self.new_position = 2 * self.position - self.old_position - self.force * dt**2

        velocity = (self.new_position - self.old_position) / (2 * dt)
        self.kinetic_energy = self.mass * abs(velocity) * abs(velocity) / 2
        self.total_energy = self.potential_energy + self.kinetic_energy

        self.old_position = self.position;
        self.position = self.new_position;

        self.force = Vector(0, 0, 0)
        self.potential_energy = 0

    def move_by(self, shift):

        self.old_position = self.position
        self.position = self.position + shift

    def show(self):

        return "Position " + self.position.show() + " mass " + str(self.mass)
