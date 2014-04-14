import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from body import Body
from string import String
from vector import Vector

delay = 10

class Integrator(QtGui.QWidget):

    def __init__(self):

        super(Integrator, self).__init__()

        self.show()

        self.bodies = []
        self.interactions = []

    def add_bodies(self, bodies):

        self.bodies = bodies

    def add_body(self, body):

        if isinstance(body, Body):

            self.bodies.append(body)

        else:

            print "Not a physical body"

    def add_interactions(self, interactions):

        self.interactions = interactions

    def shift_body(self, index_of_body, shift):

        self.bodies[index_of_body].move_by(shift)

    def integrate(self, dt):

        for interaction in self.interactions:

            interaction.compute()

        for body in self.bodies:

            body.calculate(dt)

    def show_bodies(self):

        for body in self.bodies:

            print str(self.bodies.index(body)) + " " + body.show()

    def show_interactions(self):

        for interaction in self.interactions:

            print interaction.show()
