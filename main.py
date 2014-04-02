import sys
from time import sleep

from body import Body
from string import String
from cartesian import Vector

delay = 10

class Main(object):

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


if __name__ == '__main__':

    dt = 0.01
    k = 1

    m = Main()

    bodies = [Body(Vector(1, 1), 100),
              Body(Vector(2, 1), 1),
              Body(Vector(3, 1), 100)]

    interactions = [String(bodies[0],
                           bodies[1],
                           k),
                    String(bodies[1],
                           bodies[2],
                           k),
                ]

    m.add_bodies(bodies)
    m.add_interactions(interactions)

    # m.show_bodies()
    # m.show_interactions()

    m.integrate(dt)
