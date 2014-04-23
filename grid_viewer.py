import sys
import time
import math

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from integrator import Integrator


class GridViewer(QtGui.QWidget):

    def __init__(self, integrator, dt, k_list):

        super(GridViewer, self).__init__()
        self.setMouseTracking(True)

        self.k_index = 0
        self.k_list = k_list
        self.view_x = 0
        self.view_y = 0
        self.show()
        self.dt = dt
        self.updating = False
        self.left_clicked = False
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
            tresh = math.exp(self.integrator.max_energy * fraction) * 100 / math.exp(self.integrator.max_energy)

            painter.drawText(35, (index + 1) * self.size - self.size * 0.25, 
                             "%.4f %%" % tresh)

        painter.end()

    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            pos = event.pos()
            self.drag_start_x = pos.x()
            self.drag_start_y = pos.y()

            self.left_clicked = True

    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            self.left_clicked = False

    def mouseMoveEvent(self, event):

        if self.left_clicked:

            pos = event.pos()
            self.drag_end_x = pos.x()
            self.drag_end_y = pos.y()

            self.view_x +=  self.drag_end_x - self.drag_start_x
            self.view_y +=  self.drag_end_y - self.drag_start_y

            self.drag_start_x = pos.x()
            self.drag_start_y = pos.y()
        
    def paintEvent(self, event):

        if not self.updating:

            painter = QtGui.QPainter()
            painter.begin(self)

            for index, interaction in enumerate(self.integrator.interactions):

                if self.integrator.k[index] == self.k_list[self.k_index]:

                    l_index = interaction[0]
                    r_index = interaction[1]

                    startx = self.view_x + self.integrator.position[l_index][0]
                    starty = self.view_y + self.integrator.position[l_index][1]
                    endx = self.view_x + self.integrator.position[r_index][0]
                    endy = self.view_y + self.integrator.position[r_index][1]

                    painter.drawLine(startx, starty, endx, endy)

            for index, body_pos in enumerate(self.integrator.position):

                if not self.integrator.max_energy == 0:

                    rate = self.integrator.rate_function(index, self.steps)

                else:

                    rate = self.steps - 1

                painter.drawPixmap(self.view_x + body_pos[0] - self.size / 2,
                                   self.view_y + body_pos[1] - self.size / 2,
                                   self.pixmaps[rate])

            painter.drawPixmap(self.width() - 150,
                               50,
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
            print 'Max energy', self.integrator.get_max_energy(), self.integrator.get_total_energy()
