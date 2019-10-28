from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
import subprocess
import logging
import time
from functools import partial
# from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, QGroupBox,
#                              QHBoxLayout)
# from PyQt5 import QtCore, QtGui


class MainAppWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        # self.today = datetime.date()
        # logging.basicConfig(format='%(name)s: %(asctime)s : %(message)s', level=logging.INFO,
        #                     filename="TimeLogger.log")
        logging.basicConfig(format='%(message)s', level=logging.INFO, filename="TimeLogger.log")
        self.time_logger = logging.getLogger('Time')
        # logging.basicConfig(format='%(message)s', level=logging.INFO, filename="CodeLogger.log")
        # self.code_logger = logging.getLogger('Code')
        # TODO: Have proper formatting for the time_logger

        self.mainLayout = QVBoxLayout()
        self.startButton = QPushButton("Start")

        self.codeIntervalLabel = QtWidgets.QLabel("Code Interval Time (seconds):")

        self.codeIntervalText = QLineEdit()
        self.codeIntervalText.setText("5")
        self.codeIntervalTime = 5

        # self.codeIntervalLabel.move(0, 100)
        # self.codeIntervalLabel.resize(20, 20)
        # self.codeIntervalLabel.resize(10, 200)
        self.mainLayout.addWidget(self.codeIntervalLabel)
        self.mainLayout.addWidget(self.codeIntervalText)
        self.mainLayout.addWidget(self.startButton)

        self.codeIntervalLabel.setAlignment(Qt.AlignBottom)
        # self.codeIntervalText.setAlignment(Qt.AlignTop)
        # self.codeIntervalText.move(0, -100)
        # self.startButton.move(100, 0)
        # self.codeIntervalLabel.move(100, 100)
        # self.codeEditorTextBox.move(20, 20)
        # self.codeEditorTextBox.move(20, 20)

        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)

        self.currentTask = None
        self.currentTask = 1
        self.currentTaskNumLabel = QLabel("Task %d" % self.currentTask)

        self.tabWidget = QTabWidget()

        self.currentTab = None

        self.tabLayout = QVBoxLayout()
        self.tabWidget.setLayout(self.tabLayout)

        self.readMe = 'ReadMe'
        self.codeEditor = 'Code Editor'
        self.terminal = 'Terminal'
        self.manual = 'Manual'
        self.tabs = {}

        self.numTasks = 4

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

        self.codeEditorTextBox = QTextEdit(self)
        with open('Code1.txt', 'r') as f:
            code = f.read()
        self.codeEditorTextBox.setText(code)
        # self.codeEditorTextBox.move(20, 20)
        # self.codeEditorTextBox.resize(280,200)
        codeEditor_layout.addWidget(self.codeEditorTextBox)
        # self.codePrevChangedState = None

        self.latestCodeFiles = ["Code%d.txt" % (i + 1) for i in range(self.numTasks)]
        self.latestCodes = [''] * self.numTasks
        for i in range(self.numTasks):
            with open(self.latestCodeFiles[i], 'r') as f:
                self.latestCodes[i] = f.read()

        self.latestCodeEditTime = [None] * self.numTasks
        self.codeChangeStartTime = [None] * self.numTasks
        self.previousCodeTask = self.currentTask

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
        self.manualLabel.setAlignment(Qt.AlignTop)
        self.manualLayout.addWidget(self.manualLabel)

        self.numManualPages = 4

        self.manualPageLabels = QtWidgets.QLabel()
        self.manualButtons = [QPushButton("Page %d" % (i + 1)) for i in range(self.numManualPages)]
        self.manualPageLabels.setText(
            "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % 1)
        # self.manualPageClicked = [self.manualPage1, self.manualPage2, self.manualPage3, self.manualPage4]
        self.manualButtonBox = QGroupBox()
        self.manualButtonsLayout = QHBoxLayout()
        self.manualButtonBox.setLayout(self.manualButtonsLayout)

        self.manualLayout.addWidget(self.manualPageLabels)

        for i in range(self.numManualPages):
            self.manualButtonsLayout.addWidget(self.manualButtons[i])
            # self.manualButtons[i].clicked.connect(self.manualPageClicked[i])
            self.manualButtons[i].clicked.connect(partial(self.manualPage_i, i+1))
        self.manualLayout.addWidget(self.manualButtonBox)
        self.currentManualPage = None

        ################ Tab Layout ################
        self.tabIndex = {0: self.readMe, 1: self.codeEditor, 2: self.terminal, 3: self.manual}
        self.tabs[self.readMe] = readme
        self.tabs[self.codeEditor] = codeEditor
        self.tabs[self.terminal] = terminal
        self.tabs[self.manual] = manual

        self.tabWidget.addTab(self.tabs[self.readMe], self.readMe)
        self.tabWidget.addTab(self.tabs[self.codeEditor], self.codeEditor)
        self.tabWidget.addTab(self.tabs[self.terminal], self.terminal)
        self.tabWidget.addTab(self.tabs[self.manual], self.manual)

        ################ Tasks ################
        # self.numTasks ->  # Defined earlier

        self.TaskButtonBox = QGroupBox()
        self.TaskButtonsLayout = QHBoxLayout()
        self.TaskButtonBox.setLayout(self.TaskButtonsLayout)

        self.Task_Buttons = [QPushButton("Task %d" % (i + 1)) for i in range(4)]

        for i in range(self.numTasks):
            self.TaskButtonsLayout.addWidget(self.Task_Buttons[i])

        self.taskStartTimes = [None] * self.numTasks
        self.taskEndTimes = [None] * self.numTasks

        ################ Click Events ################
        self.startButton.clicked.connect(self.startButtonClicked)  # , "Hello") #("Hello"))
        # self.startButton.clicked.connect(lambda: self.startButtonClicked("hello"))
        # self.startButton.clicked.connect(partial(self.startButtonClicked, "hello"))

        self.tabWidget.currentChanged.connect(self.whatTab)
        # Reference: https://stackoverflow.com/questions/21562485/pyqt-qtabwidget-currentchanged

        self.execute.clicked.connect(self.executeClicked)

        for i in range(self.numTasks):
            self.Task_Buttons[i].clicked.connect(partial(self.task_i_Click, i + 1))

        self.codeEditorTextBox.textChanged.connect(self.codeChanged)

        # TODO: When was each task started and ended

        # self.actionExit.triggered.connect(self.close)

    def startButtonClicked(self, s="Default"):
        if not s:
            print("Def")
        else:
            print(s)
        try:
            self.codeIntervalTime = float(self.codeIntervalText.text())
            print("Code interval time: %.2f" % self.codeIntervalTime)
        except ValueError:
            return
        self.codeIntervalLabel.setDisabled(True)
        self.codeIntervalLabel.setVisible(False)
        self.codeIntervalText.setDisabled(True)
        self.codeIntervalText.setVisible(False)
        self.startButton.setDisabled(True)
        self.startButton.setVisible(False)
        self.mainLayout.removeWidget(self.startButton)
        self.mainLayout.removeWidget(self.codeIntervalLabel)
        self.mainLayout.removeWidget(self.codeIntervalText)
        self.mainLayout.addWidget(self.currentTaskNumLabel)
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addWidget(self.TaskButtonBox)
        self.currentTabName = self.tabIndex[0]
        self.time_logger.info("Start Time: %s\n\n" % time.asctime())
        self.startTime = time.time()

    def tabSelected(self, arg=None):
        print('\n\t tabSelected() current Tab index =', arg)

    def manualPage_i(self, i):
        pageNum = i
        if self.currentManualPage != pageNum:
            self.currentManualPage = pageNum
            self.manualPageLabels.setText(
                "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % pageNum)
            now = time.time() - self.startTime
            now_minutes = int(now // 60)
            now_seconds = round(now % 60, 1)
            # self.time_logger.info("\nTask %d %d:%.1fs" % (self.currentTask, now_minutes, now_seconds))
            self.time_logger.info("Manual page %d:   %d:%.1fs" % (pageNum, now_minutes, now_seconds))

    def whatTab(self):
        currentIndex = self.tabWidget.currentIndex()
        currentTabName = self.tabIndex[currentIndex]
        if self.currentTab != currentTabName:
            self.currentTab = currentTabName
            try:
                now = time.time() - self.startTime
                now_minutes = int(now // 60)
                now_seconds = round(now % 60, 1)
                self.time_logger.info("Tab %s:   %d:%.1fs" % (currentTabName, now_minutes, now_seconds))
                pageNum = 1
                if self.currentTab == self.tabIndex[3]:
                    self.currentManualPage = pageNum
                    self.manualPageLabels.setText(
                        "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % pageNum)
                    self.time_logger.info("Manual page %d:   %d:%.1fs" % (pageNum, now_minutes, now_seconds))

                # taskIndex = self.currentTask - 1
                # self.codeEditorTextBox.setText(self.latestCodes[taskIndex])


            except ValueError:
                now_minutes = 0
                now_seconds = 0
                self.time_logger.info("Tab %s:   %d:%.1fs" % (currentTabName, now_minutes, now_seconds))
                # self.codeEditorTextBox.setText(self.latestCodes[0])
                # start
        # currentWidget = self.tabWidget.currentWidget()

        print('\n\t Query: current Tab index =', currentIndex)

    # noinspection PyTypeChecker
    def codeChanged(self):
        # TODO: Summarised code modification logging
        # nt
        # taskChangedFlag = False
        if self.previousCodeTask != self.currentTask:
            taskNum = self.previousCodeTask
            self.previousCodeTask = self.currentTask
            # taskChangedFlag = True
        else:
            taskNum = self.currentTask
        taskIndex = taskNum - 1
        now = time.time() - self.startTime

        # now_minutes = int(now // 60)
        # now_seconds = int(now % 60)
        # now_millis = int(now * 1000)

        if self.latestCodeEditTime[taskIndex] is None:
            self.codeChangeStartTime[taskIndex] = now
            self.latestCodeEditTime[taskIndex] = now

        elif now - self.latestCodeEditTime[taskIndex] < self.codeIntervalTime:
            self.latestCodeEditTime[taskIndex] = now
            return
        else:
            self.codeChangeStartTime[taskIndex] = now
            self.latestCodeEditTime[taskIndex] = now
            self.codeChangedLog(taskIndex)
        code = self.codeEditorTextBox.toPlainText()
        self.latestCodes[self.currentTask - 1] = code
        # self.codeEditorTextBox.setText(code)   #DoNOT uncomment this line

    # noinspection PyTypeChecker
    def codeChangedLog(self, taskIndex):
        prevStartTime = self.codeChangeStartTime[taskIndex]
        prevEndTime = self.latestCodeEditTime[taskIndex]

        code = self.codeEditorTextBox.toPlainText()
        start_minutes = int(prevStartTime // 60)
        start_seconds = int(prevStartTime % 60)
        start_millis = int(prevStartTime * 1000)
        end_minutes = int(prevEndTime // 60)
        end_seconds = int(prevEndTime % 60)
        end_millis = int(prevEndTime * 1000)

        fname = 'Codes/Code%d___%d_%d_%d___%d_%d_%d.txt' % (self.currentTask, start_minutes, start_seconds,
                                                            start_millis, end_minutes, end_seconds, end_millis)
        with open(fname, 'w') as f:
            f.write(code)
        self.time_logger.info("Code changed: \n    Start:  %d:%.1fs \n    End:  %d:%.1fs\n" % (
            start_minutes, start_seconds, end_minutes, end_seconds))
        print("Code changed")

    def closeEvent(self, event):
        try:
            now = time.time() - self.startTime
        except AttributeError:
            now = 0.0
        now_minutes = int(now // 60)
        now_seconds = int(now % 60)
        now_millis = int(now * 1000)

        for i in range(self.numTasks):
            taskIndex = i
            if self.latestCodeEditTime[taskIndex] is not None:
                self.codeChangedLog(taskIndex)

        for i in range(self.numTasks):
            if self.taskEndTimes[i] is None:
                # noinspection PyTypeChecker
                self.taskEndTimes[i] = (now_minutes, now_seconds, now_millis)
            try:
                self.time_logger.info(
                    "Task %d:   Start: %d %.1fs" % (i + 1, self.taskStartTimes[i][0], self.taskStartTimes[i][1]))
                self.time_logger.info(
                    "Task %d:   End: %d %.1fs \n" % (i + 1, self.taskEndTimes[i][0], self.taskEndTimes[i][1]))
            except (TypeError, IndexError, ValueError):
                pass
        self.time_logger.info("Exit:   %d:%.1fs" % (now_minutes, now_seconds))
        sys.exit()

    def executeClicked(self):
        code = self.codeEditorTextBox.toPlainText()
        # p = subprocess.Popen("ls hello", stdout=subprocess.PIPE, shell=True)
        p = subprocess.Popen(code, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        # TODO: Save the task status
        # TODO: When does the task end (complete)
        (output, err) = p.communicate()
        outStr = output.decode('utf-8')
        errStr = err.decode('utf-8')

        if errStr:
            if outStr:
                outputText = outStr + '\n' + errStr
            else:
                outputText = errStr
        else:
            outputText = outStr
        self.terminalLabel.setText(outputText)

    def task_i_Click(self, i):
        taskNum = i
        print("TaskNum:",i)
        if self.taskStartTimes[taskNum - 1] is None:
            self.currentTask = taskNum
            self.currentTaskNumLabel.setText("Task %d" % taskNum)
            self.codePrevChangedState = None

            now = time.time() - self.startTime
            now_minutes = int(now // 60)
            now_seconds = round(now % 60, 1)
            self.time_logger.info("\nTask %d %d:%.1fs" % (taskNum, now_minutes, now_seconds))
            self.time_logger.info("Tab %s:   %d:%.1fs" % ("Read Me", now_minutes, now_seconds))
            # noinspection PyTypeChecker
            self.taskStartTimes[taskNum - 1] = [now_minutes, now_seconds]

            self.tabWidget.setCurrentIndex(0)
            with open('ReadMe%d.txt' % taskNum, 'r') as f:
                text = f.read()
                self.readmeLabel.setText(text)

            code = self.latestCodes[taskNum - 1]
            self.codeEditorTextBox.setText(code)

        if self.currentTask != taskNum:
            oldTask = self.currentTask
            self.currentTask = taskNum
            self.currentTaskNumLabel.setText("Task %d" % taskNum)
            self.latestCodes[oldTask - 1] = self.codeEditorTextBox.toPlainText()
            # self.codeChangedLog(self, oldTask-1)
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

            # with open(self.latestCodeFiles[taskNum - 1], 'r') as f:
            #     code = f.read()
            #     self.codeEditorTextBox.setText(code)
            code = self.latestCodes[taskNum - 1]
            self.codeEditorTextBox.setText(code)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainAppWindow()
    mainWin.show()
    # mainWin.resize(1366, 720)
    mainWin.resize(640, 480)
    sys.exit(app.exec_())
