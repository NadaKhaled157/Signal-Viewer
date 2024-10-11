from PyQt5 import QtWidgets, QtGui, QtCore

class SignalEditor(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height, label_text):
        super().__init__(parent)
        
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
        self.SignalLabel.setGeometry(QtCore.QRect(70, 10, 91, 31))
        self.SignalLabel.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "font-size: 18px")
        self.SignalLabel.setText(label_text)
        
        # Rename Button
        self.RenameButton = QtWidgets.QPushButton(self.InnerSignalWindow)
        self.RenameButton.setGeometry(QtCore.QRect(30, 70, 131, 31))
        self.RenameButton.setStyleSheet(
            "background-color: rgb(24, 24, 24);\n"
            "color: rgb(255, 255, 255);\n"
            "border: 1px;\n"
            "border-radius: 15px;\n"
            "font-weight:800;"
        )
        self.RenameButton.setIcon(rename_icon)
        self.RenameButton.setText(_translate("MainWindow","Rename"))
        
        # Color Button
        self.ColorButton = QtWidgets.QPushButton(self.InnerSignalWindow)
        self.ColorButton.setGeometry(QtCore.QRect(30, 120, 131, 31))
        self.ColorButton.setStyleSheet(
            "background-color: rgb(24, 24, 24);\n"
            "color: rgb(255, 255, 255);\n"
            "border: 1px;\n"
            "border-radius: 15px;\n"
            "font-weight:800;"
        )
        self.ColorButton.setIcon(color_icon)
        self.ColorButton.setText(_translate("MainWindow","Change Color"))

        # Channel 1 Checkbox
        self.channel1Checkbox = QtWidgets.QCheckBox(self.InnerSignalWindow)
        self.channel1Checkbox.setGeometry(QtCore.QRect(20, 170, 81, 20))
        self.channel1Checkbox.setStyleSheet("color: rgb(255, 255, 255);")
        self.channel1Checkbox.setText(_translate("MainWindow","Channel 1"))
        
        # Channel 2 Checkbox
        self.channel2Checkbox = QtWidgets.QCheckBox(self.InnerSignalWindow)
        self.channel2Checkbox.setGeometry(QtCore.QRect(110, 170, 81, 20))
        self.channel2Checkbox.setStyleSheet("color: rgb(255, 255, 255);")
        self.channel2Checkbox.setText(_translate("MainWindow","Channel 2"))

