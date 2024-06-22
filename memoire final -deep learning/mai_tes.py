from lanc import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
import sys

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    lanc = Main()
    exit(app.exec_())
app = QApplication(sys.argv)
Lanc = Main()
exit(app.exec_())
