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
        self.integration_code = """
        #include <math.h>

        float extension_length = 0, new_extension_length = 0;
        int x = 0, y = 0, z = 0, right_i = 0, left_i = 0;

        for(int index = 0; index < interactions_size; index++) {

        x = index * 3;
        y = x + 1;
        z = x + 2;

        left_i = left[index] * 3;
        right_i = right[index] * 3;

        extension[x] = position[left_i] - position[right_i];
        extension[y] = position[left_i + 1] - position[right_i + 1];
        extension[z] = position[left_i + 2] - position[right_i + 2];

        extension_length = sqrt(extension[x] * extension[x] +
        extension[y] * extension[y] +
        extension[z] * extension[z]);

        extension[x] = extension[x] * (extension_length - length[index]) / extension_length;
        extension[y] = extension[y] * (extension_length - length[index]) / extension_length;
        extension[z] = extension[z] * (extension_length - length[index]) / extension_length;

        string_force[x] = k[index] * extension[x];
        string_force[y] = k[index] * extension[y];
        string_force[z] = k[index] * extension[z];

        new_extension_length = sqrt(extension[x] * extension[x] +
        extension[y] * extension[y] +
        extension[z] * extension[z]);

        string_potential_energy[index] = k[index] * new_extension_length * new_extension_length / 2.0;

        body_force[right_i] -= string_force[x];
        body_force[right_i + 1] -= string_force[y];
        body_force[right_i + 2] -= string_force[z];

        body_force[left_i] += string_force[x];
        body_force[left_i + 1] += string_force[y];
        body_force[left_i + 2] += string_force[z];

        body_potential_energy[left_i] += string_potential_energy[index];
        body_potential_energy[right_i] += string_potential_energy[index];
        }

        for(int index = 0; index < bodies; index++) {

        x = index * 3;
        y = x + 1;
        z = x + 2;

        new_position[x] = 2 * position[x] - old_position[x] - body_force[x] * dt * dt;
        new_position[y] = 2 * position[y] - old_position[y] - body_force[y] * dt * dt;
        new_position[z] = 2 * position[z] - old_position[z] - body_force[z] * dt * dt;

        velocity_vector[x] = (new_position[x] - old_position[x]) / (2 * dt);
        velocity_vector[y] = (new_position[y] - old_position[y]) / (2 * dt);
        velocity_vector[z] = (new_position[z] - old_position[z]) / (2 * dt);

        speed[index] = sqrt(velocity_vector[x] * velocity_vector[x] +
        velocity_vector[y] * velocity_vector[y] +
        velocity_vector[z] * velocity_vector[z]);

        body_kinetic_energy[index] = mass[index] * speed[index] * speed[index] / 2.0;
        body_total_energy[index] = body_kinetic_energy[index] + body_potential_energy[index];

        old_position[x] = position[x];
        old_position[y] = position[y];
        old_position[z] = position[z];

        position[x] = new_position[x];
        position[y] = new_position[y];
        position[z] = new_position[z];

        body_force[x] = 0;
        body_force[y] = 0;
        body_force[z] = 0;

        body_potential_energy[index] = 0;
        }
        """

    def shift_body(self, index_of_body, shift):

        self.position[index_of_body] = numpy.add(self.position[index_of_body], shift)

    def integrate(self, dt):

        bodies = self.bodies
        position = self.position
        old_position = self.old_position
        new_position = self.new_position
        mass = self.mass
        acceleration = self.acceleration
        velocity_vector = self.velocity_vector
        body_force = self.force
        body_potential_energy = self.body_potential_energy
        body_kinetic_energy = self.body_kinetic_energy
        system_total_energy = self.system_total_energy
        body_total_energy = self.body_total_energy
        speed = self.speed
        right = self.right
        left = self.left
        k = self.k
        extension = self.extension
        length = self.length
        string_force = self.string_force
        string_potential_energy = self.string_potential_energy
        interactions_size = self.interactions_size

        scipy.weave.inline(self.integration_code,
                           ['bodies', 'position', 'old_position', 'new_position',
                            'mass', 'acceleration', 'velocity_vector',
                            'body_force', 'body_potential_energy', 'body_total_energy', 'speed',
                            'right', 'left', 'k', 'length', 'extension', 'body_kinetic_energy',
                            'string_force', 'string_potential_energy', 'interactions_size', 'dt',
                            'system_total_energy'],
                           headers=['<math.h>'])

    def get_total_energy(self):

        return numpy.sum(self.body_total_energy)

    def get_max_energy(self):

        return numpy.amax(self.body_total_energy)

    def normalize(self, value):

        return math.log(1 + value)

    def rate_function(self, body, steps):

        rate = int(steps - self.normalize(body.total_energy) * steps / self.max_energy) - 1
        if not (rate < 0):

            return rate

        else:

            return 0
