from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Point import Point
from pyqtgraph import functions as fn

from PyQt5.QtCore import pyqtSignal

__all__ = ['ViewBox']

class CustomViewBox(pg.ViewBox):

    sigRangeSelect = pyqtSignal(QtCore.QRectF)

    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)

        self.setMouseMode(self.RectMode)
        self.setMouseMode(self.RectMode)

    def wheelEvent(self, ev, axis=None):
        mask = np.array(self.state['mouseEnabled'], dtype=np.float)
        if axis is not None and axis >= 0 and axis < len(mask):
            mv = mask[axis]
            mask[:] = 0
            mask[axis] = mv
        s = ((mask * 0.02) + 1) ** (ev.delta() * self.state['wheelScaleFactor'])  # actual scaling factor

        center = Point(fn.invertQTransform(self.childGroup.transform()).map(ev.pos()))
        # center = ev.pos()

        self._resetTarget()
        self.scaleBy(s, center)
        self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        ev.accept()

        rect = QtCore.QRectF()
        rect.setCoords(self.state['viewRange'][0][0], self.state['viewRange'][1][0], self.state['viewRange'][0][1],
                       self.state['viewRange'][1][1])
        self.sigRangeSelect.emit(rect)

    def mouseDragEvent(self, ev, axis=None):
        ev.accept()

        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1
        mouseEnabled = np.array(self.state['mouseEnabled'], dtype=np.float)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0

        if ev.button() & (QtCore.Qt.LeftButton | QtCore.Qt.MidButton):
            tr = dif * mask
            tr = self.mapToView(tr) - self.mapToView(Point(0, 0))
            x = tr.x() if mask[0] == 1 else None
            y = tr.y() if mask[1] == 1 else None

            self._resetTarget()
            if x is not None or y is not None:
                self.translateBy(x=x, y=y)
                self.sigRangeChangedManually.emit(self.state['mouseEnabled'])

                rect  = QtCore.QRectF()
                rect.setCoords(self.state['viewRange'][0][0], self.state['viewRange'][1][0], self.state['viewRange'][0][1], self.state['viewRange'][1][1])
                self.sigRangeSelect.emit(rect)


        elif ev.button() & QtCore.Qt.RightButton:
            if ev.isFinish():
                self.rbScaleBox.hide()
                ax = QtCore.QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))
                ax = self.childGroup.mapRectFromParent(ax)
                rect = ax
                self.showAxRect(ax)
                self.axHistoryPointer += 1
                self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]

                self.sigRangeSelect.emit(rect)



            else:
                self.updateScaleBox(ev.buttonDownPos(), ev.pos())
