# from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QGroupBox, QHBoxLayout
import sys, os
import subprocess
import logging
import time

class Dialog_01(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        # self.today = datetime.date()
        # logging.basicConfig(format='%(name)s: %(asctime)s : %(message)s', level=logging.INFO, filename="TimeLogger.log")
        logging.basicConfig(format='%(message)s', level=logging.INFO, filename="TimeLogger.log")
        self.time_logger = logging.getLogger('Time')
        # logging.basicConfig(format='%(message)s', level=logging.INFO, filename="CodeLogger.log")
        # self.code_logger = logging.getLogger('Code')
        # TODO: Have proper formatting for the time_logger

        self.mainLayout = QVBoxLayout()
        self.startButton = QPushButton("Start")
        self.mainLayout.addWidget(self.startButton)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)


        self.currentTask = None
        self.currentTask = 1

        self.tabWidget = QTabWidget()

        self.currentTab = None

        # self.tabWidget.connect(self.tabWidget, QWidget.SIGNAL("currentChanged(int)"), self.tabSelected)
        self.tabWidget.currentChanged.connect(self.whatTab)
        # Reference: https://stackoverflow.com/questions/21562485/pyqt-qtabwidget-currentchanged

        self.tabLayout = QVBoxLayout()
        self.tabWidget.setLayout(self.tabLayout)

        self.readMe = 'ReadMe'
        self.codeEditor = 'Code Editor'
        self.terminal = 'Terminal'
        self.manual = 'Manual'
        self.tabs = {}


        ################ ReadMe Tab ################
        readme = QWidget()
        readMe_layout = QVBoxLayout()
        readme.setLayout(readMe_layout)

        self.readmeLabel = QtWidgets.QLabel()
        with open('ReadMe1.txt', 'r') as f:
            text = f.read()
        self.readmeLabel.setText(text)
        self.readmeLabel.setAlignment(Qt.AlignLeft)
        readMe_layout.addWidget(self.readmeLabel)
        # Reference : https://www.tutorialspoint.com/pyqt/pyqt_qlabel_widget.htm


        ################ Code Editor Tab ################
        codeEditor = QWidget()
        codeEditor_layout = QVBoxLayout()
        codeEditor.setLayout(codeEditor_layout)

        self.textbox = QTextEdit(self)
        with open('Code1.txt', 'r') as f:
            code = f.read()
        self.textbox.setText(code)
        # self.textbox.move(20, 20)
        # self.textbox.resize(280,200)
        codeEditor_layout.addWidget(self.textbox)
        self.codePrevChangedState = None


        ################ Terminal Tab ################
        terminal = QWidget()
        self.terminalLayout = QVBoxLayout()
        terminal.setLayout(self.terminalLayout)
        self.terminalLabel = QtWidgets.QLabel()
        self.terminalLayout.addWidget(self.terminalLabel)

        self.execute = QPushButton("Execute")
        self.terminalLayout.addWidget(self.execute)


        ################ Manual Tab ################
        manual = QWidget()
        self.manualLayout = QVBoxLayout()
        manual.setLayout(self.manualLayout)
        self.manualLabel = QtWidgets.QLabel()
        self.manualLayout.addWidget(self.manualLabel)

        self.numManualPages = 4

        self.manualPageLabels = QtWidgets.QLabel()
        self.manualButtons = [QPushButton("Page %d" % (i+1)) for i in range(self.numManualPages)]
        self.manualPageLabels.setText("This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % (1))
        self.manualPageClicked = [self.manualPage1, self.manualPage2, self.manualPage3, self.manualPage4]
        self.manualButtonBox = QGroupBox()
        self.manualButtonsLayout = QHBoxLayout()
        self.manualButtonBox.setLayout(self.manualButtonsLayout)

        self.manualLayout.addWidget(self.manualPageLabels)

        for i in range(self.numManualPages):
            self.manualButtonsLayout.addWidget(self.manualButtons[i])
            self.manualButtons[i].clicked.connect(self.manualPageClicked[i])

        self.manualLayout.addWidget(self.manualButtonBox)
        self.currentManualPage = None


        ################ Tab Layout ################
        self.tabIndex = {0: self.readMe, 1: self.codeEditor, 2: self.terminal, 3:self.manual}
        self.tabs[self.readMe] = readme
        self.tabs[self.codeEditor] = codeEditor
        self.tabs[self.terminal] = terminal
        self.tabs[self.manual] = manual

        self.tabWidget.addTab(self.tabs[self.readMe], self.readMe)
        self.tabWidget.addTab(self.tabs[self.codeEditor], self.codeEditor)
        self.tabWidget.addTab(self.tabs[self.terminal],self.terminal)
        self.tabWidget.addTab(self.tabs[self.manual], self.manual)

        self.TaskButtonBox = QGroupBox()
        self.TaskButtonsLayout = QHBoxLayout()
        self.TaskButtonBox.setLayout(self.TaskButtonsLayout)

        # Button_01 = QPushButton("What Tab?")
        # self.TaskButtonsLayout.addWidget(Button_01)
        # Button_01.clicked.connect(self.whatTab)


        ################ Tasks ################
        self.numTasks = 4

        self.Task_Buttons = [QPushButton("Task %d" % (i+1)) for i in range(4)]

        for i in range(self.numTasks):
            self.TaskButtonsLayout.addWidget(self.Task_Buttons[i])

        # Task_1 = QPushButton("Task 1")
        # self.TaskButtonsLayout.addWidget(Task_1)
        #
        # Task_2 = QPushButton("Task 2")
        # self.TaskButtonsLayout.addWidget(Task_2)
        #
        # Task_3 = QPushButton("Task 3")
        # self.TaskButtonsLayout.addWidget(Task_3)
        #
        # Task_4 = QPushButton("Task 4")
        # self.TaskButtonsLayout.addWidget(Task_4)

        self.latestCodeFiles = ["Code%d.txt" % (i+1) for i in  range(4)]

        self.taskStartTimes = [None for i in range(self.numTasks)]
        self.taskEndTimes = [None for i in range(self.numTasks)]

        self.startButton.clicked.connect(self.startButtonClicked) #, "Hello") #("Hello"))
        self.execute.clicked.connect(self.executeClicked)

        self.Task_i_Click_functions = [self.Task_1_Click, self.Task_2_Click, self.Task_3_Click, self.Task_4_Click]

        for i in range(self.numTasks):
            self.Task_Buttons[i].clicked.connect(self.Task_i_Click_functions[i])
        # Task_1.clicked.connect(self.Task_1_Click)
        # Task_2.clicked.connect(self.Task_2_Click)
        # Task_3.clicked.connect(self.Task_3_Click)
        # Task_4.clicked.connect(self.Task_4_Click)

        self.textbox.textChanged.connect(self.codeChanged)

        # TODO: When was each task started and ended

        # self.actionExit.triggered.connect(self.close)


    def startButtonClicked(self, s):
        print(s)
        self.mainLayout.removeWidget(self.startButton)
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addWidget(self.TaskButtonBox)
        self.currentTabName = self.tabIndex[0]
        self.time_logger.info("Start Time: %s\n\n" % time.asctime())
        self.startTime = time.time()


    def tabSelected(self, arg=None):
        print ('\n\t tabSelected() current Tab index =', arg)


    def manualPage_i(self, i):
        pageNum = i
        if self.currentManualPage != pageNum:
            self.currentManualPage = pageNum
            self.manualPageLabels.setText(
                "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % (pageNum))
            now = time.time() - self.startTime
            now_minutes = int(now // 60)
            now_seconds = round(now % 60, 1)
            self.time_logger.info("\nTask %d %d:%.1fs" % (self.currentTask, now_minutes, now_seconds))
            self.time_logger.info("Manual page %d:   %d:%.1fs" % (pageNum, now_minutes, now_seconds))

    def manualPage1(self):
        self.manualPage_i(1)

    def manualPage2(self):
        self.manualPage_i(2)

    def manualPage3(self):
        self.manualPage_i(3)

    def manualPage4(self):
        self.manualPage_i(4)


    def whatTab(self):
        currentIndex = self.tabWidget.currentIndex()
        currentTabName = self.tabIndex[currentIndex]
        if self.currentTab != currentTabName:
            self.currentTab = currentTabName
            try:
                now = time.time() - self.startTime
                now_minutes = int(now//60)
                now_seconds = round(now%60,1)
                self.time_logger.info("Tab %s:   %d:%.1fs" % (currentTabName, now_minutes, now_seconds))
                pageNum = 1
                self.currentManualPage = pageNum
                self.manualPageLabels.setText(
                    "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % (pageNum))
            except AttributeError:
                now_minutes = 0
                now_seconds = 0
                self.time_logger.info("Tab %s:   %d:%.1fs" % (currentTabName, now_minutes, now_seconds))
                # start
        # currentWidget = self.tabWidget.currentWidget()

        print ('\n\t Query: current Tab index =', currentIndex)


    def codeChanged(self):
        # TODO: Summarised code modification logging
        # nt
        code = self.textbox.toPlainText()
        now = time.time() - self.startTime
        now_minutes = int(now // 60)
        now_seconds = int(now % 60)
        now_millis = int(now * 1000)
        fname = 'Codes/Code%d___%d_%d_%d.txt' % (self.currentTask, now_minutes, now_seconds, now_millis)
        with open(fname, 'w') as f:
            f.write(code)
        self.time_logger.info("Tab %s:   %d:%.1fs" % ("Code changed", now_minutes, now_seconds))
        print("Code changed")

    def closeEvent(self, event):
        now = time.time() - self.startTime
        now_minutes = int(now // 60)
        now_seconds = int(now % 60)
        now_millis = int(now * 1000)
        for i in range(self.numTasks):
            if self.taskEndTimes[i] is None:
                self.taskEndTimes[i] = [now_minutes, now_seconds, now_millis]
            try:
                self.time_logger.info("Task %d:   Start: %d %.1fs" % (i+1, self.taskStartTimes[i][0], self.taskStartTimes[i][1]))
                self.time_logger.info(
                    "Task %d:   End: %d %.1fs \n" % (i + 1, self.taskEndTimes[i][0], self.taskEndTimes[i][1]))
            except:
                pass
        self.time_logger.info("Exit:   %d:%.1fs" % (now_minutes, now_seconds))


    def executeClicked(self):
        code = self.textbox.toPlainText()
        # p = subprocess.Popen("ls hello", stdout=subprocess.PIPE, shell=True)
        p = subprocess.Popen(code, stdout=subprocess.PIPE, shell=True)
        # TODO: Take errors from the Linux Shell commands and display them
        # TODO: Save the task status
        # TODO: When does the task end (complete)
        (output, err) = p.communicate()
        outstr = output.decode('utf-8')
        self.terminalLabel.setText(outstr)


    def Task_i_Click(self, i):
        taskNum = i
        if self.taskStartTimes[taskNum-1] is None:
            self.currentTask = taskNum
            self.codePrevChangedState = None
            now = time.time() - self.startTime
            now_minutes = int(now // 60)
            now_seconds = round(now % 60, 1)
            self.time_logger.info("\nTask %d %d:%.1fs" % (taskNum, now_minutes, now_seconds))
            self.time_logger.info("Tab %s:   %d:%.1fs" % ("Read Me", now_minutes, now_seconds))
            self.taskStartTimes[taskNum-1] = [now_minutes, now_seconds]

        if self.currentTask != taskNum:
            self.currentTask = taskNum
            self.codePrevChangedState = None
            now = time.time() - self.startTime
            now_minutes = int(now // 60)
            now_seconds = round(now % 60, 1)
            self.time_logger.info("\nTask %d %d:%.1fs" % (taskNum, now_minutes, now_seconds))
            self.time_logger.info("Tab %s:   %d:%.1fs" % ("Read Me", now_minutes, now_seconds))

            self.tabWidget.setCurrentIndex(0)
            with open('ReadMe%d.txt' % taskNum, 'r') as f:
                text = f.read()
                self.readmeLabel.setText(text)

            with open(self.latestCodeFiles[0], 'r') as f:
                code = f.read()
                self.textbox.setText(code)

    def Task_1_Click(self):
        self.Task_i_Click(1)

    def Task_2_Click(self):
        self.Task_i_Click(2)

    def Task_3_Click(self):
        self.Task_i_Click(3)

    def Task_4_Click(self):
        self.Task_i_Click(4)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog_1 = Dialog_01()
    dialog_1.show()
    dialog_1.resize(640, 480)
    sys.exit(app.exec_())