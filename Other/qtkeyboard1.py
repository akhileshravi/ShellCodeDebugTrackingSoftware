import sys
from PyQt5 import QtGui, QtWidgets, QtCore


class Body(QtWidgets.QWidget):
    def __init__(self):
        super(Body, self).__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(400, 400, 250, 150)
        self.setWindowTitle('keyboard-Event handler')
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    e = Body()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()