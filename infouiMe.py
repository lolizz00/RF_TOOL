# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\RF_TOOL\RF_TOOL-master\ui\infoyMe.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InfoMe(object):
    def setupUi(self, InfoMe):
        InfoMe.setObjectName("InfoMe")
        InfoMe.resize(500, 150)
        InfoMe.setMinimumSize(QtCore.QSize(500, 150))
        InfoMe.setMaximumSize(QtCore.QSize(500, 150))
        self.widget = QtWidgets.QWidget(InfoMe)
        self.widget.setGeometry(QtCore.QRect(70, 20, 351, 102))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logo = QtWidgets.QPushButton(self.widget)
        self.logo.setMinimumSize(QtCore.QSize(100, 100))
        self.logo.setMaximumSize(QtCore.QSize(100, 100))
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.horizontalLayout.addWidget(self.logo)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(InfoMe)
        QtCore.QMetaObject.connectSlotsByName(InfoMe)

    def retranslateUi(self, InfoMe):
        _translate = QtCore.QCoreApplication.translate
        InfoMe.setWindowTitle(_translate("InfoMe", "About"))
        self.label.setText(_translate("InfoMe", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">TextLabel</span></p></body></html>"))


