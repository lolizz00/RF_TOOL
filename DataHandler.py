from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
import time
import numpy as np
from scipy.fftpack import fft, fftfreq, fftshift
from scipy.signal import get_window
from scipy.signal import find_peaks

class DataHandler(QObject):

    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    stop_signal = pyqtSignal()

    osc_signal = pyqtSignal(np.ndarray, np.ndarray, int)
    fft_signal = pyqtSignal(np.ndarray, np.ndarray, int)

    data_in_sig = pyqtSignal()

    def sleep(self, val):
        from PyQt5.QtCore import QThread
        val = val * 100
        val= int(val)
        QThread.msleep(val)
        
    
    def log(self, _str, error=False):
        msg = 'DataHandler :: ' + _str
        if not error:
            self.log_signal.emit(msg)
        else:
            self.error_signal.emit(msg)

    def __init__(self):

        self.midCnt = 1


        self.midErrSch = 0

        super(DataHandler, self).__init__()

        self.dataIn = []
        self.stopFlg = False

        self.wins = {
            'Нет': None,
            'Bartlett': 'bartlett',
            'Blackman-Harris': 'blackmanharris',
            'triangular': 'triang',
            'Parzen': 'parzen'
        }


        self.runFlg = False
        self.exitFlg = False


    # количество каналов
    # fs
    # максимальное значение
    # окно
    # комплекный ли спектр
    # считаем ли спектр
    def setParams(self, chanN, fs, maxRef,  isComplFFT, isMid):
        self.chanN = chanN
        self.fs = fs
        self.maxref = maxRef
        self.isComplFFT = isComplFFT
        self.isMid = isMid

        self.clearMidSlot()


    def clearMidSlot(self):
        self.data = [[] for i in range(self.chanN)]


    def dataInSlot(self, data, chanN):
        self.dataIn.append([data, chanN])

    def stopSlot(self):
        self.stopFlg = True
        self.log("остановлен.")
        self.stop_signal.emit()

    def setOscEn(self, en):
        self.oscEn = en

    def setFftEn(self, en):
        self.fftEn = en

    def run(self):
        while not self.exitFlg:
            if self.runFlg:
                self.runFlg = False

                self.dataIn = []
                self.clearMidSlot()

                self.handleStart()
            self.sleep(0.1)

        print('DataReader finish')

    def setStartFlg(self):
        self.runFlg = True


    # ЗАПУСК

    def exitSlot(self):
        self.exitFlg = True

    def handleStart(self):
        self.log("запущен.")

        self.stopFlg = False

        while True:
            self.sleep(0.00001)
            if len(self.dataIn):

                self.data_in_sig.emit()

                data = self.dataIn.pop(0)
                if self.oscEn:
                    self.calcOsc(data[0], data[1])
                if self.fftEn:
                    self.calcFFT(data[0], data[1])

            if self.stopFlg:
                break



    def calcOsc(self, data, chanN):

        if not len(data):
            return

        tp = str(type(data[0]))
        if 'complex' in tp:
            from helper import complToReal
            data = complToReal(data, self.fs)
        y = data
        x = np.arange(len(y))
        self.osc_signal.emit(x, y, chanN)


    def setWindow(self, win):
        self.win = self.wins[win]

    def setMidCnt(self, midCnt):
        self.midCnt = midCnt

    def handleMidFFT(self, data, chanN):
        if not len(self.data[chanN]):
            self.data[chanN] = []
            self.data[chanN].append(data)
            return data
        else:

            try:

                _data = self.data[chanN][0]

                if len(_data) == len(data):

                    self.midErrSch = 0

                    self.data[chanN].append(data)

                    while len(self.data[chanN]) > self.midCnt:
                        self.data[chanN].pop(0)

                    for i in range(1, len(self.data[chanN])):
                        _data = _data + self.data[chanN][i]


                    _data = _data / len(self.data[chanN])

                else:

                    for i in range(1, len(self.data[chanN])):
                        _data = _data + self.data[chanN][i]

                    _data = _data / len(self.data[chanN])

                    self.midErrSch = self.midErrSch + 1
                    if self.midErrSch == 3:
                        self.midErrSch = 0
                        self.data[chanN] = []


            except Exception as e:
                self.data[chanN] = []


        return _data


    def calcFFT(self, y, chanN):

        from math import floor, log2

        #n = 2 ** floor(log2(len(y)))
        n = len(y)

        y = y[:n]


        N = len(y)
        T = 1 / self.fs
        if not N:
            return

        if self.win != None:
            win = get_window(self.win, N)
            y = y * win




        yf = fft(y)

        if not self.isComplFFT:
            xf = fftfreq(N, T)[:N // 2]
            yf = 2.0 / N * np.abs(yf[0:N // 2])
        else:
            xf = fftfreq(N, T)

            xf = fftshift(xf)
            yf = fftshift(yf)
            yf = 1.0 / N * np.abs(yf)

        yf = 20 * np.log10(yf / self.maxref)

        yf = self.handleMidFFT(yf, chanN)

        self.fft_signal.emit(xf, yf, chanN)