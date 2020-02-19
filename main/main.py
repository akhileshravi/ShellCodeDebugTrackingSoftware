from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, os
import subprocess
import logging
import time
from functools import partial
import shutil
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
# from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QVBoxLayout, QGroupBox,
#                              QHBoxLayout)
# from PyQt5 import QtCore, QtGui


class MainAppWindow(QMainWindow):
    def __init__(self):

        super(QMainWindow, self).__init__()

        self.cwd = os.getcwd() + '/'
        print(self.cwd)
        self.homePath = self.cwd[:-5]
        expt = os.path.join(self.homePath, "Experiments")
        exptNum = len(os.listdir(expt)) + 1
        self.dataLogPath = os.path.join(self.homePath, "Experiments", "Expt_%d" % exptNum)
        os.mkdir(self.dataLogPath)
        self.codeLogPath = os.path.join(self.dataLogPath, "Codes")
        os.mkdir(self.codeLogPath)

        logging.basicConfig(format='%(message)s', level=logging.INFO,
                            filename=os.path.join(self.dataLogPath, "TimeLogger.log"))
        self.time_logger = logging.getLogger('Time')
        # TODO: Have proper formatting for the time_logger

        self.numTasks = 12
        ################ File Paths ################
        self.taskPaths = ["TaskFiles/Task_%d/" % (i+1) for i in range(self.numTasks)]
        self.codeFiles = ["Code_%d.sh" % (i+1) for i in range(self.numTasks)]
        self.readmeFiles = ["ReadMe_%d.txt" % (i+1) for i in range(self.numTasks)]

        os.chdir(self.taskPaths[0])

        self.mainLayout = QVBoxLayout()
        self.startButton = QPushButton("Start")

        self.codeIntervalLabel = QtWidgets.QLabel("Code Interval Time (seconds):")

        self.codeIntervalText = QLineEdit()
        self.codeIntervalText.setText("5")
        self.codeIntervalTime = 5

        self.mainLayout.addWidget(self.codeIntervalLabel)
        self.mainLayout.addWidget(self.codeIntervalText)
        self.mainLayout.addWidget(self.startButton)

        self.codeIntervalLabel.setAlignment(Qt.AlignBottom)

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
        self.video = 'Video'
        self.tabs = {}

        #TODO: Use correct number of characters per line in the readme files. (readme file 1 is different between Task files and Orig..)


        ################ ReadMe Tab ################
        readme = QWidget()
        readMe_layout = QVBoxLayout()
        readme.setLayout(readMe_layout)

        self.readmeLabel = QtWidgets.QLabel()
        with open(self.cwd + self.taskPaths[0] + self.readmeFiles[0], 'r') as f:
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
        with open(self.cwd + self.taskPaths[0] + self.codeFiles[0], 'r') as f:
            code = f.read()
        self.codeEditorTextBox.setText(code)
        codeEditor_layout.addWidget(self.codeEditorTextBox)

        self.latestCodeFiles = [self.cwd + self.taskPaths[i] + self.codeFiles[i] for i in range(self.numTasks)]
        self.latestCodes = [''] * self.numTasks
        for i in range(self.numTasks):
            with open(self.latestCodeFiles[i], 'r') as f:
                self.latestCodes[i] = f.read()

        self.latestCodeEditTime = [None] * self.numTasks
        self.codeChangeStartTime = [None] * self.numTasks
        self.previousCodeTask = self.currentTask
        self.prevCodeChanged = False
        self.taskChangedFlag = False

        ################ Terminal Tab ################
        terminal = QWidget()
        self.terminalLayout = QVBoxLayout()
        terminal.setLayout(self.terminalLayout)
        self.terminalLabel = QtWidgets.QLabel()
        self.terminalLayout.addWidget(self.terminalLabel)

        self.execute = QPushButton("Execute")
        self.resetButton = QPushButton("Reset")
        self.terminalLayout.addWidget(self.execute)
        self.terminalLayout.addWidget(self.resetButton)

        ################ Manual Tab ################
        manual = QWidget()
        self.manualLayout = QVBoxLayout()
        manual.setLayout(self.manualLayout)
        self.manualLabel = QtWidgets.QLabel()
        self.manualLabel.setAlignment(Qt.AlignTop)
        self.manualLayout.addWidget(self.manualLabel)

        self.numManualPages = 4

        self.manualFiles = ["ManualPage%d.txt" % (i+1) for i in range(self.numManualPages)]
        self.manualPageLabels = QtWidgets.QLabel()
        self.manualButtons = [QPushButton("Page %d" % (i + 1)) for i in range(self.numManualPages)]
        pageNum = 1
        self.currentManualPage = pageNum
        with open(self.cwd + self.manualFiles[pageNum - 1], 'r') as f:
            manText = f.read()
        self.manualPageLabels.setText(manText)
        # self.manualPageLabels.setText(
        #     "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % 1)
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

        ################ Video Tab ################

        self.videotab = QWidget()
        self.video_layout = QVBoxLayout()
        self.videotab.setLayout(self.video_layout)
        self.videowidget = QVideoWidget()
        self.videowidget.resize(300, 300)
        self.videowidget.move(0, 0)
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.videowidget)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("/home/akhil/Videos/SoftwareTrial.mp4")))

        self.videoButton = QPushButton('Start Video')
        self.videoButton.clicked.connect(self.callback)
        self.video_layout.addWidget(self.videowidget)
        # self.video_layout.addWidget(self.player)
        self.video_layout.addWidget(self.videoButton)


        ################ Tab Layout ################
        self.tabIndex = {0: self.readMe, 1: self.codeEditor, 2: self.terminal, 3: self.manual, 4:self.videotab}
        self.tabs[self.readMe] = readme
        self.tabs[self.codeEditor] = codeEditor
        self.tabs[self.terminal] = terminal
        self.tabs[self.manual] = manual
        self.tabs[self.video] = self.videotab

        self.tabWidget.addTab(self.tabs[self.readMe], self.readMe)
        self.tabWidget.addTab(self.tabs[self.codeEditor], self.codeEditor)
        self.tabWidget.addTab(self.tabs[self.terminal], self.terminal)
        self.tabWidget.addTab(self.tabs[self.manual], self.manual)
        self.tabWidget.addTab(self.tabs[self.video], self.video)

        ################ Tasks ################
        # self.numTasks ->  # Defined earlier

        self.TaskButtonBox = QGroupBox()
        self.TaskButtonsLayout = QHBoxLayout()
        self.TaskButtonBox.setLayout(self.TaskButtonsLayout)

        self.Task_Buttons = [QPushButton("Task %d" % (i + 1)) for i in range(self.numTasks)]

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

    def startButtonClicked(self, s="Default"):
        if not s:
            print("Def")
        else:
            print(s)
        try:
            self.codeIntervalTime = float(self.codeIntervalText.text())
            print("Code interval time: %.2f" % self.codeIntervalTime)
            self.time_logger.info("Code Interval Time: %d s\n --------" % self.codeIntervalTime)
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
            self.currentManualPage = pageNum
            with open(self.cwd + self.manualFiles[pageNum - 1], 'r') as f:
                manText = f.read()
            self.manualPageLabels.setText(manText)
            # self.manualPageLabels.setText(
            #     "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % pageNum)
            now = time.time() - self.startTime
            now_minutes = int(now // 60)
            now_seconds = round(now % 60, 1)
            # self.time_logger.info("\nTask %d %d:%.1fs" % (self.currentTask, now_minutes, now_seconds))
            self.time_logger.info("Manual page %d:   %d:%.1fs" % (pageNum, now_minutes, now_seconds))

    def callback(self):
        self.player.setPosition(0) # to start at the beginning of the videowidget every time
        self.videowidget.show()
        self.player.play()

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
                    with open(self.cwd + self.manualFiles[pageNum-1], 'r') as f:
                        manText = f.read()
                    self.manualPageLabels.setText(manText)
                        # "This is page %d.\nDo the following.\n  1. Read.\n  2. Write.\n  3. Execute" % pageNum)
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
        # self.taskChangedFlag = False
        if self.previousCodeTask != self.currentTask:
            taskNum = self.previousCodeTask
            # self.taskChangedFlag = True
            taskIndex = taskNum - 1
            now = time.time() - self.startTime

            self.codeChangeStartTime[self.currentTask-1] = None
            self.latestCodeEditTime[self.currentTask-1] = None

            if self.prevCodeChanged:
                self.codeChangedLog(taskIndex)
            code = self.codeEditorTextBox.toPlainText()
            # self.latestCodes[taskIndex] = code
            # self.codeEditorTextBox.setText(code)   #DoNOT uncomment this line
            self.previousCodeTask = self.currentTask
            print("Code Task changed")
            self.prevCodeChanged = False

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

            else:
                self.codeChangeStartTime[taskIndex] = now
                self.latestCodeEditTime[taskIndex] = now
                self.codeChangedLog(taskIndex)
            code = self.codeEditorTextBox.toPlainText()
            self.latestCodes[taskIndex] = code
            self.prevCodeChanged = True
            # self.codeEditorTextBox.setText(code)   #DoNOT uncomment this line


    # noinspection PyTypeChecker
    def codeChangedLog(self, taskIndex):
        prevStartTime = self.codeChangeStartTime[taskIndex]
        prevEndTime = self.latestCodeEditTime[taskIndex]

        code = self.latestCodes[taskIndex]
        start_minutes = int(prevStartTime // 60)
        start_seconds = int(prevStartTime % 60)
        start_millis = int(prevStartTime * 1000)
        end_minutes = int(prevEndTime // 60)
        end_seconds = int(prevEndTime % 60)
        end_millis = int(prevEndTime * 1000)

        fname = os.path.join(self.codeLogPath,
                             'Code%d___%d_%d_%d___%d_%d_%d.txt' % (self.currentTask, start_minutes, start_seconds,
                                                            start_millis, end_minutes, end_seconds, end_millis)
                             )
        with open(fname, 'w') as f:
            f.write(code)
        self.time_logger.info("Code changed: \n    Start:  %d:%.1fs \n    End:  %d:%.1fs\n" % (
            start_minutes, start_seconds, end_minutes, end_seconds))
        print("Code changed")

    def resetClicked(self):
        now = time.time()
        now_minutes = int(now // 60)
        now_seconds = int(now % 60)

        taskIndex = self.currentTask - 1
        with open(self.latestCodeFiles[taskIndex], 'r') as f:
            code = f.read()
            self.latestCodes[taskIndex] = code
        # self.codeEditorTextBox.setText(code)
        self.time_logger.info("Reset code: %d:%.1f" % (now_minutes, now_seconds))
        os.chdir(self.cwd)
        copyPath = os.path.join(self.cwd, "main", "OriginalTaskFiles", "Task_%d"%(taskIndex+1))
        rmPath = os.path.join(self.cwd, "main", "TaskFiles", "Task_%d"%(taskIndex+1))
        shutil.rmtree(rmPath)
        shutil.copytree(copyPath, rmPath)
        os.chdir(self.cwd + self.taskPaths[taskIndex])
        with open(self.cwd + self.taskPaths[taskIndex] + self.codeFiles[taskIndex], 'r') as f:
            code = f.read()
            self.latestCodes[taskIndex] = code
        self.codeEditorTextBox.setText(code)

    def closeEvent(self, event):
        try:
            now = time.time() - self.startTime
        except AttributeError:
            now = 0.0
        now_minutes = int(now // 60)
        now_seconds = int(now % 60)
        now_millis = int(now * 1000)

        taskIndex = self.currentTask - 1
        if self.prevCodeChanged:
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
        os.chdir(self.cwd + self.taskPaths[self.currentTask-1])
        code = self.codeEditorTextBox.toPlainText()
        # p = subprocess.Popen("ls hello", stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        codelines = code.split('\n')
        outStr = ''
        for line in codelines:
            p = subprocess.Popen(line, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
            # TODO: Save the task status
            # TODO: When does the task end (complete)
            (output, err) = p.communicate()
            outStr += output.decode('utf-8')
            outStr += err.decode('utf-8')

        outputText = outStr
        self.terminalLabel.setText(outputText)

    def task_i_Click(self, i):
        taskNum = i
        taskIndex = i-1
        print("TaskNum:",i)
        if self.taskStartTimes[taskNum - 1] is None:
            os.chdir("../../")
            os.chdir(self.taskPaths[taskIndex])
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
            with open(self.cwd + self.taskPaths[taskNum-1] + self.readmeFiles[taskNum-1], 'r') as f:
                text = f.read()
                self.readmeLabel.setText(text)

            code = self.latestCodes[taskIndex]
            self.codeEditorTextBox.setText(code)
            self.terminalLabel.clear()

        if self.currentTask != taskNum:
            os.chdir("../../")
            os.chdir(self.taskPaths[taskIndex])
            self.taskChangedFlag = True
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
            with open(self.cwd + self.taskPaths[taskIndex] + self.readmeFiles[taskIndex], 'r') as f:
                text = f.read()
                self.readmeLabel.setText(text)

            # with open(self.latestCodeFiles[taskNum - 1], 'r') as f:
            #     code = f.read()
            #     self.codeEditorTextBox.setText(code)
            code = self.latestCodes[taskNum - 1]
            self.codeEditorTextBox.setText(code)
            self.terminalLabel.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainAppWindow()
    mainWin.show()
    # mainWin.resize(1366, 720)
    mainWin.resize(1366, 720)
    sys.exit(app.exec_())
