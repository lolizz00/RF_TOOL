# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\RF_TOOL\RF_TOOL-master\ui\meas.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MeasWid(object):
    def setupUi(self, MeasWid):
        MeasWid.setObjectName("MeasWid")
        MeasWid.resize(814, 150)
        MeasWid.setMinimumSize(QtCore.QSize(0, 0))
        MeasWid.setMaximumSize(QtCore.QSize(16777215, 150))
        self.tabWidget = QtWidgets.QTabWidget(MeasWid)
        self.tabWidget.setGeometry(QtCore.QRect(0, -10, 811, 161))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 221, 121))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.closePushButton = QtWidgets.QPushButton(self.tab)
        self.closePushButton.setGeometry(QtCore.QRect(760, 20, 40, 40))
        self.closePushButton.setMinimumSize(QtCore.QSize(40, 40))
        self.closePushButton.setMaximumSize(QtCore.QSize(40, 40))
        self.closePushButton.setText("")
        self.closePushButton.setObjectName("closePushButton")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(510, 10, 241, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mark1ComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.mark1ComboBox.setObjectName("mark1ComboBox")
        self.gridLayout.addWidget(self.mark1ComboBox, 0, 1, 1, 2)
        self.mark2ComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.mark2ComboBox.setObjectName("mark2ComboBox")
        self.gridLayout.addWidget(self.mark2ComboBox, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.SNR_updPushButton = QtWidgets.QPushButton(self.tab)
        self.SNR_updPushButton.setGeometry(QtCore.QRect(560, 90, 121, 31))
        self.SNR_updPushButton.setObjectName("SNR_updPushButton")
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setGeometry(QtCore.QRect(240, 10, 258, 121))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.markTableWidget = QtWidgets.QTableWidget(self.widget)
        self.markTableWidget.setObjectName("markTableWidget")
        self.markTableWidget.setColumnCount(0)
        self.markTableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.markTableWidget)
        self.tabWidget.addTab(self.tab, "")

        self.retranslateUi(MeasWid)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MeasWid)

    def retranslateUi(self, MeasWid):
        _translate = QtCore.QCoreApplication.translate
        MeasWid.setWindowTitle(_translate("MeasWid", "Справка"))
        self.label.setText(_translate("MeasWid", "<html><head/><body><p><span style=\" font-weight:600;\">Маркер 1:</span></p></body></html>"))
        self.label_2.setText(_translate("MeasWid", "<html><head/><body><p><span style=\" font-weight:600;\">Маркер 2:</span></p></body></html>"))
        self.SNR_updPushButton.setText(_translate("MeasWid", "Добавить разницу"))
        self.label_3.setText(_translate("MeasWid", "Доступные маркеры"))


