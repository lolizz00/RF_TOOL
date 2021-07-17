# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\RF_TOOL\RF_TOOL-master\ui\marker.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_markerWid(object):
    def setupUi(self, markerWid):
        markerWid.setObjectName("markerWid")
        markerWid.resize(600, 600)
        markerWid.setMinimumSize(QtCore.QSize(600, 600))
        markerWid.setMaximumSize(QtCore.QSize(600, 600))
        self.label = QtWidgets.QLabel(markerWid)
        self.label.setGeometry(QtCore.QRect(80, 70, 301, 21))
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setObjectName("label")
        self.markerTableWidget = QtWidgets.QTableWidget(markerWid)
        self.markerTableWidget.setGeometry(QtCore.QRect(100, 110, 256, 192))
        self.markerTableWidget.setObjectName("markerTableWidget")
        self.markerTableWidget.setColumnCount(0)
        self.markerTableWidget.setRowCount(0)
        self.label2 = QtWidgets.QLabel(markerWid)
        self.label2.setGeometry(QtCore.QRect(30, 340, 550, 110))
        self.label2.setMinimumSize(QtCore.QSize(550, 110))
        self.label2.setMaximumSize(QtCore.QSize(550, 110))
        self.label2.setObjectName("label2")
        self.groupBox = QtWidgets.QGroupBox(markerWid)
        self.groupBox.setGeometry(QtCore.QRect(70, 460, 441, 70))
        self.groupBox.setMinimumSize(QtCore.QSize(0, 70))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 70))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 20, 423, 32))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addPushButton = QtWidgets.QPushButton(self.widget)
        self.addPushButton.setMinimumSize(QtCore.QSize(0, 30))
        self.addPushButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.addPushButton.setStyleSheet("QPushButton\n"
" {\n"
"font-size:10pt;\n"
"font-weight:600;\n"
"}")
        self.addPushButton.setObjectName("addPushButton")
        self.horizontalLayout.addWidget(self.addPushButton)
        self.chanLabel = QtWidgets.QLabel(self.widget)
        self.chanLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.chanLabel.setMaximumSize(QtCore.QSize(16777215, 200))
        self.chanLabel.setObjectName("chanLabel")
        self.horizontalLayout.addWidget(self.chanLabel)

        self.retranslateUi(markerWid)
        QtCore.QMetaObject.connectSlotsByName(markerWid)

    def retranslateUi(self, markerWid):
        _translate = QtCore.QCoreApplication.translate
        markerWid.setWindowTitle(_translate("markerWid", "Управление маркерами"))
        self.label.setText(_translate("markerWid", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">УПРАВЛЕНИЕ МАРКЕРАМИ</span></p></body></html>"))
        self.label2.setText(_translate("markerWid", "<html><head/><body><p><span style=\" font-size:10pt;\">Канал для установки маркера (активный) выбирается в таблице справа от графика.<br/><br/>Для добавления маркера автоматически на пик нажмите &quot;Добавить маркер на пик&quot;.</span></p><p><span style=\" font-size:10pt;\">Для добавления маркера вручную, двойное нажатие ЛКМ в нужной точке графика.</span></p></body></html>"))
        self.addPushButton.setText(_translate("markerWid", "Добавить маркер на пик"))
        self.chanLabel.setText(_translate("markerWid", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Активный канал: -</span></p></body></html>"))


