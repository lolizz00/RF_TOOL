def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))


    print('\n\n-------------------------------------------- \n')
    print(text)
    print('\n----------------------------------------------\n')

import ctypes, sys



def win():
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon
    from PyQt5 import QtCore
    from MW import MW
    import os

    sys.excepthook = log_uncaught_exceptions

    import pyqtgraph as pg
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    pg.setConfigOption('antialias', False)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)


    app = QApplication(sys.argv)

    import ctypes
    myappid = 'null.rftool.null.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app_icon = QIcon()
    app_icon.addFile('icon/win/lama-16x16.png', QtCore.QSize(16, 16))
    app_icon.addFile('icon/win/lama-24x24.png', QtCore.QSize(24, 24))
    app_icon.addFile('icon/win/lama-32x32.png', QtCore.QSize(32, 32))
    app_icon.addFile('icon/win/lama-48x48.png', QtCore.QSize(48, 48))
    app_icon.addFile('icon/win/lama-256x256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    mv = MW()
    mv.hide()
    sys.exit(app.exec_())




win()


