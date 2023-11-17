import logging
import sys
from PySide6 import QtWidgets

from interfaces.mainwindow import MainWindow

# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())