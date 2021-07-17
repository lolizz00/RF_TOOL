from mwui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QHeaderView,QAbstractItemView, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QThread, QTimer,pyqtSignal
from PyQt5.QtGui import  QIcon
import PyQt5.QtCore

from DataHandler import DataHandler
from DataReader import DataReader

from PyQt5.QtWidgets import QAction, QMenu, QTableWidget,  QGraphicsAnchorLayout, QToolButton
from PyQt5.QtCore import Qt
import PyQt5.QtGui as gui
from PyQt5.QtGui import QBrush, QColor, QPixmap

from startform import StartFrom

class MW(QMainWindow, Ui_MainWindow):

    start_sig = pyqtSignal()
    stop_signal = pyqtSignal()
    exit_sig = pyqtSignal()

    del_marker_sig = pyqtSignal(int)
    add_markerpeak_sig = pyqtSignal()
    clear_mid_sig = pyqtSignal()

    def showInfoMe(self):
        from InfoMe import InfoMe
        self.inf = InfoMe()
        self.inf.show()

    def showMeasAll(self):
        self.measWid.tabWidget.setCurrentIndex(0)
        self.measWid.setMinimumSize(0, 150)
        self.measWid.setMaximumSize(1e5, 150)

    def genToolTipStyle(self, ptr):
        ptr.setStyleSheet("QToolTip { \
    font-size:9pt; \
    color:white; padding:2px; \
    border-width:2px;\
    border-style:solid;\
    border-radius:20px;\
    background-color: black;\
    border: 1px solid white;}")



    def readConf(self):

        from PyQt5.QtWidgets import QLineEdit, QCheckBox, QRadioButton, QComboBox

        try:
            f = open('conf.conf', 'r')

            for line in f:
                line = line.replace('\n', '')

                line = line.split('\t')

                if len(line) == 2: line.append('')

                name, typ,  val = line


                if typ == 'QLineEdit':
                    obj = self.startWid.findChildren(QLineEdit, name)[0]
                    obj.setText(val)
                elif typ == 'QCheckBox':
                    obj = self.startWid.findChildren(QCheckBox, name)[0]
                    obj.setChecked(int(val))
                elif typ == 'QRadioButton':
                    obj = self.startWid.findChildren(QRadioButton, name)[0]
                    obj.setChecked(int(val))
                elif typ == 'QComboBox':
                    obj = self.startWid.findChildren(QComboBox, name)[0]
                    obj.setCurrentIndex(int(val))


        except:
            print('No conf file')

    def saveConf(self):

        from PyQt5.QtWidgets import  QLineEdit, QCheckBox, QRadioButton, QComboBox

        listLine = self.startWid.findChildren(QLineEdit)
        listCheck = self.startWid.findChildren(QCheckBox)
        listRadio = self.startWid.findChildren(QRadioButton)
        listCombo = self.startWid.findChildren(QComboBox)


        f = open('conf.conf', 'w')

        for t in listLine:
            if not 'qt_' in t.objectName():
                f.write(t.objectName() + '\tQLineEdit\t'+  t.text() + '\n')

        for t in listCheck:
            if not 'qt_' in t.objectName():
                if t.isChecked():
                    val = 1
                else:
                    val = 0
                f.write(t.objectName() +  '\tQCheckBox\t'  + str(val)+ '\n')

        for t in listRadio:
            if not 'qt_' in t.objectName():
                if t.isChecked():
                    val = 1
                else:
                    val = 0
                f.write(t.objectName() + '\tQRadioButton\t'  + str(val) + '\n')

        for t in listCombo:
            if not 'qt_' in t.objectName():
                f.write(t.objectName() + '\tQComboBox\t' + str(t.currentIndex())+ '\n')

        f.close()

    def initMenu(self):

        self.btnRun = QAction(QIcon("icon/n.png"), "actRun", self)
        self.btnUpd = QAction(QIcon("icon/r.png"), "actUpd", self)
        self.btnStop = QAction(QIcon("icon/s.png"), "actStop", self)
        self.btnInfo = QAction(QIcon("icon/i.png"), "actStop", self)

        self.btnConf = QAction(QIcon("icon/config.png"), "act1", self)

        self.btnRun.setToolTip('Считать последовательно')
        self.btnUpd.setToolTip('Считать при изменении')

        self.btnStop.setToolTip('Остановить')
        self.btnInfo.setToolTip('Информация')
        self.btnConf.setToolTip('Настройка')

        self.toolbar = self.addToolBar("Run")



        menu = QMenu()
        act1 = menu.addAction('Дельта-маркеры')
        act1.triggered.connect(self.showMeasAll)

        # -----


        # ----

        self.measTool = QToolButton(self.toolbar)
        self.measTool.setPopupMode(QToolButton.InstantPopup)
        self.measTool.setIcon(QIcon("icon/m.png"))
        self.measTool.setMenu(menu)

        self.measTool.setToolTip('Измерения')

        self.toolbar.addAction(self.btnRun)
        self.toolbar.addAction(self.btnUpd)
        self.toolbar.addAction(self.btnStop)
        self.toolbar.addAction(self.btnConf)
        self.toolbar.addWidget(self.measTool)
        self.toolbar.addAction(self.btnInfo)

        self.genToolTipStyle(self.toolbar)

        self.btnRun.triggered.connect(self.actionRun)
        self.btnUpd.triggered.connect(self.actionUpd)
        self.btnStop.triggered.connect(self.actionStop_)
        self.btnInfo.triggered.connect(self.showInfoMe)
        self.btnConf.triggered.connect(self.acttionConfig)

    def acttionConfig(self):
        self.stopClicked()
        self.hide()
        self.startWid.show()

    def clearAllMark(self):
        table = self.newTableMark
        while table.rowCount():
            self.markerClickSlot(0, 4)

    def markerClickSlot(self, row, col):
        if col == 4:
            table = self.newTableMark
            id = int(table.item(row, 0).text().replace('M', ''))
            self.del_marker_sig.emit(id)
            table.removeRow(row)


    def stringCutter(self, str, cnt=3):
        pass

    def updateValsSlot(self, ID, freq, amp, width):
        freq = round(freq, 1)
        amp = int(amp)

        table = self.newTableMark

        for i in range(table.rowCount()):
            _id = int(table.item(i, 0).text().replace('M', ''))
            if _id == ID:

                if not table.item(_id, 3):
                    return

                table.item(_id, 1).setText(str(freq))
                table.item(_id, 2).setText(str(amp))

                if width:
                    table.item(_id, 5).setText('Width:' + str(width))
                else:
                    table.item(_id, 5).setText('')

                break

    def stringCut(self, st, max):
        pass

    def addMarkerClickSlot(self, chanN, freq, amp, ID):
        table = self.newTableMark
        newID = table.rowCount()
        table.setRowCount(newID + 1)

        item = QTableWidgetItem()
        item.setText('M' + str(ID))
        table.setItem(newID, 0,item)

        freq = round(freq, 1)

        #amp = round(amp, 1)


        table.setItem(newID, 1, QTableWidgetItem(str(freq)))


        amp = int(amp)
        item = QTableWidgetItem()
        item.setText(str(amp))
        table.setItem(newID, 2, item)



        item = QTableWidgetItem()
        item.setText('Канал №' + str(chanN))
        item.setForeground(QBrush(QColor(self.colorsByInd[chanN][0],\
                                         self.colorsByInd[chanN][1], self.colorsByInd[chanN][2])))
        table.setItem(newID, 3, item)

        item = QTableWidgetItem()
        item.setIcon(QIcon('icon/delete.png'))
        table.setItem(newID, 4, item)

        item = QTableWidgetItem()
        table.setItem(newID, 5, item)

        # item.setForeground(QBrush(QColor(0, 255, 0)))

    def initNewMark(self):
        self.newTableMark = QTableWidget(self.specWid.graphicsView)
        table = self.newTableMark

        # border: 0px solid #333333;

        table.setStyleSheet("QTableWidget { border: none;"
                           " background-color: transparent; }"
              "QHeaderView::section {background-color: transparent;}"
              "QHeaderView {background-color: transparent;}"
              "QTableCornerButton::section {background-color: transparent;}")

        table.cellClicked.connect(self.markerClickSlot)

        table.setShowGrid(False)

        table.setColumnCount(6)
        table.setRowCount(0)

        table.horizontalHeader().hide()
        table.verticalHeader().hide()

        table.resize(350, 290)
        table.move(60, 30)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        table.setFocusPolicy(Qt.NoFocus)
        table.setEditTriggers(gui.QAbstractItemView.NoEditTriggers)

        self.osclegTableWidget.setEditTriggers(gui.QAbstractItemView.NoEditTriggers)
        self.osclegTableWidget.setSelectionMode(gui.QAbstractItemView.NoSelection)

        from PyQt5.QtGui import QFont
        font = QFont("times", 10)
        font.setBold(True)
        table.setFont(font)

        table.setColumnWidth(1, 50)

        table.setColumnWidth(3, 400)
        table.setColumnWidth(4, 10)


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

    def actionRun(self):
        self.mode = 'step'
        self.startClicked()

    def actionUpd(self):
        self.mode = 'check'
        self.startClicked()

    def actionStop_(self):
        self.stopClicked()

    def test(self):
        print(1)

    def generateLegendInit(self):
        table1 = self.speclegTableWidget
        table2 = self.osclegTableWidget
        tables = [table1, table2]

        for table in tables:

            table.verticalHeader().setVisible(False)
            table.setColumnCount(1)
            table.setHorizontalHeaderLabels(['Список каналов'])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table1.cellClicked.connect(self.tableSpecClick)
        table1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table1.setSelectionMode(QAbstractItemView.NoSelection)

        self.currChannel = None

    def tableSpecClick(self, row, col):
        table = self.speclegTableWidget

        for i in range(table.rowCount()):
            text = table.item(i, 0).text()
            text = text.replace(' (активный)', '')
            table.item(i, 0).setText(text)

        if not table.rowCount():
            return

        text = table.item(row, 0).text()
        text = text + ' (активный)'
        table.item(row, 0).setText(text)

        self.setActiveChanel(row)

    def generateLegend(self, chanN):
        from PyQt5.QtGui import QColor

        table1 = self.speclegTableWidget
        table2 = self.osclegTableWidget
        tables = [table1, table2]

        colors = self.specWid.colorsByInd

        for table in tables:
            table.setRowCount(chanN)

            for i in range(chanN):
                item = QTableWidgetItem()
                item.setText('Канал №' + str(i))

                qcolor = QColor()
                qcolor.setRgb(colors[i][0],  colors[i][1], \
                              colors[i][2])

                item.setBackground(qcolor)

                table.setItem(i, 0, item)

    def setActiveChanel(self, chanN):
        self.chanN = chanN
        self.specWid.setCurrChan(chanN)

    def clearActiveChan(self):
        self.chanN = None


    def specCntPushButtonClicked(self):
        self.oscWid.setOscLen(self.SPEC_cntSpinBox.value())

    def drawOscCheckBoxToggl(self):
        self.handler.setOscEn(self.drawOscCheckBox.isChecked())

    def __init__(self):
        super(MW, self).__init__()
        self.setupUi(self)

        from MeasClass import MeasClass
        self.measWid = MeasClass()

        self.initUI()





        # newmark__
        self.specWid.add_marker_sig.connect(self.addMarkerClickSlot)
        self.specWid.update_marker_sig.connect(self.updateValsSlot)
        self.del_marker_sig.connect(self.specWid.delMarkerSlot)
        self.markerPeakPushButton.clicked.connect(self.specWid.addMarkerPeak)
        # ----

        self.specWid.error_sig.connect(self.showError)

        self.clearSpecPushButton.clicked.connect(self.speclegTableWidgetClear)

        self.drawOscCheckBox.setChecked(False)

        self.initMenu()
        self.initNewMark()
        self.clearActiveChan()

        self.initUpdReaderOnWork()

        self.setOnWork(False)

        self.drawOscCheckBox.toggled.connect(self.drawOscCheckBoxToggl)

        # -------

        self.specWid.list_mark_sig.connect(self.measWid.updateMarks) # cnt
        self.specWid.mark_all_sig.connect(self.measWid.updMarkVals) # vals


        self.measWid.mark_width_sig.connect(self.specWid.setMarkerWidth)
        self.measWid.error_sig.connect(self.showError)

        self.hide()

        self.startWid = StartFrom(self)
        self.startWid.HIDE_SIG.connect(self.hideSlot)
        self.startWid.SHOW_SIG.connect(self.showSlot)

        self.startWid.START_RD_SIG.connect(self.actionRun)
        self.startWid.START_UPD_SIG.connect(self.actionUpd)
        self.startWid.STOP_SIG.connect(self.actionStop_)

        self.startWid.EXIT_SIG.connect(self.exitSlot)

        self.startWid.show()

        self.cntPushButton.clicked.connect(self.updReaderOnWork_cnt)
        self.specCntPushButton.clicked.connect(self.specCntPushButtonClicked)

        self.readConf()

        self.genPow2()


        self.pow2ComboBox.currentIndexChanged.connect(self.pow2Changed)

        #self.measTool.setEnabled(False)

    def genPow2(self):
        for i in range(10, 21):
            val = 2 ** i
            self.pow2ComboBox.addItem(str(val))

    def pow2Changed(self):
        val = self.pow2ComboBox.currentText()
        self.RD_cntSpinBox.setValue(int(val))

    def showSlot(self):
        self.showMaximized()

    def hideSlot(self):
        self.hide()

    def initUI(self):
        self.setUiDefault()
        self.fixUi()
        self.initSelectUi()
        self.initLayout()
        self.initSub()
        self.initSignals()
        self.generateLegendInit()

    def showInfo(self):
        from InfoWid import InfoWid
        self.info = InfoWid()
        self.info.show()



    def initSignals(self):
        self.clearOscPushButton.clicked.connect(self.oscWid.clear)
        self.clearSpecPushButton.clicked.connect(self.specWid.clear)
        self.info0PushButton.clicked.connect(self.showInfo)
        self.info1PushButton.clicked.connect(self.showInfo)



    def startSlot(self):
        self.setOnWork(True)





    def stopSlot(self):
        self.setOnWork(False)
        self.timer.stop()




    def setOnWork(self, state):
        self.onWork = state
        self.btnRun.setEnabled(not state)
        self.btnUpd.setEnabled(not state)
        self.btnStop.setEnabled(state)

    def clearLog(self):
        self.logTextBrowser.setText('')

    def log(self, newText):

        return

        txt = self.logTextBrowser.toPlainText()
        if txt == '':
            self.logTextBrowser.setText(newText)
        else:
            self.logTextBrowser.setText(txt + '\n' + newText)

    def midChanged(self):
        self.handler.setMidCnt(int(self.midSpinBox.value()))

    def initSub(self):

        self.midSpinBox.valueChanged.connect(self.midChanged)

        self.rdr = DataReader()
        self.handler = DataHandler()
        self.timer = QTimer()

        self.rdr.data_signal.connect(self.handler.dataInSlot)
        self.handler.fft_signal.connect(self.specWid.dataIn)
        self.handler.osc_signal.connect(self.oscWid.dataIn)

        self.rdr.error_signal.connect(self.showError)

        self.specWid.data_first_sig.connect(self.setChanDef)

        self.exit_sig.connect(self.rdr.exitSlot)
        self.exit_sig.connect(self.handler.exitSlot)

        self.timer.timeout.connect(self.rdr.timerSlot)

        self.rdr.log_signal.connect(self.log)
        self.handler.log_signal.connect(self.log)


        self.handler.data_in_sig.connect(self.rdr.dataHandledSlot)

        self.start_sig.connect(self.startSlot)
        self.stop_signal.connect(self.stopSlot)



        # стоп сигнал от окна к ридеру
        self.stop_signal.connect(self.rdr.stopSlot)
        # стоп сигнал от ридера к хендлеру
        self.rdr.stop_signal.connect(self.handler.stopSlot)

        # стоп от хэндлера к окну
        self.handler.stop_signal.connect(self.stopSlot)

        self.clear_mid_sig.connect(self.handler.clearMidSlot)

        self.clearSpecPushButton.clicked.connect(self.clearAllMark)



        self.rdrTh = QThread()
        self.handlerTh = QThread()

        # запуск от окна к ридеру
        self.start_sig.connect(self.rdr.setStartFlg)
        # запуск от ридера к хендлеру
        self.rdr.start_signal.connect(self.handler.setStartFlg)



        self.rdr.moveToThread(self.rdrTh)
        self.handler.moveToThread(self.handlerTh)


        # запуск потоков - запуск ридера/хендлера
        self.handlerTh.started.connect(self.handler.run)
        self.rdrTh.started.connect(self.rdr.run)
        self.handlerTh.start()
        self.rdrTh.start()






        # --- timer




    def initLayout(self):
        self.setCentralWidget(self.tabWidget)


        self._lt0 = QVBoxLayout()
        self._lt0.addWidget(self.specWid)
        self._lt0.addWidget(self.measWid)

        self.lt0 = QHBoxLayout()
        self.lt0.addLayout(self._lt0)

        self.lt0.addWidget(self.controlSpecGroupBox)
        self.tabFFT.setLayout(self.lt0)

        self.lt1 = QHBoxLayout()
        self.lt1.addWidget(self.oscWid)
        self.lt1.addWidget(self.controlOscGroupBox)
        self.tabOsc.setLayout(self.lt1)



    def showError(self, text0):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text0)
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def fixUi(self):

       pass




    def setUiDefault(self):
        self.drawOscCheckBox.setChecked(True)

        self.actionStart.setEnabled(True)
        self.actionStop.setEnabled(False)

        self.tabWidget.setCurrentIndex(0)

    def initSelectUi(self):
        self.actionStart.triggered.connect(self.startClicked)
        self.actionStop.triggered.connect(self.stopClicked)



    def RD_changed(self):
        if 0:
            self.rdTabWidget.setCurrentIndex(0)
            self.meanCheckBox.setEnabled(False)
            self.specClearMidPushButton.setEnabled(False)
        elif self.READ_stepRadioButton.isChecked():
            self.rdTabWidget.setCurrentIndex(1)
            self.meanCheckBox.setEnabled(True)
            self.specClearMidPushButton.setEnabled(True)
        elif self.RD_changeRadioButton.isChecked():
            self.rdTabWidget.setCurrentIndex(2)
            self.meanCheckBox.setEnabled(True)
            self.specClearMidPushButton.setEnabled(True)
        elif self.RD_timerRadioButton.isChecked():
            self.rdTabWidget.setCurrentIndex(3)
            self.meanCheckBox.setEnabled(True)
            self.specClearMidPushButton.setEnabled(True)


    def FOR_changed(self):
        if self.FOR_binRadioButton.isChecked():
            self.formTabWidget.setCurrentIndex(0)
        elif self.FOR_textRadioButton.isChecked():
            self.formTabWidget.setCurrentIndex(1)

    def SRC_changed(self):
        if self.SRC_onefileRadioButton.isChecked():
            self.SRC_tabWidget.setCurrentIndex(0)

        elif self.SRC_onefilechanRadioButton.isChecked():
            self.SRC_tabWidget.setCurrentIndex(1)


        elif self.SRC_filesRadioButton.isChecked():
            self.SRC_tabWidget.setCurrentIndex(2)

        elif self.SRC_sharedRadioButton.isChecked():
            self.SRC_tabWidget.setCurrentIndex(3)




    # ----------

    def setChanDef(self):
        self.tableSpecClick(0,0)


    def startClicked(self):
        self.parseParams()
        self.specWid.clearStart()
        self.oscWid.clearStart()
        self.start_sig.emit()






    def stopClicked(self):
        self.stop_signal.emit()

    def readParams(self):
        pass

    def saveClicked(self):

        f = open('cnf.cfg' ,'w')

        cnt = self.RD_cntSpinBox.text()
        f.write(cnt + '\n')

        if self.SRC_onefileRadioButton.isChecked():
            f.write('0\n')
        #elif self.SRC_filesRadioButton.isChecked():


        f.close()


    def speclegTableWidgetClear(self):

        if self.onWork:
            return

        table = self.speclegTableWidget

        while table.rowCount():
            table.removeRow(0)




    def SRC_chanNcomboBoxChange(self):
        table = self.SRC_chanTableWidget
        cnt = int(self.SRC_chanNcomboBox.currentText())
        table.setRowCount(cnt)



        for i in range(cnt):
            item = QTableWidgetItem()
            item.setText(str(i))
            item.setFlags(item.flags() & ~ PyQt5.QtCore.Qt.ItemIsEditable)
            table.setItem(i, 0, item)


            table.setItem(i, 1, QTableWidgetItem(''))

            item = QTableWidgetItem()
            item.setIcon(QIcon('icon/file.png'))
            item.setFlags(item.flags() & ~ PyQt5.QtCore.Qt.ItemIsEditable)
            table.setItem(i, 2, item)

    # ----------


    def parseParams(self):

        # --- как идут каналы

        if self.startWid.SRC_onefileRadioButton.isChecked():
            self.specWid.setChanN(1)
            self.oscWid.setChanN(1)
            self.measWid.setChan(1)
            self.generateLegend(1)
            chanN = 1
            files = [self.startWid.SRC_onefileSelectLineEdit.text()]
        elif self.startWid.SRC_onefilechanRadioButton.isChecked():
            pass
        elif self.startWid.SRC_filesRadioButton.isChecked():
            table = self.startWid.SRC_chanTableWidget
            chanN = int(self.startWid.SRC_chanNcomboBox.currentText())
            files = []
            for i in range(chanN):
                val = table.item(i, 1).text()
                files.append(val)

            self.specWid.setChanN(chanN)
            self.oscWid.setChanN(chanN)
            self.measWid.setChan(chanN)
            self.generateLegend(chanN)

        self._chanN = chanN
        self.measWid.setChan(chanN)
        self.rdr.setChanN(chanN)
        self.rdr.setFiles(files)

        # ----- комплексные ли

        isCompl = self.startWid.FOR_bincomplexCheckBox.isChecked()

        self.rdr.setIsCompl(isCompl)


        # ---- формат данных
        params = {}
        params['end'] = self.startWid.FOR_binendianComboBox.currentText()
        params['sign'] = self.startWid.FOR_binsignComboBox.currentText()
        params['ln'] = int(self.startWid.FOR_binsizeComboBox.currentText())

        self.rdr.setDataFromat(params)

        # --- режим чтения


        if self.mode == 'step':
            self.tim = 500
            self.rdr.setPauseStep(self.tim)

        self.rdr.setMode(self.mode)

        maxPnt = int(self.startWid.RD_cntSpinBox.text())
        self.rdr.setMaxPnt(maxPnt)
        self.handler.setFftEn(True)
        self.handler.setOscEn(self.drawOscCheckBox.isChecked())

        self.handlerUpdateParams()



    def setThePeak(self):
        val = float(self.peak_lineEdit.text())

        sz = self.peak_ComboBox.currentText()

        if sz == 'kHz':
            val = val * 1000
        elif sz == 'mHz':
            val = val * 1000000



    def initUpdReaderOnWork(self):
        self.complSpecCheckBox.toggled.connect(self.updReaderOnWork_isCompl)
        self.specWinComboBox.currentIndexChanged.connect(self.updReaderOnWork_win)

        # --

    def meanCheckBoxChanged(self):
        if self.meanCheckBox.isChecked():
            self.specClearMidPushButton.setEnabled(True)
        else:
            self.specClearMidPushButton.setEnabled(False)

    def updReaderOnWork_mid(self):
        self.handlerUpdateParams()
        self.clear_mid_sig.emit()

    def updReaderOnWork_cnt(self):
        maxPnt = int(self.RD_cntSpinBox.text())
        self.rdr.setMaxPnt(maxPnt)
        self.clear_mid_sig.emit()

    def updReaderOnWork_win(self):
        self.handlerUpdateParams()
        self.clear_mid_sig.emit()

    def updReaderOnWork_isCompl(self):
        self.handlerUpdateParams()
        self.clear_mid_sig.emit()


    def handlerUpdateParams(self):

        fs = int(self.startWid.fsLineEdit.text())

        if self.startWid.fsComboBox.currentText() == 'kHz':
            fs = fs * 1000
        elif self.startWid.fsComboBox.currentText() == 'MHz':
            fs = fs * 1000000



        ref = (2 ** int(self.startWid.FOR_binsizeComboBox.currentText())) / 2



        # yes
        win = self.specWinComboBox.currentText()
        isComplFFT = self.complSpecCheckBox.isChecked()
        chanN = self._chanN # cnt


        self.handler.setParams(chanN, fs, ref, isComplFFT, False)
        self.handler.setWindow(win)




    def sleep(self, val):
        from PyQt5.QtCore import QThread
        val = val * 100
        val = int(val)
        QThread.msleep(val)


    def exitSlot(self):
        t = 0.2
        self.stop_signal.emit()
        self.sleep(t)
        self.exit_sig.emit()
        self.sleep(t)
        self.rdrTh.quit()
        self.handlerTh.quit()
        self.rdrTh.wait()
        self.handlerTh.wait()
        self.startWid.close()

        self.saveConf()


    def closeEvent(self, event):
        event.ignore()
        self.stopClicked()
        self.hide()
        self.startWid.show()






