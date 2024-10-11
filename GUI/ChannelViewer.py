from PyQt5 import QtCore, QtGui, QtWidgets

class ChannelViewer(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(x, y, width, height))
        self.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)