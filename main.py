import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from integrator import Integrator
from body import Body
from string import String
from cartesian import Vector

delay = 10

def run():

    integrator.integrate(dt)
    integrator.repaint()
    timer.start(delay)

if __name__ == '__main__':

    dt = 0.01
    k = 1

    bodies = [Body(Vector(100, 100), 1000),
              Body(Vector(200, 100), 1),
              Body(Vector(300, 100), 1000)]

    interactions = [String(bodies[0],
                           bodies[1],
                           k),
                    String(bodies[1],
                           bodies[2],
                           k),
                ]

    app = QtGui.QApplication(sys.argv)
    integrator = Integrator()

    integrator.add_bodies(bodies)
    integrator.add_interactions(interactions)

    integrator.shift_body(1, Vector(1, 0, 0))

    timer = QTimer()
    timer.timeout.connect(run)
    timer.start(50)

    sys.exit(app.exec_())
