from PyQt5.QtWidgets import QTableWidget
from PyQt5 import QtGui, QtCore

class DropTableWidget(QTableWidget):
    def __init__(self, obj):
        super(DropTableWidget, self).__init__(obj)

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

            schRow = 0

            for data in event.mimeData().urls():
                txt = data.path()[1:]

                item = self.item(schRow, 1)

                if item == None:
                    break

                item.setText(txt)

                schRow = schRow + 1

            event.accept()

        else:
            event.ignore()

