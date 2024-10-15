from PyQt5 import QtWidgets, QtGui, QtCore

class SignalEditor(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height, label_text, id):
        super(SignalEditor, self).__init__(parent)
        self.ID=id
        self.setMinimumSize(231, 350)
        # Set geometry and style of SignalEditor window
        self.setGeometry(QtCore.QRect(x, y, width, height))
        self.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        _translate = QtCore.QCoreApplication.translate

        rename_icon = QtGui.QIcon("Deliverables/rename.png")
        color_icon = QtGui.QIcon("Deliverables/color-wheel.png")
        
        # Inner window setup
        self.InnerSignalWindow = QtWidgets.QFrame(self)
        self.InnerSignalWindow.setGeometry(QtCore.QRect(10, 10, width - 20, height - 20))
        self.InnerSignalWindow.setStyleSheet(
            "border-radius: 20px;\n"
            "background-color: rgb(42, 42, 42);"
        )
        self.InnerSignalWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.InnerSignalWindow.setFrameShadow(QtWidgets.QFrame.Raised)

        # Label
        self.SignalLabel = QtWidgets.QLabel(self.InnerSignalWindow)
        self.SignalLabel.setGeometry(QtCore.QRect(30, 20, 150, 31))
        self.SignalLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "font-size: 18px")
        self.SignalLabel.setText(label_text)
        self.SignalLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.renameTextField = QtWidgets.QLineEdit(self.InnerSignalWindow)
        self.renameTextField.setGeometry(QtCore.QRect(30, 80, 150, 40))
        self.renameTextField.setPlaceholderText("Change name")
        self.renameTextField.setStyleSheet(
            "background-color: rgb(24, 24, 24);\n"
            "color: rgb(255, 255, 255);\n"
            "border: 1px solid transparent;\n"  # Use 'solid' for proper border styling
            "border-radius: 20px;\n"
            "padding-left: 10px;\n"
        )

        palette = self.renameTextField.palette()
        palette.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor(100, 100, 100))  # Set the placeholder text color
        self.renameTextField.setPalette(palette)
        
        # Color Button
        self.ColorButton = QtWidgets.QPushButton(self.InnerSignalWindow)
        self.ColorButton.setGeometry(QtCore.QRect(35, 140, 131, 40))
        self.ColorButton.setStyleSheet(
            "background-color: rgb(24, 24, 24);\n"
            "color: rgb(255, 255, 255);\n"
            "border: 1px;\n"
            "border-radius: 20px;\n"
            "font-weight:800;"
        )
        self.ColorButton.setIcon(color_icon)
        self.ColorButton.setText(_translate("MainWindow","Change Color"))

        # Channel 1 Checkbox
        self.channel1Checkbox = QtWidgets.QCheckBox(self.InnerSignalWindow)
        self.channel1Checkbox.setGeometry(QtCore.QRect(20, 280, 81, 20))
        self.channel1Checkbox.setStyleSheet("color: rgb(255, 255, 255);")
        self.channel1Checkbox.setText(_translate("MainWindow","Channel 1"))
        
        # Channel 2 Checkbox
        self.channel2Checkbox = QtWidgets.QCheckBox(self.InnerSignalWindow)
        self.channel2Checkbox.setGeometry(QtCore.QRect(110, 280, 81, 20))
        self.channel2Checkbox.setStyleSheet("color: rgb(255, 255, 255);")
        self.channel2Checkbox.setText(_translate("MainWindow","Channel 2"))

        self.nonpolarButton = QtWidgets.QPushButton(self.InnerSignalWindow)
        self.nonpolarButton.setGeometry(QtCore.QRect(35, 200, 131, 41))
        self.nonpolarButton.setStyleSheet("background-color: rgb(24, 24, 24);\n"
        "color: rgb(255, 255, 255);\n"
        "border: 1px;\n"
        "border-radius: 20px;\n"
        "font-weight:800;")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("Deliverables/nonpolar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nonpolarButton.setIcon(icon12)
        self.nonpolarButton.setObjectName("nonpolarButton")
        self.nonpolarButton.setText(_translate("MainWindow","Show in Polar"))

    def getCheckBox(self,ch1=True):
        if ch1:
            return self.channel1Checkbox
        else:
            return self.channel1Checkbox
    
        
