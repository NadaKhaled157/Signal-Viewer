from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

class ComboBoxDemo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.combo = QtWidgets.QComboBox(self)

        # Add items to the combo box
        self.combo.addItem("Item 1")
        self.combo.addItem("Item 2")
        self.combo.addItem("Item 3")

        # Customizing the appearance using style sheet
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: #333333;    /* Background color */
                color: #ffffff;               /* Text color */
                border: 1px solid #555555;    /* Border style */
            }
            QComboBox QAbstractItemView {
                background-color: #444444;    /* Dropdown list background */
                color: #ffffff;               /* Dropdown list text color */
                selection-background-color: #555555;  /* Highlight background */
                selection-color: #ffcc00;     /* Highlighted text color */
            }
            QComboBox::drop-down {
                background-color: #555555;    /* Dropdown button background color */
                width: 30px;                  /* Adjust width of the button */
                border-left: 1px solid #333333; /* Left border of dropdown */
            }
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
                image: url(../Deliverables/down_arrow.png);    /* Replace this with a colored arrow image */
            }
        """)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.combo)
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle("QComboBox Custom Arrow Example")
        self.resize(300, 100)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    demo = ComboBoxDemo()
    demo.show()
    app.exec_()
