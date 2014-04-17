import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from grid_viewer import GridViewer
from integrator import Integrator
from body import Body
from interactions import String
from vector import Vector

delay = 10

def init_system(file_name, bodies, interactions):

    with open(file_name) as data:

        for line in data:

            tmp = line.split(' ')

            if tmp[0] == 'Body':

                x = float(eval(tmp[1]))
                y = float(eval(tmp[2]))
                z = float(eval(tmp[3]))
                m = float(eval(tmp[4]))

                bodies.append(Body(Vector(x, y, z), m))

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

    viewer.integrator.integrate(dt)
    viewer.repaint()
    timer.start(delay)


if __name__ == '__main__':

    if len(sys.argv) == 3:

        dt = 0.01

        bodies = []
        interactions = []

        app = QtGui.QApplication(sys.argv)
        integrator = Integrator()
        viewer = GridViewer(integrator, dt)

        init_system(sys.argv[1], bodies, interactions)

        integrator.add_bodies(bodies)
        integrator.add_interactions(interactions)

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
