import sys
import time
import math

import numpy
import scipy.weave

from body import Body
from interactions import String
from vector import Vector


class Integrator:

    def __init__(self, bodies_data, interaction_data):

        self.first_run = True
        self.interactions_size = len(interaction_data[0])
        self.max_energy = 0

        self.interactions = numpy.array(interaction_data[4])
        self.right = numpy.array(interaction_data[0])
        self.left = numpy.array(interaction_data[1])
        self.k = numpy.array(interaction_data[2])
        self.length = numpy.array(interaction_data[3])
        self.extension = numpy.zeros((self.interactions_size, 3))
        self.string_force = numpy.zeros((self.interactions_size, 3))
        self.string_potential_energy = numpy.zeros((self.interactions_size, 1))

        self.position = numpy.array(bodies_data[0])
        self.old_position = numpy.array(bodies_data[0])
        self.mass = numpy.array(bodies_data[1])

        self.bodies = len(self.position)

        self.new_position = numpy.zeros((self.bodies, 3))
        self.acceleration = numpy.zeros((self.bodies, 3))
        self.velocity_vector = numpy.zeros((self.bodies, 3))
        self.force = numpy.zeros((self.bodies, 3))

        self.body_potential_energy = numpy.zeros((self.bodies, 1))
        self.body_kinetic_energy = numpy.zeros((self.bodies, 1))
        self.body_total_energy = numpy.zeros((self.bodies, 1))
        self.speed = numpy.zeros((self.bodies, 1))

        self.system_total_energy = 0


            body.calculate(dt)

    def show_bodies(self):

        for body in self.bodies:

            print str(self.bodies.index(body)) + " " + body.show()

    def get_total_energy(self):

        energy = 0;
        for body in self.bodies:

            energy += body.total_energy

        return energy

    def get_max_energy(self):

        energy = -sys.maxint - 1

        for body in self.bodies:

            if body.total_energy > energy:

                energy = body.total_energy

        return energy

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
