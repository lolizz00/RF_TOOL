from startformui import  Ui_startform
from PyQt5 import QtCore, QtGui, QtWidgets


from PyQt5.QtCore import QThread, QTimer,pyqtSignal

from PyQt5.QtGui import  *
from PyQt5.QtWidgets import *
import PyQt5

DEBUG = True


class StartFrom(QWidget, Ui_startform):

    SHOW_SIG  = pyqtSignal()
    HIDE_SIG = pyqtSignal()

    START_UPD_SIG = pyqtSignal()
    START_RD_SIG = pyqtSignal()
    STOP_SIG = pyqtSignal()

    EXIT_SIG = pyqtSignal()

    def startRdPushButtonClicked(self):
        self.hide()
        self.SHOW_SIG.emit()
        self.START_RD_SIG.emit()

    def startUpdPushButtonClicked(self):
        self.hide()
        self.SHOW_SIG.emit()
        self.START_UPD_SIG.emit()

    def ltConf(self):
        self.setLayout(self.mainGridLayout)
        self.SRC_groupBox.setLayout(self.gridLayout_4)
        self.FOR_groupBox.setLayout(self.gridLayout_5)
        self.groupBox.setLayout(self.horizontalLayout_2)


    def __init__(self, parent=None):
        super(StartFrom, self).__init__()
        self.setupUi(self)
        self.preinitUi()

        self.startRdPushButton.clicked.connect(self.startRdPushButtonClicked)
        self.startUpdPushButton.clicked.connect(self.startUpdPushButtonClicked)


        self.setFixedHeight(620)
        self.setFixedWidth(550)


    def genToolTipStyle(self, ptr):
        ptr.setStyleSheet("QToolTip { \
    font-size:9pt; \
    color:white; padding:2px; \
    border-width:2px;\
    border-style:solid;\
    border-radius:20px;\
    background-color: black;\
    border: 1px solid white;}")


    def closeEvent(self, QCloseEvent):
        self.EXIT_SIG.emit()
        QCloseEvent.accept()


    def genPow2(self):
        for i in range(10, 21):
            val = 2 ** i
            self.pow2ComboBox.addItem(str(val))

    def pow2Changed(self):
        val = self.pow2ComboBox.currentText()
        self.RD_cntSpinBox.setValue(int(val))

    def initMainButtons(self):

        self.startRdPushButton.setIcon( QIcon(("icon/n.png")))
        self.startRdPushButton.setIconSize(QtCore.QSize(45, 45))
        self.startRdPushButton.setFlat(True)
        self.genToolTipStyle(self.startRdPushButton)
        self.startRdPushButton.setToolTip('Считать последовательно')

        self.startUpdPushButton.setIcon( QIcon(("icon/r.png")))
        self.startUpdPushButton.setIconSize(QtCore.QSize(45, 45))
        self.startUpdPushButton.setFlat(True)
        self.genToolTipStyle(self.startUpdPushButton)
        self.startUpdPushButton.setToolTip('Считать при изменении')

    def preinitUi(self):
        self.setWindowTitle('RF Tool Config')
        self.initMainButtons()

        self.SRC_onefileRadioButton.setChecked(True)
        self.SRC_tabWidget.setCurrentIndex(0)

        self.SRC_tabWidget.tabBar().setEnabled(False)
        self.SRC_tabWidget.tabBar().hide()

        self.formTabWidget.tabBar().setEnabled(False)
        self.formTabWidget.tabBar().hide()

        self.SRC_onefileRadioButton.toggled.connect(self.SRC_changed)
        self.SRC_onefilechanRadioButton.toggled.connect(self.SRC_changed)
        self.SRC_filesRadioButton.toggled.connect(self.SRC_changed)



        self.SRC_groupBox.setStyleSheet('QTabWidget::pane { border: 0; }')
        self.FOR_groupBox.setStyleSheet('QTabWidget::pane { border: 0; }')


        self.SRC_onefileselectFilePushButton.clicked.connect(self.SRC_onefileselectFilePushButtonClicked)

        self.SRC_chanTableWidgetInit()

        icon = QIcon("icon/file.png")
        self.SRC_onefileselectFilePushButton.setIcon(icon)
        self.SRC_onefileselectFilePushButton.setText('')

        self.ltConf()

        self.genPow2()

        self.pow2ComboBox.currentIndexChanged.connect(self.pow2Changed)

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

    def SRC_chanTableWidgetInit(self):
        table = self.SRC_chanTableWidget
        table.verticalHeader().setVisible(False)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['№', 'Файл', ' '])
        table.cellClicked.connect(self.SRC_chanTableWidgetClick)
        self.SRC_chanNcomboBox.currentIndexChanged.connect(self.SRC_chanNcomboBoxChange)

        self.SRC_chanNcomboBoxChange()

    def SRC_chanTableWidgetClick(self, row, col):
        if col == 2:
            table = self.SRC_chanTableWidget
            fl = QFileDialog.getOpenFileName()[0]
            table.setItem(row, 1, QTableWidgetItem(fl))

    def SRC_onefileselectFilePushButtonClicked(self):
        fl = QFileDialog.getOpenFileName()[0]
        self.SRC_onefileSelectLineEdit.setText(fl)

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