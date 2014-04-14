import sys

from body import Body
from string import String
from vector import Vector


class Integrator():

    def __init__(self):

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

    def normalize(self, value):

        return math.log(1 + value)

    def rate_function(self, body, steps):

        rate = int(steps - self.normalize(body.total_energy) * steps / self.max_energy) - 1
        if not (rate < 0):

            return rate

        else:

            return 0
