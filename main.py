import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from integrator import Integrator
from body import Body
from string import String
from vector import Vector

delay = 10

def init_system(file_name, bodies, interactions):

    with open(file_name) as data:

        for line in data:

            tmp = line.split(' ')

            if tmp[0] == 'Body':

                x = float(tmp[1])
                y = float(tmp[2])
                m = float(tmp[3])

                bodies.append(Body(Vector(x, y), m))

            elif tmp[0] == 'String':

                right = int(tmp[1])
                left = int(tmp[2])
                k = float(tmp[3])

                interactions.append(String(bodies[right],
                                           bodies[left],
                                           k))

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
                displacement = Vector(x, y, z)
                integrator.shift_body(index, displacement)

def run():

    integrator.integrate(dt)
    integrator.repaint()
    timer.start(delay)


if __name__ == '__main__':

    if len(sys.argv) == 3:

        dt = 0.01
        k = 1

        bodies = []
        interactions = []

        app = QtGui.QApplication(sys.argv)
        integrator = Integrator()

        init_system(sys.argv[1], bodies, interactions)

        integrator.add_bodies(bodies)
        integrator.add_interactions(interactions)

        configure_system(sys.argv[2], integrator)

        timer = QTimer()
        timer.timeout.connect(run)
        timer.start(50)

        sys.exit(app.exec_())

    else:

        print "Insufficient amount of parameters"
