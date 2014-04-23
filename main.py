import sys
import math

import numpy
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from grid_viewer import GridViewer
from integrator import Integrator
from body import Body
from interactions import String
from vector import Vector

delay = 10
k_list = []

def init_system(file_name, bodies, interactions):

    with open(file_name) as data:

        for line in data:

            tmp = line.split(' ')

            if tmp[0] == 'Body':

                x = float(eval(tmp[1]))
                y = float(eval(tmp[2]))
                z = float(eval(tmp[3]))
                m = float(eval(tmp[4]))

                bodies[0].append([x, y, z])
                bodies[1].append([m])

            elif tmp[0] == 'String':

                right = int(tmp[1])
                left = int(tmp[2])
                k = float(tmp[3])

                if k not in k_list:

                    k_list.append(k)

                interactions[0].append([right])
                interactions[1].append([left])
                interactions[2].append([k])
                interactions[4].append([left, right])
                interactions[3].append([math.sqrt((bodies[0][left][0] - bodies[0][right][0])**2 +
                                                  (bodies[0][left][1] - bodies[0][right][1])**2 +
                                                  (bodies[0][left][2] - bodies[0][right][2])**2)])

def configure_system(file_name, integrator):

    with open(file_name) as data:

        for line in data:

            tmp = line.split(' ')

            if tmp[0] == 'move':

                index = int(eval(tmp[1]))
                x = float(eval(tmp[2]))
                y = float(eval(tmp[3]))
                z = float(eval(tmp[4]))
                print 'Moving ',index, ' by [',x, y, z, ']'
                displacement = numpy.array([x, y, z])
                integrator.shift_body(index, displacement)

def run():

    viewer.integrator.integrate(dt)
    viewer.repaint()
    timer.start(delay)


if __name__ == '__main__':

    if len(sys.argv) == 3:

        dt = 0.01

        bodies = [[], []]
        interactions = [[], [], [], [], []]

        app = QtGui.QApplication(sys.argv)

        init_system(sys.argv[1], bodies, interactions)

        integrator = Integrator(bodies, interactions)
        viewer = GridViewer(integrator, dt, k_list)

        configure_system(sys.argv[2], integrator)

        integrator.integrate(dt)
        integrator.max_energy = integrator.normalize(integrator.get_max_energy())
        viewer.prepare_color_key()

        timer = QTimer()
        timer.timeout.connect(run)
        timer.start(10)

        sys.exit(app.exec_())

    else:

        print "Insufficient amount of parameters"
