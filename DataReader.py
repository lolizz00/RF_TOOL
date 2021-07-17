from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
import numpy as np
import time
from ctypes import *

class DataReader(QObject):

    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    stop_signal = pyqtSignal()
    start_signal = pyqtSignal()

    data_signal = pyqtSignal(np.ndarray, int)

    # --------- shared

    def connectDLL(self):
        try:

            import platform
            arch = platform.architecture()[1]

            if '64' in arch:
                self.dll = cdll.LoadLibrary('pshow_get_x64.dll')
            else:
                self.dll = cdll.LoadLibrary('pshow_get_x32.dll')

            self.dll.pshow_get.restype = c_int
            self.dll.pshow_get.argtypes = \
                [
                    POINTER(c_uint32),  # channels_num

                    POINTER(c_int32),  # phase_add
                    POINTER(c_uint16),  # data

                    c_uint32,  # iq_max_num
                    c_uint32  # timeout_ms
                ]



        except Exception as e:
            print(e)


    def readSharedCycle(self):
        pass

    def readSharedUpd(self):
        pass

    def setSharedName(self, names):
        self.sharedNames = names

    # -----------

    def exitSlot(self):
        self.exitFlg = True

    def __init__(self):
        super(DataReader, self).__init__()

        self.runFlg = False
        self.exitFlg = False

        self.connectDLL()

    def log(self, _str, error=False):
        msg = 'DataReader :: ' + _str
        if not error:
            self.log_signal.emit(msg)
        else:
            self.error_signal.emit(msg)

    # 'check', 'once', 'step', 'timer'
    def setMode(self, mode):
        self.mode = mode

    # 1 - 8
    def setChanN(self, chanN):
        self.chanN = chanN

    # пауза при чтении по шагам
    def setPauseStep(self, pause):
        self.pausestep = pause / 1000

    # list of files
    def setFiles(self, files):
        self.files = files

    def stopSlot(self):
        self.stopFlg = True
        self.log("остановлен.")

        self.sleep(0.1)
        self.stop_signal.emit()

    # ЗАПУСК ПОТОКА
    def run(self):
        while not self.exitFlg:
            if self.runFlg:
                self.runFlg = False
                self.startHandle()
            self.sleep(0.1)

        print('DataReader finish')

    def setStartFlg(self):
        self.runFlg = True


    # ЗАПУСК
    def startHandle(self):

        self.log("запущен.")
        self.stopFlg = False
        self.dataHandl = False
        self.start_signal.emit()


        if self.mode == 'check':
            self.handleCheck()
        elif self.mode == 'once':
            self.handleOnce()
        elif self.mode == 'step':
            self.handleStep()
        elif self.mode == 'timer':
            self.timerFlg = False
            self.handleTimer()

    def setDataFromat(self, params):
        self.params = params

    def setIsCompl(self, isCompl):
        self.isCompl = isCompl

    def setMaxPnt(self, maxPnt):
        from math import log2, floor





        self.maxPnt = maxPnt

    def generateDataFormat(self):

        if self.params['end'] == 'little-endian':
            frmt =  '<'
        elif self.params['end'] == 'big-endian':
            frmt = '>'

        frmt = frmt + 'i'


        frmt = frmt + str(int(self.params['ln'] / 8))


        return frmt

    def handleCheck(self):
        self.log('Начинаем следить за файлами.')

        self.stopFlg = False
        self.old_stamp = [0 for i in range(self.chanN)]

        import os

        while not self.stopFlg:
            for i in range(self.chanN):
                stamp = os.stat(self.files[i]).st_mtime
                if stamp != self.old_stamp[i]:
                    self.old_stamp[i] = stamp
                    self.log("Изменились данные на " + str(i) + ' канале')

                    data = self._readFile(i)
                    self.data_signal.emit(data, i)


        self.log('Закончили следить за файлами')

    def _readFile(self, chanN):
        frmt = self.generateDataFormat()
        fName = self.files[chanN]

        maxPnt = self.maxPnt
        size = self.params['ln']



        fPtr = open(fName, 'rb')

        size = int(self.params['ln'] / 8) * self.maxPnt
        if not self.isCompl:
            packet = fPtr.read(size)
            data = np.frombuffer(packet, dtype=np.dtype(frmt))
        else:
            packet = fPtr.read(size)
            data = np.frombuffer(packet, dtype=np.dtype(frmt))

            I = data[0::2]
            Q = data[1::2]
            data = I + 1j * Q

        fPtr.close()

        return data

    def dataHandledSlot(self):
        self.dataHandl = True

    def handleOnce(self):

        err = False

        for i in range(self.chanN):
            try:
                data = self._readFile(i)
                self.data_signal.emit(data, i)
            except Exception as e:
                txt = str(e)
                self.error_signal.emit(txt)
                err = True
                break



        if not err:
            while not self.dataHandl:
                self.sleep(0.01)

        self.stopSlot()

    def sleep(self, val):
        from PyQt5.QtCore import QThread
        val = val * 100
        val= int(val)
        QThread.msleep(val)

    def timerSlot(self):
        self.timerFlg = True

    def handleTimer(self):

        while not self.stopFlg:
            self.sleep(1e-5)

            if self.timerFlg:
                self.timerFlg = False

                self.log_signal.emit('читаем по таймеру')

                for i in range(self.chanN):
                    data = self._readFile(i)
                    self.data_signal.emit(data, i)

    def handleStep(self):

        err = False

        try:
            flsPtr = [open(fName, 'rb') for fName in self.files]
        except Exception as e:
            self.stopSlot()
            txt = str(e)
            self.error_signal.emit(txt)
            return
        flsPtr = [ open(fName, 'rb')  for fName in self.files ]

        frmt = self.generateDataFormat()


        while not self.stopFlg: # пока вручную не остановили
            self.sleep(self.pausestep)

            for i in range(self.chanN): # идем по каналам
                data = np.array([])
                maxPnt = self.maxPnt

                size = int(self.params['ln'] / 8) * self.maxPnt

                if not self.isCompl:

                    packet = flsPtr[i].read(size)

                    data = np.frombuffer(packet, dtype=np.dtype(frmt))

                    if packet == b'':
                        flsPtr[i].seek(0)
                        continue

                    self.data_signal.emit(data, i)


                else:

                    packet = flsPtr[i].read(size)

                    data = np.frombuffer(packet, dtype=np.dtype(frmt))

                    if packet == b'':
                        flsPtr[i].seek(0)
                        continue


                    I = data[0::2]
                    Q = data[1::2]

                    data = I + 1j * Q

                    self.data_signal.emit(data, i)


        for t in flsPtr:
            t.close()