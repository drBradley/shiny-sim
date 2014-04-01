import sys
from time import sleep

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from particle import Particle

delay = 10

class Main(QtGui.QWidget):

    def __init__(self):

        super(Main, self).__init__()

        self.setWindowTitle('Oscilator')
        self.show()

        self.particles = []

    def integrate(self, dt):

        for p in self.particles:

            p.verlet(dt)

    def add_particle(self, list_of_particles):

        self.particles.append(list_of_particles)

    def set_bounds_between_particles(self):

        for i in range(len(self.particles) - 1):

            self.particles[i].attach(self.particles[i + 1])

    def paintEvent(self, event):

        i = 1
        painter = QtGui.QPainter()
        painter.begin(self)

        for p in self.particles:

            p.draw(painter, 100 + 50 * i)
            i += 1

        painter.end()

    def keyPressEvent(self, event):

        key = event.key()

        if key == QtCore.Qt.Key_Escape:

            self.close()

def work():

    main.integrate(dt)
    main.repaint()
    timer.start(delay)

if __name__ == '__main__':

    dt = 0.01
    dx = 1
    x = 1
    k = 1
    m = 1

    app = QtGui.QApplication(sys.argv)
    main = Main()

    main.add_particle(Particle(0, 0, 100, 10))
    main.add_particle(Particle(1, 1, 1, 10))
    main.add_particle(Particle(1, 1.1, 1, 10))
    main.add_particle(Particle(1, 1, 1, 10))
    main.add_particle(Particle(1, 1, 1, 10))
    main.add_particle(Particle(1, 1, 1, 10))
    main.add_particle(Particle(1, 1, 100, 10))

    main.set_bounds_between_particles()

    timer = QTimer()
    timer.timeout.connect(work)
    timer.start(50)

    sys.exit(app.exec_())
