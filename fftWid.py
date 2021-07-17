from PyQt5.QtWidgets import QWidget, QVBoxLayout
from A_PlotWidget import A_PlotWidget
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import pyqtSignal
import numpy as np
from scipy.signal import find_peaks


class fftWid(QWidget, A_PlotWidget):

    update_marker_sig = pyqtSignal(int, float, float, int)

    add_marker_sig = pyqtSignal(int, float, float, int)

    data_first_sig = pyqtSignal()

    error_sig = pyqtSignal(str)

    list_mark_sig = pyqtSignal(type([]))
    mark_all_sig = pyqtSignal(type({}))

    def __init__(self, parent=None):
        super(fftWid, self).__init__(parent)



        self.setCorrLabels()

        self.graphicsView.scene().sigMouseClicked.connect(self.mouseDouble)

        self.timeClick = None
        self.markers = {}

        self.updFlg = False

        self.maxMarkCnt = 9

        self.thePeakVal = 10

    def findNear(self, freq, chanN):
        array = np.asarray(self.currData[chanN][0])
        idx = (np.abs(array - freq)).argmin()
        return idx

    def clear(self):
        self.plt.clear()
        self.currData = {}

    def clearMarkers(self):
        t = list(self.markers.keys())
        for _t in t:
            self.delMarkerSlot(_t)

    def delMarkerSlot(self, ID):
        try:
            pl = self.markers[ID][2]
        except:
            return
        if pl:
            self.plt.removeItem(pl[1])
            self.plt.removeItem(pl[0])

            self.plt.removeItem(pl[2][0])
            self.plt.removeItem(pl[2][1])
            self.plt.removeItem(pl[2][2])


        if ID in self.currDataFreqMark[self.currChan]:
            del self.currDataFreqMark[self.currChan][ID]

        del self.markers[ID]

        self.plotMarkers()

    def clearStart(self):
        self.updFlg = False

        self.vb.enableAutoRange('x', True)
        self.vb.enableAutoRange('y', True)

    def setMarkerWidth(self, ID, width):

        if width == 1:
            width = 0

        chan = self.markers[ID][1]
        width2 = int(width / 2)
        xMark = self.markers[ID][0]
        idX = self.findNear(xMark, chan)

        t1 = idX - width2
        t2 = idX + width2

        if t1 < 0 or t2 >= len(self.currData[chan][1]):
            return



        self.markers[ID][3] = width

    def plotMarkers(self):


        markerSym = ['t', 'd', '+', 'star', 'x']


        t  = []

        marks = {}

        for ID in self.markers:

            chan = self.markers[ID][1]
            xMark = self.markers[ID][0]

            idX = self.findNear(xMark, chan)
            freq = self.currData[chan][0][idX]

            if not self.markers[ID][3]:
                amp = self.currData[chan][1][idX]
                width = 0
            else:
                width = self.markers[ID][3]
                width2 =  int(width / 2)
                val = 0

                for i in range(idX - width2, idX + width2):
                   val = val +  self.currData[chan][1][i]
                val = val / width
                amp = val


            self.update_marker_sig.emit(ID, freq, amp, width)


            pl =  self.markers[ID][2]

            if pl:
                if pl[2][0]:
                    self.plt.removeItem(pl[2][0])
                    self.plt.removeItem(pl[2][1])
                    self.plt.removeItem(pl[2][2])

                _t = pl[1]
                _pl = pl[0]
            else:
                _t =  None
                _pl = None

            self.markers[ID][2] = self.genMarker(ID, freq, amp, width, idX, chan, _t, _pl)

            marks[ID] = [freq, amp]

            if chan == self.currChan:
                t.append(str(ID))

        self.list_mark_sig.emit(t)
        self.mark_all_sig.emit(marks)


    def genMarker(self, ID, freq, amp, width, idX, chan, t, pl):
        import pyqtgraph as pg
        from PyQt5.QtGui import QFont

        markerColor = (0, 0, 0)
        markerSize = 20
        markerWidth = 80
        markerTextSize = 13

        
        if not t:
            t = pg.TextItem(anchor=(0,0), text='M' + str(ID), color=markerColor)
            t.setTextWidth(markerWidth)
            font = QFont("times", markerTextSize)
            font.setBold(True)
            t.setFont(font)
            t.setPos(freq, amp)

            pl = pg.ArrowItem(angle=-90, brush=(0, 0, 0))
            pl.setPos(freq, amp)

            self.plt.addItem(t)
            self.plt.addItem(pl)

        else:
            t.setPos(freq, amp)
            pl.setPos(freq, amp)

        ln0 = None
        ln1 = None
        ln2 = None

        if width != 0:

           width2 = int(width/2)

           from pyqtgraph import mkPen
           from PyQt5 import QtCore
           _pen = mkPen('k', width=3, style=QtCore.Qt.DashLine)

           valLn0 = self.currData[chan][0][idX-width2]
           ln0 = pg.InfiniteLine(pos = valLn0, pen=_pen)

           valLn1 = self.currData[chan][0][idX + width2]
           ln1 = pg.InfiniteLine(pos=valLn1, pen=_pen)

           ln2 = self.plt.plot([valLn0, valLn1], [amp, amp], pen=_pen)


           self.plt.addItem(ln0)
           self.plt.addItem(ln1)



        return [pl, t, [ln0, ln1, ln2]]

    def sortPeaks(self):

        if not self.currData:
            return

        # TODO DIST

        the = np.mean(self.currData[self.currChan][1])

        from collections import OrderedDict
        from operator import itemgetter
        peaks_ind = OrderedDict(sorted(enumerate(self.currData[self.currChan][0]),\
                                       key=itemgetter(1), reverse=True))


        peaks = {}
        for i in range(len(peaks_ind)):
            peaks[self.currData[self.currChan][0][i]] = self.currData[self.currChan][1][i]

        import operator
        peaks = sorted(peaks.items(), key=operator.itemgetter(1), reverse=True)

        peaks = [peaks[i][0] for i in range(len(peaks))]

        return peaks

    def nearest(self, lst, target):
        return min(lst, key=lambda x: abs(x - target))

    def setThePeak(self, val):
        self.thePeakVal = val

    def addMarkerPeak(self):

        ID = self.getFreeMarkFreeID()

        if ID == None:
            self.error_sig.emit('Максимальное кол-во маркеров!')
            return

        if self.currData == {}:
            return



        _mrk = list(self.currDataFreqMark[self.currChan].values()) # получаем частоты занятых пиков на этом канале

        peaks = self.sortPeaks()  # получаем индексы найденных пиков


        if len(_mrk):
            for i in range(len(peaks)): # идем по пикам
                nr = self.nearest(_mrk, peaks[i])
                if abs(nr - peaks[i]) > self.thePeakVal:
                    freq = peaks[i]
                    break
        else:
            freq = peaks[0]



        amp = 0

        self.currDataFreqMark[self.currChan][ID] = freq

        self.markers[ID] = [freq, self.currChan, None, None]

        self.add_marker_sig.emit(self.currChan, freq, amp, ID)

        self.plotMarkers()

    def getFreeMarkFreeID(self):
        ids = list(self.markers.keys())

        _x = list(range(self.maxMarkCnt))

        free = [t for t in _x if not t in ids]

        if not free:
            return None

        return free[0]

    def mouseDouble(self, evt):
        tp = str(type(evt))
        if not 'MouseClickEvent'  in tp:
            return
        tim = evt._time
        if not self.timeClick:
            self.timeClick = tim
            return
        diff = abs(self.timeClick - tim)

        if diff > 0.5:
            self.timeClick = tim
            return


        t = evt._scenePos
        mousePoint = self.plt.vb.mapSceneToView(t)
        xMark = mousePoint.x()
        y = mousePoint.y()


        if self.currChan != None:
            idX = self.findNear(xMark, self.currChan)
            freq = self.currData[self.currChan][0][idX]
            amp = self.currData[self.currChan][1][idX]



            # -----
            ID = self.getFreeMarkFreeID()

            if ID == None:
                self.error_sig.emit('Максимальное кол-во маркеров!')
                return

            self.markers[ID] = [xMark, self.currChan, None, None]

            self.add_marker_sig.emit(self.currChan, freq, amp, ID)
        else:
            print('None chan')

        self.plotMarkers()

        self.timeClick = tim

    def setCorrLabels(self):
        self.setLabels('БПФ', 'Уровень, dBFS', 'Частота')

    def setChanN(self, n):
        self.chanN = n
        self.clear()

        self.plots = {}
        self.currData = {}
        self.markers = {}
        self.currDataFreqMark = {}

    def createPenList(self, chanN):

        if self.chanN == 1:
            alpha = 255
        else:
            alpha = 255 / 2


        qcolor = QColor()
        qcolor.setRgb(self.colorsByInd[chanN][0], self.colorsByInd[chanN][1], self.colorsByInd[chanN][2], alpha)
        pen = QPen()
        pen.setColor(qcolor)
        pen.setWidth(1 / 1e2)
        return pen

    def dataIn(self, x, y, n):

        if not n in self.plots:
            self.currDataFreqMark[n] = {}


        pen = self.createPenList(n)

        try:

            if n in self.plots:

                if len(x) == len(y):
                    self.plots[n].setData(x, y, pen=pen)
            else:
                self.plots[n] = self.plt.plot(x, y, pen=pen)


            if self.currChan != None:
                actPlot = self.plots[self.currChan]
                self.plt.removeItem(actPlot)
                self.plt.addItem(actPlot)


            self.currData[n] = [x, y]

            self.plotMarkers()

            if not self.updFlg:
                self.updFlg = True
                self.vb.enableAutoRange('x', False)
                self.vb.enableAutoRange('y', False)
                self.data_first_sig.emit()

        except:
            pass




