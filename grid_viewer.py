import sys
import time
import math

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from integrator import Integrator


class GridViewer(QtGui.QWidget):

    def __init__(self, integrator, dt):

        super(GridViewer, self).__init__()

        self.show()
        self.dt = dt
        self.updating = False
        self.size = 20
        self.steps = 255
        self.divisor = 8
        self.pixmaps = []
        self.integrator = integrator
        self.prepare_maps()

        self.color_key =  QtGui.QPixmap(150, self.steps * self.size / self.divisor + 50)

    def prepare_color_key(self):

        self.color_key.fill(QtGui.QColor(0, 0, 0, 0))
        painter = QtGui.QPainter(self.color_key)
        painter.begin(self)

        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.drawText(10, 0, str(self.integrator.max_energy))

        treshes = xrange(int(self.steps / self.divisor))

        for index in treshes:

            painter.drawPixmap(10,
                               index * self.size,
                               self.pixmaps[index * self.divisor])

            painter.setPen(QtGui.QColor(0, 0, 0))

            fraction = float(self.steps - index * self.divisor) / self.steps
            tresh = self.integrator.max_energy * fraction

            painter.drawText(35, (index + 1) * self.size - self.size * 0.25, 
                             str(tresh))

        painter.end()
        
    def paintEvent(self, event):

        if not self.updating:

            painter = QtGui.QPainter()
            painter.begin(self)

            for interaction in self.integrator.interactions:

                interaction.draw(painter)

            for body in self.integrator.bodies:

                pos = body.position
                if not self.integrator.max_energy == 0:

                    rate = self.integrator.rate_function(body, self.steps)

                else:

                    rate = 0

                painter.drawPixmap(pos.x - self.size / 2,
                                   pos.y - self.size / 2,
                                   self.pixmaps[rate])

            painter.drawPixmap(1700,
                               100,
                               self.color_key)

            painter.end()

    def prepare_maps(self):

        self.updating = True

        self.pixmaps = []
        for treshold in xrange(self.steps):

            qmap = QtGui.QPixmap(self.size + 1, self.size + 1)
            qmap.fill(QtGui.QColor(0, 0, 0, 0))
            painter = QtGui.QPainter(qmap)

            color = QtGui.QColor()
            color.setHsv(int(255 * treshold / self.steps), 220, 220, 70)
            painter.setPen(color)
            painter.setBrush(color)
            painter.drawEllipse(0, 0, self.size, self.size)
            self.pixmaps.append(qmap)
            painter.end()

        self.updating = False

    def keyPressEvent(self, event):

        key = event.key()

        if key == QtCore.Qt.Key_Escape:

            self.close()

        if key == QtCore.Qt.Key_R:

            self.integrator.max_energy = self.integrator.normalize(self.integrator.get_max_energy())
            self.prepare_maps()
            self.prepare_color_key()
