from PyQt5 import QtCore, QtGui, QtWidgets

class ChannelEditor(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height, label_text):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(x, y, width, height))
        self.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        _translate = QtCore.QCoreApplication.translate

        zoom_in_icon = QtGui.QIcon()
        zoom_in_icon.addPixmap(QtGui.QPixmap("Deliverables\zoom-in (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        zoom_out_icon = QtGui.QIcon()
        zoom_out_icon.addPixmap(QtGui.QPixmap("Deliverables\zoom-out (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        rewind_icon = QtGui.QIcon()
        rewind_icon.addPixmap(QtGui.QPixmap("Deliverables/rewind.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        turtle_icon = QtGui.QPixmap("Deliverables/turtle (2).png")
        rabbit_icon = QtGui.QPixmap("Deliverables/rabbit (2).png")

        # Inner Window
        self.InnerWindow = QtWidgets.QFrame(self)
        self.InnerWindow.setGeometry(QtCore.QRect(10, 10, 241, 261))
        self.InnerWindow.setStyleSheet("border-radius: 20px;\nbackground-color: rgb(42, 42, 42);")
        self.InnerWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.InnerWindow.setFrameShadow(QtWidgets.QFrame.Raised)

        # Zoom Out Button
        self.zoomOutButton = QtWidgets.QPushButton(self.InnerWindow)
        self.zoomOutButton.setGeometry(QtCore.QRect(140, 80, 41, 41))
        self.zoomOutButton.setStyleSheet("background-color: rgb(24, 24, 24);\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "border: 1px;\n"
                                         "border-radius: 20px;\n"
                                         "font-weight:800;")
        self.zoomOutButton.setText("")
        self.zoomOutButton.setIcon(zoom_out_icon)
        self.zoomOutButton.setIconSize(QtCore.QSize(24, 24))

        # Rewind Button
        self.RewindButton = QtWidgets.QPushButton(self.InnerWindow)
        self.RewindButton.setGeometry(QtCore.QRect(50, 140, 141, 31))
        self.RewindButton.setStyleSheet("background-color: rgb(24, 24, 24);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border: 1px;\n"
                                        "border-radius: 15px;\n"
                                        "font-weight:800;")
        self.RewindButton.setIcon(rewind_icon)
        self.RewindButton.setText(_translate("MainWindow", " Rewind"))
        
        

        # Zoom In Button
        self.zoomInButton = QtWidgets.QPushButton(self.InnerWindow)
        self.zoomInButton.setGeometry(QtCore.QRect(60, 80, 41, 41))
        self.zoomInButton.setStyleSheet("background-color: rgb(24, 24, 24);\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "border: 1px;\n"
                                        "border-radius: 20px;\n"
                                        "font-weight:800;")
        self.zoomInButton.setText("")
        self.zoomInButton.setIcon(zoom_in_icon)
        self.zoomInButton.setIconSize(QtCore.QSize(24, 24))

        # Channel Label
        self.ChannelLabel = QtWidgets.QLabel(self.InnerWindow)
        self.ChannelLabel.setGeometry(QtCore.QRect(80, 10, 91, 31))
        self.ChannelLabel.setStyleSheet("color:white;\nfont-size: 18px")
        self.ChannelLabel.setText(label_text)

        # Rabbit Icon
        self.rabbitLabel = QtWidgets.QLabel(self.InnerWindow)
        self.rabbitLabel.setGeometry(QtCore.QRect(200, 180, 31, 41))
        self.rabbitLabel.setPixmap(rabbit_icon)

        # Speed Slider
        self.SpeedSlider = QtWidgets.QSlider(self.InnerWindow)
        self.SpeedSlider.setGeometry(QtCore.QRect(60, 200, 131, 16))
        self.SpeedSlider.setStyleSheet("QSlider::groove:horizontal {\n"
                                       "    height: 5px;\n"
                                       "    background: white;  \n"
                                       "    border-radius: 6px;    \n"
                                       "}\n"
                                       "\n"
                                       "QSlider::handle:horizontal { \n"
                                       "    background-color: rgb(0, 170, 255);\n"
                                       "    border: 1px solid #333333;\n"
                                       "    width: 10px;\n"
                                       "    height: 10px;\n"
                                       "    border-radius: 6px;    \n"
                                       "    margin: -4px 0;       \n"
                                       "}")
        self.SpeedSlider.setOrientation(QtCore.Qt.Horizontal)

        # Turtle Icon
        self.turtleLabel = QtWidgets.QLabel(self.InnerWindow)
        self.turtleLabel.setGeometry(QtCore.QRect(20, 180, 31, 51))
        self.turtleLabel.setPixmap(turtle_icon)

# Usage example for Channel1Editor and Channel2Editor
# icon_zoom_in = QtGui.QIcon()
# icon_zoom_in.addPixmap(QtGui.QPixmap("path/to/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
# icon_zoom_out = QtGui.QIcon()
# icon_zoom_out.addPixmap(QtGui.QPixmap("path/to/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
# icon_rewind = QtGui.QIcon()
# icon_rewind.addPixmap(QtGui.QPixmap("path/to/rewind-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
# icon_turtle = QtGui.QPixmap("path/to/turtle.png")
# icon_rabbit = QtGui.QPixmap("path/to/rabbit.png")

# self.Channel1Editor = ChannelEditor(self.centralwidget, 1090, 100, 261, 281, "Channel 1", icon_zoom_in, icon_zoom_out, icon_rewind, icon_turtle, icon_rabbit)
# self.Channel2Editor = ChannelEditor(self.centralwidget, 1090, 400, 261, 281, "Channel 2", icon_zoom_in, icon_zoom_out, icon_rewind, icon_turtle, icon_rabbit)
