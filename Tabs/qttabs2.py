from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QGroupBox, QHBoxLayout
import sys, os


class Dialog_01(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()

        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QVBoxLayout()
        mainWidget.setLayout(mainLayout)

        self.tabWidget = QTabWidget()
        mainLayout.addWidget(self.tabWidget)

        # self.tabWidget.connect(self.tabWidget, QWidget.SIGNAL("currentChanged(int)"), self.tabSelected)
        self.tabWidget.currentChanged.connect(self.whatTab)
        # Reference: https://stackoverflow.com/questions/21562485/pyqt-qtabwidget-currentchanged

        myBoxLayout = QVBoxLayout()
        self.tabWidget.setLayout(myBoxLayout)

        self.readme = 'ReadMe'
        self.texteditor = 'TextEditor'
        self.terminal = 'Terminal'
        self.tabs = {}

        readme = QWidget()
        readme_layout = QVBoxLayout()
        readme.setLayout(readme_layout)

        label1 = QtWidgets.QLabel()
        label1.setText("Sample Label \n Hi there! Keep up the good work!")
        label1.setAlignment(Qt.AlignLeft)
        readme_layout.addWidget(label1)
        # Reference : https://www.tutorialspoint.com/pyqt/pyqt_qlabel_widget.htm


        # self.tabs[self.readme] = QWidget()
        self.tabs[self.readme] = readme
        self.tabs[self.texteditor] = QWidget()
        self.tabs[self.terminal] = QWidget()

        self.tabWidget.addTab(self.tabs[self.readme],self.readme)
        self.tabWidget.addTab(self.tabs[self.texteditor],self.texteditor)
        self.tabWidget.addTab(self.tabs[self.terminal],self.terminal)




        ButtonBox = QGroupBox()
        ButtonsLayout = QHBoxLayout()
        ButtonBox.setLayout(ButtonsLayout)

        Button_01 = QPushButton("What Tab?")
        ButtonsLayout.addWidget(Button_01)
        Button_01.clicked.connect(self.whatTab)

        mainLayout.addWidget(ButtonBox)


    def tabSelected(self, arg=None):
        print ('\n\t tabSelected() current Tab index =', arg)

    def whatTab(self):
        currentIndex = self.tabWidget.currentIndex()
        currentWidget = self.tabWidget.currentWidget()

        print ('\n\t Query: current Tab index =', currentIndex)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())