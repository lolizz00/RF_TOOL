from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpinBox
from measui import  Ui_MeasWid
from PyQt5.QtGui import  QIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, \
    QHeaderView,QAbstractItemView, QMessageBox, QTableWidgetItem

class MeasClass(QWidget,  Ui_MeasWid):

    mark_width_sig = pyqtSignal(int, int)

    error_sig = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MeasClass, self).__init__(parent)
        self.setupUi(self)

        self.closePushButton.clicked.connect(self.closeClick)
        self.closePushButton.setIcon(QIcon("icon/c.png"))
        self.closePushButton.setIconSize(QtCore.QSize(35, 35))

        self.lt = QVBoxLayout()
        self.lt.addWidget(self.tabWidget)

        self.DELTA_mark1 = -1
        self.DELTA_mark2 = -1

        self.initTable()

        self.SNR_updPushButton.clicked.connect(self.SNR_setParams)

    def closeClick(self):
        self.setMinimumSize(0, 0)
        self.setMaximumSize(1e5,0)

    def changeWidthMark(self, val, name):
        n = int(name.replace('widthSpin_', ''))
        self.mark_width_sig.emit(n, val)

    def SNR_setParams(self):


        mark1 = self.mark1ComboBox.currentText()
        mark2 = self.mark2ComboBox.currentText()




        if mark1 == '' or mark2 == '':
            self.error_sig.emit('Не выбран маркер!')
            return
        if mark1 == mark2:
            self.error_sig.emit('Выберите разные маркеры!')
            return

        table = self.tableWidget
        newID = table.rowCount()
        table.setRowCount(newID + 1)
        table.setItem(newID, 0, QTableWidgetItem('M' + str(mark1)))
        table.setItem(newID, 1, QTableWidgetItem('M' + str(mark2)))
        table.setItem(newID, 2, QTableWidgetItem(''))
        item = QTableWidgetItem()
        item.setIcon(QIcon('icon/delete.png'))
        table.setItem(newID, 3, item)

    def remDelta(self,row, col):
        if col == 3:
            table = self.tableWidget
            table.removeRow(row)

    def initTable(self):
        self.tabWidget.tabBar().setEnabled(False)
        self.tabWidget.tabBar().hide()
        self.setStyleSheet('QTabWidget::pane { border: 0; }')

        table = self.tableWidget
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['', '', 'Разница', ''])
        table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.verticalHeader().hide()
        table.cellClicked.connect(self.remDelta)

        table = self.markTableWidget
        table.setRowCount(0)
        table.setColumnCount(2)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.setHorizontalHeaderLabels(['Маркер', 'Ширина'])
        table.verticalHeader().hide()

    def setChan(self, n):
        table = self.tableWidget

    def calcDelta(self, marks):



        table = self.tableWidget

        for i in range(table.rowCount()):
            m1 = int(table.item(i, 0).text().replace('M', ''))
            m2 = int(table.item(i, 1).text().replace('M', ''))

            m1 = marks[m1][1]
            m2 = marks[m2][1]


            val = m1 - m2
            val = round(val)

            table.item(i, 2).setText(str(val))





    # !!!
    def updMarkVals(self, marks):
        _marks = marks.keys()
        table = self.tableWidget

        for i in range(table.rowCount()):
            try:
                m = int(table.item(i, 0).text().replace('M', ''))
                if not m in _marks:
                    table.removeRow(i)
                    continue

                m = int(table.item(i, 1).text().replace('M', ''))
                if not m in _marks:
                    table.removeRow(i)
            except Exception as e:
                pass
                print(e)


        self.calcDelta(marks)






    def updMarkList(self, marks):


        table = self.markTableWidget

        c_marks = []

        for i in range(table.rowCount()):
            mark = table.item(i, 0).text()
            mark = int(mark.replace("M", ''))
            c_marks.append(mark)


        # добавляем
        for mark in marks:
            if not mark in c_marks:
                newID = table.rowCount()
                table.setRowCount(newID + 1)

                item = QTableWidgetItem("M" + str(mark))
                table.setItem(newID, 0, item)

                rng = QSpinBox()
                rng.setMinimum(1)
                rng.setSingleStep(100)
                rng.setMaximum(5000)

                rng.setObjectName('widthSpin_' + str(mark))

                rng.valueChanged.connect(lambda val, name=rng.objectName(): self.changeWidthMark(val, name))

                table.setCellWidget(newID, 1, rng)

        # удаляем ненужные
        rem = []
        for i in range(table.rowCount()):
            _mrk =  table.item(i, 0).text()
            _mrk  = int( _mrk .replace("M", ''))

            if not _mrk in marks:
                rem.append(_mrk)
        for del_mrk in rem:
            for i in range(table.rowCount()):
                _mrk = table.item(i, 0).text()
                _mrk = int(_mrk.replace("M", ''))

                if _mrk in rem:
                    table.removeRow(i)
                    break

    def updateBoxes(self, marks):

        _m = [int(_t) for _t in marks]
        self.updMarkList(_m)

        newm = [str(_t) for _t in marks]



        cmb = [self.mark1ComboBox, self.mark2ComboBox]
        for _cmb in cmb:
            all = [_cmb.itemText(i) for i in range(_cmb.count())]

            # если такого нет добавляем
            for t in newm:
                if not t in all:
                    _cmb.addItem(t)

            # если уже нет удаляем:
            for t in all:
                if not t in newm:
                    for i in range(_cmb.count()):
                        if _cmb.itemText(i) == t:
                            _cmb.removeItem(i)
                            break

    def updateMarks(self, marks):
        self.updateBoxes(marks)








