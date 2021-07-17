from PyQt5.QtWidgets import QWidget, QVBoxLayout
from infouiMe import  Ui_InfoMe
from PyQt5.QtGui import  QIcon
from PyQt5 import QtCore
class InfoMe(QWidget,  Ui_InfoMe):
    def __init__(self, parent=None):
        super(InfoMe, self).__init__(parent)
        self.setupUi(self)
        self.ic = QIcon(("icon/lama.png"))
        self.logo.setIcon(self.ic)
        self.logo.setIconSize(QtCore.QSize(90,90))

        t = "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">"
        t = t + 'RF_TOOL  v1.0'
        t = t + "</span></p></body></html>"

        self.label.setText(t)