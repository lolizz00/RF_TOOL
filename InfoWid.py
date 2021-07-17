from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QHeaderView,QAbstractItemView, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QThread, QTimer,pyqtSignal
from PyQt5.QtGui import  QIcon


from infoui import Ui_InfoWid


class InfoWid(QWidget, Ui_InfoWid):
    def __init__(self):
        super(InfoWid, self).__init__()
        self.setupUi(self)

