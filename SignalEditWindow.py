from PyQt5 import QtWidgets, QtGui, QtCore

class SignalEditor(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height, id):
        super(SignalEditor, self).__init__(parent)
        self.ID=id
        self.setMinimumSize(231, 300)
        # Set geometry and style of SignalEditor window
        self.setGeometry(QtCore.QRect(x, y, width, height))
        self.setStyleSheet("background-color: rgb(24, 24, 24);")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        _translate = QtCore.QCoreApplication.translate

        
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
        self.SignalComboBox = QtWidgets.QComboBox(self.InnerSignalWindow)
        self.SignalComboBox.setGeometry(QtCore.QRect(30, 20, 150, 31))
        self.SignalComboBox.setStyleSheet("""
            QComboBox {
                color: rgb(255, 255, 255);
                font-size: 18px;
                background-color: rgb(24, 24, 24);
                padding-left: 15px;
                border: 1px solid transparent;
                border-radius: 15px; /* Rounded corners */
            }
            
            QComboBox QAbstractItemView {
                background-color: #444444;    /* Dropdown list background */
                color: #ffffff;               /* Dropdown list text color */
                selection-background-color: #555555;  /* Highlight background */
                selection-color: #FF5757;     /* Highlighted text color */
            }

            /* Remove the default arrow */
            QComboBox::drop-down {
                margin-right: 10px;
                border-top-right-radius: 15px; /* Apply radius to the top-right */
                border-bottom-right-radius: 15px; /* Apply radius to the bottom-right */
            }

            /* Customize the arrow (triangle) */
            QComboBox::down-arrow {
                image: url(Deliverables/down-arrow.png); /* Optional: use a custom image for the arrow */
                width: 10px;
                height: 10px;
                margin-right: 10px; /* Moves the arrow more to the right */
            }
        """)
        self.SignalComboBox.setEditable(False)  # Set to True if you want the user to be able to type in the box
        
        
        self.renameTextField = QtWidgets.QLineEdit(self.InnerSignalWindow)
        self.renameTextField.setGeometry(QtCore.QRect(30, 70, 150, 40))
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
        self.ColorButton.setGeometry(QtCore.QRect(40, 130, 131, 40))
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
        self.showHideCheckbox = QtWidgets.QCheckBox(self.InnerSignalWindow)
        self.showHideCheckbox.setGeometry(QtCore.QRect(20, 245, 81, 20))
        self.showHideCheckbox.setStyleSheet("color: rgb(255, 255, 255);")
        self.showHideCheckbox.setText(_translate("MainWindow", "Show/Hide"))

        # Channel 2 Checkbox
        self.moveSignal2anotherGraph = QtWidgets.QPushButton(self.InnerSignalWindow)
        self.moveSignal2anotherGraph.setGeometry(QtCore.QRect(110, 245, 81, 20))
        self.moveSignal2anotherGraph.setStyleSheet("color: rgb(255, 255, 255);")
        self.moveSignal2anotherGraph.setText(_translate("MainWindow", "move signal"))

        self.nonpolarButton = QtWidgets.QPushButton(self.InnerSignalWindow)
        self.nonpolarButton.setGeometry(QtCore.QRect(40, 190, 131, 41))
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
