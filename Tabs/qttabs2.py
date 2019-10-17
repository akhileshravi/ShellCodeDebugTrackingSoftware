from PyQt5 import QtGui, QtCore
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

        # self.tabWidget.tabBarClicked.connect(self.tabWidget, QWidget.SIGNAL("currentChanged(int)"), self.tabSelected)
        # self.tabWidget.emit(self.tabWidget, QWidget.SIGNAL("currentChanged(int)"), self.tabSelected)
        # self.tabWidget.tabBarClicked(self.whatTab)
        # self.tabBarClicked(self.whatTab)
        self.tabWidget.currentChanged.connect(self.whatTab)

        myBoxLayout = QVBoxLayout()
        self.tabWidget.setLayout(myBoxLayout)

        self.tabWidget.addTab(QWidget(),'Tab_01')
        self.tabWidget.addTab(QWidget(),'Tab_02')
        self.tabWidget.addTab(QWidget(),'Tab_03')


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