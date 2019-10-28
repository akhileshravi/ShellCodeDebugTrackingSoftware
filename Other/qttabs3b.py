import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QSizePolicy,
                         QDoubleSpinBox, QLabel, QCheckBox, QMainWindow,
QGridLayout)
from PyQt5.QtCore import QCoreApplication
import matplotlib
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # Geometry of main window:
        self.setGeometry(200, 200, 1000, 1000)
        self.setWindowTitle('Simulation')

        #---------------------------------------
                # Button for adding blades
        blade_button = QPushButton('Add', self)
        blade_button.clicked.connect(self.add_Bladebox)
        blade_button.move(800, 600)


        #---------------------------------------

        self.show()

    # Method for input box:
    def inputBox(self, left, top, maxvalue, step, default,decimals):
        box = QDoubleSpinBox(self)
        box.move(left,top)
        box.setDecimals(decimals)
        box.setMaximum(maxvalue)
        box.setSingleStep(step)
        box.setProperty("value", default)
        box.resize(box.sizeHint())
        box.show()

    # Method for adding blade boxes
    def add_Bladebox(self):

        print('This is Ok')

        left = 900
        top = 500
        maxvalue = 3
        step = 1
        default = 0
        decimals = 1
        self.inputBox(left, top, maxvalue, step, default, decimals)


if __name__ == '__main__':

    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())