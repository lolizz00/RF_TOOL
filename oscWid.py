from PyQt5.QtWidgets import QWidget, QVBoxLayout
from A_PlotWidget import A_PlotWidget
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import pyqtSignal


class oscWid(QWidget, A_PlotWidget):



    def __init__(self, parent=None):
        super(oscWid, self).__init__(parent)
        self.setCorrLabels()

        self.len = 100

    def clear(self):
        self.plt.clear()


    def setCorrLabels(self):
        self.setLabels('Осциллограмма', 'Значение', 'Отсчеты')

    def setChanN(self, n):
        self.chanN = n
        self.clear()
        self.plots = {}

    def createPenList(self, chanN):

        if self.chanN == 1:
            alpha = 255
        else:
            alpha = 255 / 2


        qcolor = QColor()
        qcolor.setRgb(self.colorsByInd[chanN][0], self.colorsByInd[chanN][1], self.colorsByInd[chanN][2], alpha)
        pen = QPen()
        pen.setColor(qcolor)
        pen.setWidth(1 / 50)
        return pen

    def clearStart(self):
        self.updFlg = False

        self.vb.enableAutoRange('x', True)
        self.vb.enableAutoRange('y', True)

    def setOscLen(self, _len):
        self.len = _len

        self.vb.enableAutoRange('x', True)
        self.vb.enableAutoRange('y', True)
        self.updFlg = False

    def dataIn(self, x, y, n):

        pen = self.createPenList(n)


        if len(x)  > self.len:
            x = x[:self.len]
            y = y[:self.len]


        if not n in self.plots:
            t1 = self.plt.plot(x, y, pen=pen )
            t2 = self.plt.plot(x, y, symbolPen=pen, symbolSize=2 * 3, pen=None)

            self.plots[n] = [t1, t2]
        else:
            t1, t2 = self.plots[n]
            t1.setData(x, y, pen=pen )
            t2.setData(x, y, symbolPen=pen, symbolSize=2 * 3, pen=None)

        if not self.updFlg:
            self.updFlg = True
            self.vb.enableAutoRange('x', False)
            self.vb.enableAutoRange('y', False)


