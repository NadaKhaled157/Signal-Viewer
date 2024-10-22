from PyQt5.QtWidgets import  QColorDialog
from ChannelEditor import ChannelEditor
from SignalEditWindow import SignalEditor
from main import *
from PolarSignal import PolarWindow
from LiveSignal import DataFetcher
from ExportToPdf import ExportToPdf, save_image
from GlueOptions import GlueOptions
import time
import threading
class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):

        # Window Setup
        app_icon = QtGui.QIcon('Deliverables/app icon.png')
        MainWindow.setWindowIcon(app_icon)
        MainWindow.setObjectName("Signal Viewer")
        MainWindow.setFixedSize(1379, 870)
        MainWindow.setMouseTracking(False)
        MainWindow.setStyleSheet("\n"
                                 "background-color: rgb(42, 42, 42);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.signalEditingWindows = []
        self.signals = [];
        self.signalID = 0;
        self.signalEditorID = 0;
        self.isSyncEnabled = False

        # LIVE SIGNAL VARIABLES
        self.thread = None
        self.fetch_subscriber_count = DataFetcher()
        self.fetch_subscriber_count.live_signal.connect(self.update_count)
        self.timestamps = []
        self.subscriber_counts = []
        self.start_time = time.time()

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
        # Channel 2 controls
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

        # Channel Viewer Setup
        self.Channel1Viewer = SignalCine(self.centralwidget, 290, 100, 731, 281, self.horizontalSliderChannel1,
                                         self.verticalSliderChannel1)
        self.Channel2Viewer = SignalCine(self.centralwidget, 290, 500, 731, 281, self.horizontalSliderChannel2,
                                         self.verticalSliderChannel2)

        self.Channel1Editor = ChannelEditor(self.centralwidget, 1090, 100, 261, 281, "Channel 1", self.Channel1Viewer)
        self.Channel2Editor = ChannelEditor(self.centralwidget, 1090, 500, 261, 281, "Channel 2", self.Channel2Viewer)

        # signal controls
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 60, 271, 800))
        self.scrollArea.setWidgetResizable(True)  # Ensure the scroll area resizes automatically
        self.scrollArea.setStyleSheet("background-color: rgb(42, 42, 42); border:0px;")
        scrollbar = QScrollBar()
        scrollbar.setStyleSheet("""
        QScrollBar:vertical {
            border: 1px solid #999999;
            background: #f9f9f9;
            width: 12px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #555555;
            min-height: 20px;
        }
    """)
        self.scrollArea.setVerticalScrollBar(scrollbar)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # self.Signal1EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 1")
        # self.Signal2EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 2")
        # self.Signal3EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 3")
        # self.Signal4EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 4")
        # self.Signal5EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 5")

        # # Add them to the layout
        # self.verticalLayout.addWidget(self.Signal1EditingWindow)
        # self.verticalLayout.addWidget(self.Signal2EditingWindow)
        # self.verticalLayout.addWidget(self.Signal3EditingWindow)
        # self.verticalLayout.addWidget(self.Signal4EditingWindow)
        # self.verticalLayout.addWidget(self.Signal5EditingWindow)

        # Taskbar Setup
        self.TaskBar = QtWidgets.QFrame(self.centralwidget)
        self.TaskBar.setGeometry(QtCore.QRect(-1, 0, 1381, 51))
        self.TaskBar.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.TaskBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TaskBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TaskBar.setObjectName("TaskBar")
        self.UploadButton = QtWidgets.QPushButton(self.TaskBar)
        self.UploadButton.setGeometry(QtCore.QRect(350, 10, 121, 28))
        self.UploadButton.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font-size: 15px;\n"
                                        "background-color:transparent;\n"
                                        "font-weight:800;")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Deliverables/downloads.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UploadButton.setIcon(icon5)
        self.UploadButton.setIconSize(QtCore.QSize(20, 20))
        self.UploadButton.setObjectName("UploadButton")
        self.UploadButton.clicked.connect(self.createSignalEditor)

        # LIVE SIGNAL BUTTONS

        self.ConnectToWebsite = QtWidgets.QPushButton(self.TaskBar)
        self.ConnectToWebsite.setGeometry(QtCore.QRect(500, 10, 171, 28))
        self.ConnectToWebsite.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "font-size: 15px;\n"
                                            "background-color:transparent;\n"
                                            "font-weight:800;")
        self.ConnectToWebsite.clicked.connect(lambda: self.live_connection('connect'))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Deliverables/world-wide-web.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ConnectToWebsite.setIcon(icon6)

        self.DisconnectFromWebsite = QtWidgets.QPushButton(self.TaskBar)
        self.DisconnectFromWebsite.setGeometry(QtCore.QRect(670, 10, 171, 28))
        self.DisconnectFromWebsite.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                 "font-size: 15px;\n"
                                                 "background-color:transparent;\n"
                                                 "font-weight:800;")
        self.DisconnectFromWebsite.clicked.connect(lambda: self.live_connection('disconnect'))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(
            "Deliverables/disconnect_icon.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DisconnectFromWebsite.setIcon(icon12)
        #

        self.DisconnectFromWebsite.setIconSize(QtCore.QSize(20, 20))
        self.DisconnectFromWebsite.setObjectName("DisconnectFromWebsite")
        self.ExportButton = QtWidgets.QPushButton(self.TaskBar)
        self.ExportButton.setGeometry(QtCore.QRect(860, 10, 141, 31))
        self.ExportButton.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font-size: 15px;\n"
                                        "background-color:transparent;\n"
                                        "font-weight:800;")

        self.ExportButton.clicked.connect(
            lambda: self.save_report(MainWindow.toBeGluedSignals[0], MainWindow.toBeGluedSignals[1],
            MainWindow.glue_window.glued_y, MainWindow.glue_window.glued_lists, MainWindow.glue_window.glued_count))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Deliverables/share (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExportButton.setIcon(icon7)
        self.ExportButton.setIconSize(QtCore.QSize(20, 20))
        self.ExportButton.setObjectName("ExportButton")

        self.Separator = QtWidgets.QFrame(self.centralwidget)
        self.Separator.setGeometry(QtCore.QRect(290, 450, 750, 20))
        self.Separator.setStyleSheet("color: rgb(255, 255, 255);")
        self.Separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.Separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Separator.setObjectName("separator")

        # Channel 1 controls
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
        self.PlayChannel1.clicked.connect(self.Channel1Viewer.playSignal)

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
        self.PauseChannel1.clicked.connect(self.Channel1Viewer.pauseSignal)

        self.LinkChannels = QtWidgets.QPushButton(self.centralwidget)
        self.LinkChannels.setGeometry(QtCore.QRect(1080, 425, 141, 41))
        self.LinkChannels.setStyleSheet("background-color: rgb(24, 24, 24);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border: 1px;\n"
                                        "border-radius: 20px;\n"
                                        "font-weight:800;")
        self.icon10 = QtGui.QIcon()
        self.icon10.addPixmap(QtGui.QPixmap(
            "D:\\College\\Third year\\First Term\\DSP\\Tasks\\Task 1\\Signal-Viewer\\GUI\\Deliverables/link.png"),
                              QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LinkChannels.setIcon(self.icon10)
        self.LinkChannels.setCheckable(True)
        self.LinkChannels.setObjectName("LinkChannels")
        self.LinkChannels.toggled.connect(self.linkTwoChannels)

        self.glueButton = QtWidgets.QPushButton(self.centralwidget)
        self.glueButton.setGeometry(QtCore.QRect(1225, 425, 131, 41))
        self.glueButton.setStyleSheet("background-color: rgb(24, 24, 24);\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "border: 1px;\n"
                                      "border-radius: 20px;\n"
                                      "font-weight:800;")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("Deliverables/glue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.glueButton.setIcon(icon11)
        self.glueButton.setObjectName("GlueButton")
        self.glueButton.clicked.connect(MainWindow.glue_options)

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
        self.PauseChannel2.clicked.connect(self.Channel2Viewer.pauseSignal)

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
        self.PlayChannel2.clicked.connect(self.Channel2Viewer.playSignal)

        self.Channel1Viewer.raise_()
        self.Channel1Editor.raise_()
        # self.Channel2Viewer.raise_()
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

    def temp_glue_function(self):
        print("iam the clicked that in the ui main window")

    def update_temp_rectangle(self):
        if hasattr(self, 'temp_frame'):
            self.temp_frame.setGeometry(QRect(self.begin, self.destination).normalized())
        else:
            self.temp_frame = QFrame(self)
            self.temp_frame.setGeometry(QRect(self.begin, self.destination).normalized())
            self.temp_frame.setStyleSheet("background-color: rgba(0, 0, 255, 50); border: 2px solid blue;")
            self.temp_frame.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Signal Viewer"))
        self.UploadButton.setText(_translate("MainWindow", "Upload File"))
        self.ConnectToWebsite.setText(_translate("MainWindow", "Connect to website"))
        self.DisconnectFromWebsite.setText(_translate("MainWindow", "Disconnect"))
        self.ExportButton.setText(_translate("MainWindow", "Export to PDF"))
        self.LinkChannels.setText(_translate("MainWindow", " Link channels"))
        self.glueButton.setText(_translate("MainWindow", "Combine"))

    def linkTwoChannels(self, checked):
        self.isSyncEnabled = checked
        if checked:
            # Button is toggled ON
            self.LinkChannels.setStyleSheet("background-color: green;\n"
                                            "color: white;\n"
                                            "border: 1px;\n"
                                            "border-radius: 20px;\n"
                                            "font-weight:800;")
            iconOn = QtGui.QIcon()
            iconOn.addPixmap(QtGui.QPixmap("Deliverables/unlink.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.LinkChannels.setIcon(iconOn)
            self.LinkChannels.setText("Unlink channels")
            self.Channel1Viewer.rewindSignal()
            self.Channel2Viewer.rewindSignal()

            self.Channel1Viewer.plot_graph.setXLink(self.Channel2Viewer.plot_graph)
            self.Channel1Viewer.plot_graph.setYLink(self.Channel2Viewer.plot_graph)

            # Try disconnecting signals safely
            try:

                self.Channel1Editor.RewindButton.clicked.disconnect()
                self.Channel2Editor.RewindButton.clicked.disconnect()
                self.Channel1Editor.SpeedSlider.valueChanged.disconnect()
                self.Channel2Editor.SpeedSlider.valueChanged.disconnect()
            except TypeError:
                print("Some signals were not connected before disconnecting")

            # Connect synchronized signals
            self.Channel1Editor.RewindButton.clicked.connect(self.wrappedRewind)
            self.Channel2Editor.RewindButton.clicked.connect(self.wrappedRewind)
            self.Channel1Editor.SpeedSlider.valueChanged.connect(self.syncSliders)
            self.Channel2Editor.SpeedSlider.valueChanged.connect(self.syncSliders)


        else:
            # Button is toggled OFF (revert to original state)
            self.LinkChannels.setStyleSheet("background-color: rgb(24, 24, 24);\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "border: 1px;\n"
                                            "border-radius: 20px;\n"
                                            "font-weight:800;")
            self.LinkChannels.setIcon(self.icon10)
            self.LinkChannels.setText("Link channels")
            self.Channel1Viewer.rewindSignal()
            self.Channel2Viewer.rewindSignal()

            self.Channel1Viewer.plot_graph.setXLink(self.Channel2Viewer.plot_graph)
            self.Channel1Viewer.plot_graph.setYLink(self.Channel2Viewer.plot_graph)

            # Try disconnecting signals safely
            try:

                self.Channel1Editor.RewindButton.clicked.disconnect()
                self.Channel2Editor.RewindButton.clicked.disconnect()
                self.Channel1Editor.SpeedSlider.valueChanged.disconnect()
                self.Channel2Editor.SpeedSlider.valueChanged.disconnect()
            except TypeError:
                print("Some signals were not connected before disconnecting")

            self.Channel1Editor.RewindButton.clicked.connect(self.Channel1Viewer.rewindSignal)
            self.Channel2Editor.RewindButton.clicked.connect(self.Channel2Viewer.rewindSignal)

            self.Channel1Editor.SpeedSlider.valueChanged.connect(self.Channel1Viewer.changeSpeed)
            self.Channel2Editor.SpeedSlider.valueChanged.connect(self.Channel2Viewer.changeSpeed)

    def wrappedRewind(self):
        self.Channel1Viewer.rewindSignal()
        self.Channel2Viewer.rewindSignal()

    def syncSliders(self, value):

        if self.isSyncEnabled:
            sender = self.sender()

            if sender == self.Channel1Editor.SpeedSlider:
                self.Channel2Editor.SpeedSlider.blockSignals(True)
                self.Channel2Editor.SpeedSlider.setValue(value)
                self.Channel2Editor.SpeedSlider.blockSignals(False)
            elif sender == self.Channel2Editor.SpeedSlider:
                self.Channel1Editor.SpeedSlider.blockSignals(True)
                self.Channel1Editor.SpeedSlider.setValue(value)
                self.Channel1Editor.SpeedSlider.blockSignals(False)
            # Call the wrappedChangeSpeed function to apply the new speed
            self.wrappedChangeSpeed(value)

    def wrappedChangeSpeed(self, value):

        # Apply the speed change to both viewers
        self.Channel1Viewer.changeSpeed(value)
        self.Channel2Viewer.changeSpeed(value)

    def createSignalEditor(self):

        signal = self.Channel1Viewer.uploadSignal()
        if signal is not None:
            self.signalID += 1
            self.signalEditorID += 1
            self.signals.append(signal)
            signalEditor = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 350, f"Signal {str(self.signalID)}",
                                        self.signalEditorID)
            self.verticalLayout.addWidget(signalEditor)
            self.signalEditingWindows.append(signalEditor)
            signalEditor.setVisible(True)
            self.scrollArea.update()
            # self.scrollArea.adjustSize()
            # self.scrollAreaWidgetContents.updateGeometry()
            # self.scrollArea.updateGeometry()
            # self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

        signalEditor.ColorButton.clicked.connect(lambda: self.changeColor(signalEditor.ID))
        signalEditor.renameTextField.returnPressed.connect(lambda: self.rename(signalEditor.ID))
        signalEditor.nonpolarButton.clicked.connect(
            lambda: self.show_polar_view(signal.x, signal.y, signal.name, signal.color))  # From Nada
        signalEditor.channel1Checkbox.setChecked(True)
        signalEditor.channel1Checkbox.stateChanged.connect(
            lambda state, s_id=signal.signalId: self.selectChannel1StateChanged(s_id, state))
        signalEditor.channel2Checkbox.stateChanged.connect(
            lambda state, s_id=signal.signalId: self.selectChannel2StateChanged(s_id, state))

    def get_checked_signal_id(self, channelViewer):
        signals_checked_id = []
        channelnum = 0
        if channelViewer == self.Channel1Viewer:
            channelnum = 1
        else:
            channelnum = 2
        for signalEditor in self.signalEditingWindows :
            if channelnum == 1 :
                if signalEditor.channel1Checkbox.isChecked():
                    signals_checked_id.append(signalEditor.ID)
            else:
                if signalEditor.channel2Checkbox.isChecked():
                    signals_checked_id.append(signalEditor.ID)
        return signals_checked_id
    def get_signal_by_id(self,id,channelViewer):
        for signal in channelViewer.signalsChannel :
            if signal.signalId == id:
                return signal

    def selectChannel1StateChanged(self, id, state):
        if state == Qt.Unchecked:  # ch 1 is unchecked
            for signal in self.Channel1Viewer.signalsChannel:
                if signal.signalId == id:
                    self.Channel1Viewer.plot_graph.removeItem(signal.line)  # remove from ch 1
                    signal.showSignal = False
                    break
        elif state == Qt.Checked:  # ch 1 is checked
            for signal in self.Channel1Viewer.signalsChannel:
                if signal.signalId == id and signal.line not in self.Channel1Viewer.plot_graph.listDataItems():
                    signal.line.setData(signal.time, signal.magnitude)  # reshow the signal
                    self.Channel1Viewer.plot_graph.addItem(signal.line)  # readd to the plot
                    signal.showSignal = True
                    break

    def selectChannel2StateChanged(self, id, state):
        signalRelated2Id = None
        if state == Qt.Checked:  # ch 2 is checked
            for signal in self.Channel2Viewer.signalsChannel:
                if signal.signalId == id and signal.line not in self.Channel2Viewer.plot_graph.listDataItems():  # then it was existed so we need to reshoe
                    signal.line.setData(signal.time, signal.magnitude)  # reshow the signal in Plot
                    signal.showSignal = True
                    self.Channel2Viewer.plot_graph.addItem(signal.line)
                    return
            for signal in self.Channel1Viewer.signalsChannel:  # here there is no id with that , so we need to create new signal object
                if signal.signalId == id:
                    signalRelated2Id = signal
                    break
            if signalRelated2Id is not None:
                signal = SignalObject(signalRelated2Id.x, signalRelated2Id.y, (self.Channel2Viewer).plot_graph,
                                      signalRelated2Id.color,
                                      signalRelated2Id.name, id)
                self.Channel2Viewer.plot_graph.addItem(signal.line)
                self.Channel2Viewer.signalsChannel.append(signal)
                self.signals.append(signal)
                signal.showSignal = True

                yMin, yMax = min(signalRelated2Id.y), max(signalRelated2Id.y)
                self.Channel2Viewer.plot_graph.plotItem.vb.setLimits(xMin=0, xMax=signalRelated2Id.x[-1], yMin=yMin,
                                                                     yMax=yMax)
                self.Channel2Viewer.playSignal()

        else:  # ch2 2 is unchecked
            for signal in self.Channel2Viewer.signalsChannel:
                if signal.signalId == id:
                    self.Channel2Viewer.plot_graph.removeItem(signal.line)  # remove from ch 2
                    signal.showSignal = False
                    break

    def rename(self, signalEditorId):
        signal = None
        entered_text = None
        for signal in self.Channel1Viewer.signalsChannel:
            if signal.signalId == signalEditorId:
                signalEditor = self.signalEditingWindows[signal.signalId - 1]
                entered_text = signalEditor.renameTextField.text()
                if entered_text.strip():
                    signal.label = entered_text
                    signalEditor.SignalLabel.setText(entered_text)
                    signal.rename_signal(entered_text)
                    break
        for signal in self.Channel2Viewer.signalsChannel:
            if signal.signalId == signalEditorId:
                signalEditor = self.signalEditingWindows[signal.signalId - 1]
                entered_text = signalEditor.renameTextField.text()
                if entered_text.strip():
                    signal.label = entered_text
                    signalEditor.SignalLabel.setText(entered_text)
                    signal.rename_signal(entered_text)
                    break

        # for i, plot_item in enumerate(signal.plot_widget.listDataItems()):
        #         if (plot_item.getData()[1] == signal.y[:len(plot_item.getData()[1])]).all():
        #                 if entered_text.strip():
        #                         self.Channel1Viewer.legend.removeItem(plot_item)
        #                         self.Channel1Viewer.legend.addItem(plot_item,signal.label)
        #                         break

    def changeColor(self, signalEditorID):
        color = QColorDialog.getColor()

        if color.isValid():
            signal = None
            # Apply the selected color to the signal
            for signal in self.Channel1Viewer.signalsChannel:
                if signal.signalId == signalEditorID:
                    signal.color = color
                    signal.change_color(color)
                    break
            for signal in self.Channel2Viewer.signalsChannel:
                if signal.signalId == signalEditorID:
                    signal.color = color
                    signal.change_color(color)
                    break

    # NADA'S ADDITION
    def show_polar_view(self, timestamps, signal_values, signal_label, signal_color):
        signal_window = PolarWindow(timestamps, signal_values, signal_label, signal_color)
        signal_window.show()

    def live_connection(self, status):
        if status == "connect":
            self.fetch_subscriber_count.connected = True
            self.thread = threading.Thread(target=self.fetch_subscriber_count.fetch_data)
            self.thread.start()
        else:
            self.fetch_subscriber_count.connected = False

    def update_count(self):
        # Change plot_widget_two to whatever it is called in the new UI

        subscriber_count = self.fetch_subscriber_count.subscriber_count
        elapsed_time = time.time() - self.start_time

        self.timestamps.append(elapsed_time)
        self.subscriber_counts.append(subscriber_count)

        self.Channel1Viewer.plot_graph.clear()  # not sure if this is necessary
        self.Channel1Viewer.plot_graph.plot(self.timestamps, self.subscriber_counts, pen=pg.mkPen(color='g', width=2),
                                            symbol='o',
                                            symbolBrush='w')

        # Set axis labels
        self.Channel1Viewer.plot_graph.setLabel('left', 'Subs Count')
        self.Channel1Viewer.plot_graph.setLabel('bottom', 'Time (sec)')

        # Set Y-axis range
        # if self.subscriber_counts:
        #         y_min = min(self.subscriber_counts) - 10
        #         y_max = max(self.subscriber_counts) + 10
        # self.Channel1Viewer.plot_graph.setYRange(y_min, y_max)
        # self.Channel1Viewer.plot_graph.setXRange(0, max(self.timestamps) + 5)

        # # Format x-axis to show time
        # self.Channel1Viewer.plot_graph.getAxis('bottom').setTicks(
        #         [[(t, time.strftime("%H:%M:%S", time.gmtime(t))) for t in self.timestamps]])
        #
        # # Format y-axis points
        # self.Channel1Viewer.plot_graph.getAxis('left').setTicks(
        #         [[(count, str(count)) for count in
        #           range(int(y_min), int(y_max) + 1, 5)]])  # every 5 subscribers

        # self.plot_widget_two.repaint() #I think this is useless

    # def export_to_pdf(self, signal_one_statistics, signal_two_statistics, glued_plot):
    #         pdf = ExportToPdf(signal_one_statistics, signal_two_statistics, glued_plot)
    def save_report(self, signal_one, signal_two, glued_signal_values, glued_lists, glued_count):
        print("Inside Save Report")
        # signal1, signal2 = self.gluedSignals[0], self.gluedSignals[1]
        pdf = ExportToPdf(signal_one.signalStatistics(), signal_two.signalStatistics(), glued_signal_values, glued_lists,
                          glued_count)