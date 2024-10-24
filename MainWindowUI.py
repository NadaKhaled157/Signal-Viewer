from PyQt5.QtWidgets import  QColorDialog, QMessageBox
from PyQt5.QtGui import QIcon
from ChannelEditor import ChannelEditor
from SignalEditWindow import SignalEditor
from main import *
from PolarSignal import PolarWindow
from LiveSignal import DataFetcher
from ExportToPdf import ExportToPdf
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
        self.signal_id = 0;
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

        self.signalEditor1 = SignalEditor(self.centralwidget, 50, 100, 231, 300,self.signalEditorID,)
        self.signalEditor2 = SignalEditor(self.centralwidget, 50, 500, 231, 300,self.signalEditorID)


        self.signalEditor1.ColorButton.clicked.connect(lambda: self.apply_controls("channel 1","color"))
        self.signalEditor1.renameTextField.returnPressed.connect(lambda: self.apply_controls("channel 1","rename"))
        self.signalEditor1.nonpolarButton.clicked.connect(
                lambda: self.apply_controls("channel 1","polar"))  # From Nada
        self.signalEditor1.channel1Checkbox.setChecked(True)
        self.signalEditor1.channel1Checkbox.stateChanged.connect(
            lambda state, s_id=self.signal_id: self.selectChannel1StateChanged(s_id, state))
        self.signalEditor1.channel2Checkbox.stateChanged.connect(
            lambda state, s_id=self.signal_id: self.selectChannel2StateChanged(s_id, state))
        
        self.signalEditor2.ColorButton.clicked.connect(lambda: self.apply_controls("channel 2","color"))
        self.signalEditor2.renameTextField.returnPressed.connect(lambda: self.apply_controls("channel 2","rename"))
        self.signalEditor2.nonpolarButton.clicked.connect(
            lambda: self.apply_controls("channel 2","polar"))  # From Nada
        self.signalEditor2.channel1Checkbox.setChecked(True)
        self.signalEditor2.channel1Checkbox.stateChanged.connect(
            lambda state, s_id=self.signal_id: self.selectChannel1StateChanged(s_id, state))
        self.signalEditor2.channel2Checkbox.stateChanged.connect(
            lambda state, s_id=self.signal_id: self.selectChannel2StateChanged(s_id, state))
    

        

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
        self.PlayChannel1.setGeometry(QtCore.QRect(320, 400, 35, 35))
        self.PlayChannel1.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font-size: 15px;\n"
                                        "background-color:rgb(24,24,24);\n"
                                        "font-weight:800;\n"
                                        "border-radius: 15px;\n")
        self.PlayChannel1.setText("")
        self.iconplay = QtGui.QIcon()
        self.iconplay.addPixmap(QtGui.QPixmap("Deliverables/play-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.iconpause = QtGui.QIcon()
        self.iconpause.addPixmap(QtGui.QPixmap("Deliverables/video-pause-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlayChannel1.setIcon(self.iconplay)
        self.PlayChannel1.setCheckable(True)
        self.PlayChannel1.setIconSize(QtCore.QSize(35, 35))
        self.PlayChannel1.setObjectName("PlayChannel1")
        self.PlayChannel1.toggled.connect(lambda checked: self.togglePlaySignal(checked, "channel 1"))


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


        self.PlayChannel2 = QtWidgets.QPushButton(self.centralwidget)
        self.PlayChannel2.setGeometry(QtCore.QRect(320, 800, 35, 35))
        self.PlayChannel2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                        "font-size: 15px;\n"
                                        "background-color:rgb(24,24,24);\n"
                                        "font-weight:800;\n"
                                        "border-radius: 15px;")
        self.PlayChannel2.setText("")
        self.PlayChannel2.setIcon(self.iconplay)
        self.PlayChannel2.setIconSize(QtCore.QSize(35, 35))
        self.PlayChannel2.setCheckable(True)
        self.PlayChannel2.setObjectName("PlayChannel2")
        self.PlayChannel2.toggled.connect(lambda checked: self.togglePlaySignal(checked,"channel 2"))

        self.Channel1Viewer.raise_()
        self.Channel1Editor.raise_()
        # self.Channel2Viewer.raise_()
        self.TaskBar.raise_()
        self.Separator.raise_()
        self.PlayChannel1.raise_()
        self.horizontalSliderChannel1.raise_()
        self.verticalSliderChannel1.raise_()
        self.LinkChannels.raise_()
        self.verticalSliderChannel2.raise_()
        self.horizontalSliderChannel2.raise_()
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

    def togglePlaySignal(self, checked, channel):

        if channel == "channel 1":
            if checked:
                self.PlayChannel1.setIcon(self.iconplay)
                self.Channel1Viewer.pauseSignal()
            else:
                self.PlayChannel1.setIcon(self.iconpause)
                self.Channel1Viewer.playSignal()

        elif channel == "channel 2":
            if checked:
                self.PlayChannel2.setIcon(self.iconplay)
                self.Channel2Viewer.pauseSignal()
            else:
                self.PlayChannel2.setIcon(self.iconpause)
                self.Channel2Viewer.playSignal()

        else:
            if checked:
                self.PlayChannel1.setIcon(self.iconplay)
                self.PlayChannel2.setIcon(self.iconplay)
                self.Channel1Viewer.pauseSignal()
                self.Channel2Viewer.pauseSignal()
            else:
                self.PlayChannel1.setIcon(self.iconpause)
                self.PlayChannel2.setIcon(self.iconpause)
                self.Channel1Viewer.playSignal()
                self.Channel2Viewer.playSignal()



    def linkTwoChannels(self, checked):
        self.isSyncEnabled = checked
        self.PlayChannel1.setIcon(self.iconpause)
        self.PlayChannel2.setIcon(self.iconpause)
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
                self.PlayChannel1.toggled.disconnect()
                self.PlayChannel2.toggled.disconnect()
                self.Channel1Editor.RewindButton.clicked.disconnect()
                self.Channel2Editor.RewindButton.clicked.disconnect()
                self.Channel1Editor.SpeedSlider.valueChanged.disconnect()
                self.Channel2Editor.SpeedSlider.valueChanged.disconnect()
            except TypeError:
                print("Some signals were not connected before disconnecting")

            # Connect synchronized signals
            self.PlayChannel1.toggled.connect(lambda checked: self.togglePlaySignal(checked,"both"))
            self.PlayChannel2.toggled.connect(lambda checked: self.togglePlaySignal(checked,"both"))
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

            self.Channel1Viewer.plot_graph.setXLink(None)
            self.Channel1Viewer.plot_graph.setYLink(None)

            # Try disconnecting signals safely
            try:
                self.PlayChannel1.toggled.disconnect()
                self.PlayChannel2.toggled.disconnect()
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

            self.PlayChannel1.toggled.connect(lambda checked: self.togglePlaySignal(checked,"channel 1"))
            self.PlayChannel2.toggled.connect(lambda checked: self.togglePlaySignal(checked,"channel 2"))

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


    def apply_controls(self, channel, control):
        # Get the currently selected item's index and associated signalId
        if channel == "channel 1":
            current_index = self.signalEditor1.SignalComboBox.currentIndex()

            if current_index == -1:  # No item selected
                return

            self.signal_id = self.signalEditor1.SignalComboBox.itemData(current_index)
            selected_signal_text = self.signalEditor1.SignalComboBox.currentText()
            print(f"Selected Item: {selected_signal_text}, Signal ID: {self.signal_id}")

            
            if control == "rename":
                self.rename(self.signal_id)

            elif control == "color":
                self.changeColor(self.signal_id)

            elif control == "polar":
                self.show_polar_view(self.signal_id)


        if channel == "channel 2":
            current_index = self.signalEditor2.SignalComboBox.currentIndex()

            if current_index == -1:  # No item selected
                return

            self.signal_id = self.signalEditor2.SignalComboBox.itemData(current_index)
            selected_signal_text = self.signalEditor2.SignalComboBox.currentText()

            print(f"Selected Item: {selected_signal_text}, Signal ID: {self.signal_id}")


    def createSignalEditor(self):

        signal = self.Channel1Viewer.uploadSignal()
        if signal is not None:
            self.signal_id += 1
            self.signalEditorID += 1
            self.signals.append(signal)
            self.PlayChannel1.setIcon(self.iconpause)

            new_signal_label = f"Signal {self.signal_id}"

            # Add the new signal to the combo box with its signalId as itemData
            self.signalEditor1.SignalComboBox.addItem(new_signal_label, self.signal_id)



            
            
            
        

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
                self.PlayChannel1.setIcon(self.iconplay)
                if signal.signalId == id:
                    self.Channel1Viewer.plot_graph.removeItem(signal.line)  # remove from ch 1
                    signal.showSignal = False
                    break
        elif state == Qt.Checked:  # ch 1 is checked
            self.PlayChannel1.setIcon(self.iconpause)
            for signal in self.Channel1Viewer.signalsChannel:
                if signal.signalId == id and signal.line not in self.Channel1Viewer.plot_graph.listDataItems():
                    signal.line.setData(signal.time, signal.magnitude)  # reshow the signal
                    self.Channel1Viewer.plot_graph.addItem(signal.line)  # readd to the plot
                    signal.showSignal = True
                    break

    def selectChannel2StateChanged(self, id, state):
        
        
        signalRelated2Id = None
        if state == Qt.Checked:  # ch 2 is checked
            self.PlayChannel2.setIcon(self.iconpause)
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
            self.PlayChannel2.setIcon(self.iconplay)
            for signal in self.Channel2Viewer.signalsChannel:
                if signal.signalId == id:
                    self.Channel2Viewer.plot_graph.removeItem(signal.line)  # remove from ch 2
                    signal.showSignal = False
                    break

    def rename(self, signalEditorId):
        entered_text = None
        print(signalEditorId)
        # Update Channel 1 signals
        for signal in self.Channel1Viewer.signalsChannel:
            if signal.signalId == signalEditorId:
                entered_text = self.signalEditor1.renameTextField.text()
                if entered_text.strip():
                    signal.name = entered_text

                    # Find the corresponding item in the ComboBox
                    for i in range(self.signalEditor1.SignalComboBox.count()):
                        if self.signalEditor1.SignalComboBox.itemData(i) == signal.signalId:
                            self.signalEditor1.SignalComboBox.setItemText(i, entered_text)
                            signal.rename_signal(entered_text)
                            break

        # Update Channel 2 signals
        for signal in self.Channel2Viewer.signalsChannel:
            if signal.signalId == signalEditorId:
                entered_text = self.signalEditor2.renameTextField.text()
                if entered_text.strip():
                    signal.label = entered_text

                    # Find the corresponding item in the ComboBox
                    for i in range(self.signalEditor2.SignalComboBox.count()):
                        if self.signalEditor2.SignalComboBox.itemData(i) == signal.signalId:
                            self.signalEditor2.SignalComboBox.setItemText(i, entered_text)
                            signal.rename_signal(entered_text)
                            break

    def changeColor(self,signalEditorID):
                color = QColorDialog.getColor()
                
                if color.isValid():
                        signal = None
                        # Apply the selected color to the signal
                        for signal in self.signals:
                               if signal.signalId == signalEditorID:
                                      signal.color = color
                                      signal.change_color(color)
                                      break

    def refillSignal (self, channel):
        if channel == "channel 1":
            self.signalEditor1.SignalComboBox.clear()
            for signal in self.Channel1Viewer.signalsChannel:
                self.signalEditor1.SignalComboBox.addItem(signal.name,self.signal_id)


    # NADA'S ADDITION
    def show_polar_view(self, signalID):
        print(signalID)
        for signal in self.signals:
            if signal.signalId == signalID:
                try:
                    signal_window = PolarWindow(signal.x, signal.y, signal.name, signal.color)
                    signal_window.show()
                except:
                    error_message = QMessageBox()
                    error_message.setWindowTitle("Error")
                    error_icon = QIcon("Deliverables/error_icon.png")
                    error_message.setWindowIcon(error_icon)
                    error_message.setText("An error occured. Please try again.")
                    error_message.setStandardButtons(QMessageBox.Ok)
                    error_message.exec_()

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