import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor, QPen

from  myViewBox import CustomViewBox

class A_PlotWidget:

    def __init__(self):
        self.init()

    def init(self):
        self.vb = CustomViewBox()


        self.graphicsView = pg.PlotWidget(viewBox=self.vb)
        self.plt = self.graphicsView.plotItem

        #self.plt =


        self.lt = QVBoxLayout()
        self.lt.addWidget(self.graphicsView)
        self.setLayout(self.lt)

        self.plt.showGrid(True, True)


        self.colorsByInd = {
            0 : (255,0,0),
            1 : (0,255,0),
            2 : (0,0,255),
            3 : (255,255,0),
            4 : (0,255,255),
            5 : (255,0,255),
            6 : (128,128,0),
            7 : (128,0,128)
        }


        self.currChan = None


    def setCurrChan(self, N):
        self.currChan = N




    def setLabels(self, title, y, x):
        self.plt.setLabels(title=title, left=y, bottom=x)