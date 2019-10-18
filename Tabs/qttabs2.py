from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
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
        self.codeeditor = 'Code Editor'
        self.terminal = 'Terminal' #TODO: Execute button has to be added to this tab
        self.tabs = {}

        readme = QWidget()
        readme_layout = QVBoxLayout()
        readme.setLayout(readme_layout)

        self.label1 = QtWidgets.QLabel()
        with open('ReadMe1.txt', 'r') as f:
            text = f.read()
        self.label1.setText(text)
        self.label1.setAlignment(Qt.AlignLeft)
        readme_layout.addWidget(self.label1)
        # Reference : https://www.tutorialspoint.com/pyqt/pyqt_qlabel_widget.htm

        codeeditor = QWidget()
        codeeditor_layout = QVBoxLayout()
        codeeditor.setLayout(codeeditor_layout)

        self.textbox = QTextEdit(self)
        self.textbox.setText()
        # self.textbox.move(20, 20)
        # self.textbox.resize(280,200)
        codeeditor_layout.addWidget(self.textbox)


        # self.tabs[self.readme] = QWidget()
        self.tabs[self.readme] = readme
        self.tabs[self.codeeditor] = codeeditor
        self.tabs[self.terminal] = QWidget()

        self.tabWidget.addTab(self.tabs[self.readme],self.readme)
        self.tabWidget.addTab(self.tabs[self.codeeditor], self.codeeditor)
        self.tabWidget.addTab(self.tabs[self.terminal],self.terminal)


        ButtonBox = QGroupBox()
        ButtonsLayout = QHBoxLayout()
        ButtonBox.setLayout(ButtonsLayout)

        # Button_01 = QPushButton("What Tab?")
        # ButtonsLayout.addWidget(Button_01)
        # Button_01.clicked.connect(self.whatTab)

        mainLayout.addWidget(ButtonBox)

        Task_1 = QPushButton("Task 1")
        ButtonsLayout.addWidget(Task_1)
        Task_1.clicked.connect(self.Task_1_Click)

        Task_2 = QPushButton("Task 2")
        ButtonsLayout.addWidget(Task_2)
        Task_2.clicked.connect(self.Task_2_Click)

        Task_3 = QPushButton("Task 3")
        ButtonsLayout.addWidget(Task_3)
        Task_3.clicked.connect(self.Task_3_Click)

        Task_4 = QPushButton("Task 4")
        ButtonsLayout.addWidget(Task_4)
        Task_4.clicked.connect(self.Task_4_Click)

    def tabSelected(self, arg=None):
        print ('\n\t tabSelected() current Tab index =', arg)

    def whatTab(self):
        #TODO: Have a different on-click for each tab.
        #TODO: Add timer to tab change
        currentIndex = self.tabWidget.currentIndex()
        # currentWidget = self.tabWidget.currentWidget()

        print ('\n\t Query: current Tab index =', currentIndex)

    def Task_1_Click(self):
        #TODO: Add timer to Task-click
        self.tabWidget.setCurrentIndex(0)
        with open('ReadMe1.txt', 'r') as f:
            text = f.read()
            self.label1.setText(text)

        with open('Code1.txt', 'r') as f:
            code = f.read()
            self.textbox.setText(code)

    def Task_2_Click(self):
        self.tabWidget.setCurrentIndex(0)
        with open('ReadMe2.txt', 'r') as f:
            text = f.read()
            self.label1.setText(text)

        with open('Code2.txt', 'r') as f:
            code = f.read()
            self.textbox.setText(code)

    def Task_3_Click(self):
        self.tabWidget.setCurrentIndex(0)
        with open('ReadMe3.txt', 'r') as f:
            text = f.read()
            self.label1.setText(text)

        with open('Code3.txt', 'r') as f:
            code = f.read()
            self.textbox.setText(code)

    def Task_4_Click(self):
        self.tabWidget.setCurrentIndex(0)
        with open('ReadMe4.txt', 'r') as f:
            text = f.read()
            self.label1.setText(text)

        with open('Code4.txt', 'r') as f:
            code = f.read()
            self.textbox.setText(code)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(640, 480)
    sys.exit(app.exec_())