from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtGui, QtCore

class DropLineEdit(QLineEdit):
    def __init__(self, obj):
        super(DropLineEdit, self).__init__(obj)

        self.setAcceptDrops(True)
        self.setMinimumHeight(30)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            t = event.mimeData().urls()[0].path()
            t = t[1:]
            self.setText(t)
            event.accept()

        else:
            event.ignore()

