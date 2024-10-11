from PyQt5 import QtCore, QtGui, QtWidgets
from ChannelEditor import ChannelEditor
from ChannelViewer import ChannelViewer
from SignalEditWindow import SignalEditor


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        #Window Setup
        MainWindow.setObjectName("Signal Viewer")
        MainWindow.setFixedSize(1379, 870)
        MainWindow.setMouseTracking(False)
        MainWindow.setStyleSheet("\n"
"background-color: rgb(42, 42, 42);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Channel Viewer Setup
        self.Channel1Viewer = ChannelViewer(self.centralwidget,290, 100, 731, 281)
        self.Channel2Viewer = ChannelViewer(self.centralwidget,290, 500, 731, 281)

        self.Channel1Editor = ChannelEditor(self.centralwidget, 1090, 100, 261, 281, "Channel 1")
        self.Channel2Editor = ChannelEditor(self.centralwidget, 1090, 500, 261, 281, "Channel 2")

        #signal controls
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 60, 271, 791))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("background-color: rgb(42, 42, 42); border:0px;")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        self.Signal1EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 1")
        self.Signal2EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 2")
        self.Signal3EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 3")
        self.Signal4EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 4")
        self.Signal5EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 5")

        self.verticalLayout.addWidget(self.Signal1EditingWindow)
        self.verticalLayout.addWidget(self.Signal2EditingWindow)
        self.verticalLayout.addWidget(self.Signal3EditingWindow)
        self.verticalLayout.addWidget(self.Signal4EditingWindow)
        self.verticalLayout.addWidget(self.Signal5EditingWindow)

        self.scrollAreaWidgetContents.setMinimumHeight(1300)

        #Taskbar Setup
        self.TaskBar = QtWidgets.QFrame(self.centralwidget)
        self.TaskBar.setGeometry(QtCore.QRect(-1, 0, 1381, 51))
        self.TaskBar.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.TaskBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TaskBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TaskBar.setObjectName("TaskBar")
        self.UploadButton = QtWidgets.QPushButton(self.TaskBar)
        self.UploadButton.setGeometry(QtCore.QRect(460, 10, 121, 28))
        self.UploadButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 15px;\n"
"background-color:transparent;\n"
"font-weight:800;")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("D:\\College\\Third year\\First Term\\DSP\\Tasks\\Task 1\\Signal-Viewer\\GUI\\Deliverables/downloads.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UploadButton.setIcon(icon5)
        self.UploadButton.setIconSize(QtCore.QSize(20, 20))
        self.UploadButton.setObjectName("UploadButton")
        self.ConnectToWebsite = QtWidgets.QPushButton(self.TaskBar)
        self.ConnectToWebsite.setGeometry(QtCore.QRect(630, 10, 171, 28))
        self.ConnectToWebsite.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 15px;\n"
"background-color:transparent;\n"
"font-weight:800;")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("D:\\College\\Third year\\First Term\\DSP\\Tasks\\Task 1\\Signal-Viewer\\GUI\\Deliverables/world-wide-web.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ConnectToWebsite.setIcon(icon6)
        self.ConnectToWebsite.setIconSize(QtCore.QSize(20, 20))
        self.ConnectToWebsite.setObjectName("ConnectToWebsite")
        self.ExportButton = QtWidgets.QPushButton(self.TaskBar)
        self.ExportButton.setGeometry(QtCore.QRect(850, 10, 141, 31))
        self.ExportButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 15px;\n"
"background-color:transparent;\n"
"font-weight:800;")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("D:\\College\\Third year\\First Term\\DSP\\Tasks\\Task 1\\Signal-Viewer\\GUI\\Deliverables/share (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExportButton.setIcon(icon7)
        self.ExportButton.setIconSize(QtCore.QSize(20, 20))
        self.ExportButton.setObjectName("ExportButton")
        self.Separator = QtWidgets.QFrame(self.centralwidget)
        self.Separator.setGeometry(QtCore.QRect(290, 450, 1061, 20))
        self.Separator.setStyleSheet("color: rgb(255, 255, 255);")
        self.Separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.Separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Separator.setObjectName("separator")

        #Channel 1 controls
        self.PlayChannel1 = QtWidgets.QPushButton(self.centralwidget)
        self.PlayChannel1.setGeometry(QtCore.QRect(300, 400, 31, 31))
        self.PlayChannel1.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 15px;\n"
"background-color:rgb(24,24,24);\n"
"font-weight:800;\n"
"border-radius: 15px;")
        self.PlayChannel1.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Deliverables/play-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayChannel1.setIcon(icon8)
        self.PlayChannel1.setIconSize(QtCore.QSize(25, 25))
        self.PlayChannel1.setObjectName("PlayChannel1")

        self.PauseChannel1 = QtWidgets.QPushButton(self.centralwidget)
        self.PauseChannel1.setGeometry(QtCore.QRect(340, 400, 31, 31))
        self.PauseChannel1.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 15px;\n"
"background-color:rgb(24,24,24);\n"
"font-weight:800;\n"
"border-radius: 15px;")
        self.PauseChannel1.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("Deliverables/video-pause-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PauseChannel1.setIcon(icon9)
        self.PauseChannel1.setIconSize(QtCore.QSize(25, 25))
        self.PauseChannel1.setObjectName("PauseChannel1")

        self.horizontalSliderChannel1 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderChannel1.setGeometry(QtCore.QRect(390, 410, 611, 16))
        self.horizontalSliderChannel1.setStyleSheet("QSlider::groove:horizontal {\n"
"    height: 5px;\n"
"    background: white;  \n"
"    border-radius: 3px;    \n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #000000;  \n"
"    border: 1px solid #333333;\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    border-radius: 6px;    \n"
"    margin: -4px 0;       \n"
"}\n"
"")
        self.horizontalSliderChannel1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderChannel1.setObjectName("horizontalSliderChannel1")
        self.verticalSliderChannel1 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSliderChannel1.setGeometry(QtCore.QRect(1050, 110, 16, 261))
        self.verticalSliderChannel1.setStyleSheet("QSlider::groove:vertical {\n"
"    width: 6px;\n"
"    background: white;  \n"
"    border-radius: 3px;   \n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background: #000000;   \n"
"    border: 1px solid #333333;\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    border-radius: 5px;    \n"
"    margin: 0 -4px;       \n"
"}\n"
"")
        self.verticalSliderChannel1.setOrientation(QtCore.Qt.Vertical)
        self.verticalSliderChannel1.setObjectName("verticalSliderChannel1")
        self.LinkChannels = QtWidgets.QPushButton(self.centralwidget)
        self.LinkChannels.setGeometry(QtCore.QRect(940, 60, 131, 31))
        self.LinkChannels.setStyleSheet("background-color: rgb(24, 24, 24);\n"
"color: rgb(255, 255, 255);\n"
"border: 1px;\n"
"border-radius: 15px;\n"
"font-weight:800;")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("D:\\College\\Third year\\First Term\\DSP\\Tasks\\Task 1\\Signal-Viewer\\GUI\\Deliverables/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LinkChannels.setIcon(icon10)
        self.LinkChannels.setObjectName("LinkChannels")

        #Channel 2 controls
        self.verticalSliderChannel2 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSliderChannel2.setGeometry(QtCore.QRect(1050, 510, 16, 261))
        self.verticalSliderChannel2.setStyleSheet("QSlider::groove:vertical {\n"
"    width: 6px;\n"
"    background: white;  \n"
"    border-radius: 3px;   \n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background: #000000;   \n"
"    border: 1px solid #333333;\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    border-radius: 5px;    \n"
"    margin: 0 -4px;       \n"
"}\n"
"")
        self.verticalSliderChannel2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSliderChannel2.setObjectName("verticalSliderChannel2")
        self.horizontalSliderChannel2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderChannel2.setGeometry(QtCore.QRect(390, 810, 611, 16))
        self.horizontalSliderChannel2.setStyleSheet("QSlider::groove:horizontal {\n"
"    height: 5px;\n"
"    background: white;  \n"
"    border-radius: 3px;    \n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #000000;  \n"
"    border: 1px solid #333333;\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    border-radius: 6px;    \n"
"    margin: -4px 0;       \n"
"}\n"
"")
        self.horizontalSliderChannel2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderChannel2.setObjectName("horizontalSliderChannel2")
        self.PauseChannel2 = QtWidgets.QPushButton(self.centralwidget)
        self.PauseChannel2.setGeometry(QtCore.QRect(340, 800, 31, 31))
        self.PauseChannel2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 15px;\n"
"background-color:rgb(24,24,24);\n"
"font-weight:800;\n"
"border-radius: 15px;")
        self.PauseChannel2.setText("")
        self.PauseChannel2.setIcon(icon9)
        self.PauseChannel2.setIconSize(QtCore.QSize(25, 25))
        self.PauseChannel2.setObjectName("PauseChannel2")
        self.PlayChannel2 = QtWidgets.QPushButton(self.centralwidget)
        self.PlayChannel2.setGeometry(QtCore.QRect(300, 800, 31, 31))
        self.PlayChannel2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font-size: 15px;\n"
"background-color:rgb(24,24,24);\n"
"font-weight:800;\n"
"border-radius: 15px;")
        self.PlayChannel2.setText("")
        self.PlayChannel2.setIcon(icon8)
        self.PlayChannel2.setIconSize(QtCore.QSize(25, 25))
        self.PlayChannel2.setObjectName("PlayChannel2")
        
        
        self.Channel1Viewer.raise_()
        self.Channel1Editor.raise_()
        self.Channel2Viewer.raise_()
        self.TaskBar.raise_()
        self.Separator.raise_()
        self.PlayChannel1.raise_()
        self.PauseChannel1.raise_()
        self.horizontalSliderChannel1.raise_()
        self.verticalSliderChannel1.raise_()
        self.LinkChannels.raise_()
        self.verticalSliderChannel2.raise_()
        self.horizontalSliderChannel2.raise_()
        self.PauseChannel2.raise_()
        self.PlayChannel2.raise_()
        self.Channel2Editor.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.UploadButton.setText(_translate("MainWindow", "Upload File"))
        self.ConnectToWebsite.setText(_translate("MainWindow", "Connect to website"))
        self.ExportButton.setText(_translate("MainWindow", "Export to PDF"))
        self.LinkChannels.setText(_translate("MainWindow", " Link channels"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
