import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt  # alignment

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pyautogui
import pyscreenshot as ImageGrab
from PIL import Image

screen_width, screen_height = pyautogui.size()


def take_snapshot(channel_number):
    if channel_number == 1:
        bbox = (380, 160, 1500, 535)
        # signal_name = signal_one_name
    elif channel_number == 2:
        bbox = (380, 500, 1500, 1060)
        # signal_name = signal_two_name
    else:
        bbox = (380, 160, 1500, 1070)

    # snapshot = pyautogui.screenshot()
    # snapshot_path = "Snapshots/snapshot.png"
    # snapshot.save(snapshot_path)

    snapshot = ImageGrab.grab(bbox=bbox)
    snapshot.show()
    snapshot_path = "Snapshots/snapshot.png"
    snapshot.save(snapshot_path)
    pdf = canvas.Canvas("Reports/example.pdf", pagesize=A4)
    pdf.setTitle("Sample PDF")
    # pdf.drawString(200, 800, "Hello, user!")
    pdf.drawImage(snapshot_path, 70, 500, 350, 150)
    pdf.save()


class MainWindow(QMainWindow):  # inherits from QMainWindow
    def __init__(self):   # constructor
        super().__init__()   # calls parent init to ensure proper initialization
        self.setWindowTitle("BIOSIGNAL")
        self.setGeometry(0, 0, 1860, 950)
        self.setWindowIcon(QIcon("images/app icon.png"))
        self.initUI()

    def initUI(self):
        menu_bar_label = QLabel(self)
        menu_bar_label.setGeometry(0, 0, 1860, 55)
        menu_bar_label.setStyleSheet("background-color: #f0f0f0;")

        import_button = QPushButton("Imp", self)
        import_button.setGeometry(5, 2, 50, 50)
        import_button.setStyleSheet("background-color: #fafafa")
        import_button.clicked.connect(self.import_signal)
        # snapshot_button.setIcon(QIcon("import_icon.png"))

        snapshot_button = QPushButton("1", self)
        snapshot_button.setGeometry(60, 2, 50, 50)
        snapshot_button.setStyleSheet("background-color: #fafafa")
        snapshot_button.clicked.connect(lambda: take_snapshot(1))
        # snapshot_button.setIcon(QIcon("snapshot_icon.png"))

        # link_channels_button = QPushButton("Link Channels ", self)
        # link_channels_button.setFont(QFont("Garet", 8))
        # link_channels_button.setGeometry(115, 2, 200, 50)
        # link_channels_button.setStyleSheet("background-color: #fafafa")
        # link_channels_button.setStyleSheet("color:#3f446f;"
        #                                   "background-color:white;"
        #                                   "font-weight:bold;")
        # link_channels_button.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # label.setAlignment(Qt.AlignLeft)
        # label.setAlignment(Qt.AlignVCenter)  # vertical alignment (default)
        # label.setAlignment(Qt.AlignCenter)  # center vertically & horizontally

        snapshot_two_button = QPushButton("2", self)
        snapshot_two_button.setGeometry(320, 2, 50, 50)
        snapshot_two_button.setStyleSheet("background-color: #fafafa")
        snapshot_two_button.clicked.connect(lambda: take_snapshot(2))
        # snapshot_button.setIcon(QIcon("snapshot_icon.png"))

        left_section_label = QLabel(self)
        left_section_label.setGeometry(15, 70, 300, 850)
        left_section_label.setStyleSheet("background-color: #fafafa;")

        middle_section_label = QLabel(self)
        middle_section_label.setGeometry(330, 70, 1200, 850)
        middle_section_label.setStyleSheet("background-color: #fafafa;")

        right_section_label = QLabel(self)
        right_section_label.setGeometry(1545, 70, 300, 850)
        right_section_label.setStyleSheet("background-color: #fafafa;")

        channel_one_label = QLabel(self)
        channel_one_label.setGeometry(380, 120, 1100, 350)
        channel_one_label.setStyleSheet("background-color: #f5f5f5;"
                                        "border: 2px solid #212434")

        channel_two_label = QLabel(self)
        channel_two_label.setGeometry(380, 520, 1100, 350)
        # channel_two_label.setStyleSheet("background-color: #f5f5f5;"
        #                                 "border: 2px solid #212434")
        channel_two_label.setStyleSheet("background-color: grey;"
                                        "border: 2px solid #212434")

        import_icon = QPixmap("import_icon.png")
        # link_channels_button.setPixmap(import_icon)
        # link_channels_button.setScaledContents(True)

        self.signal_one_label = QLineEdit(self)
        self.signal_one_label.setGeometry(100, 100, 200, 40)
        self.signal_one_label.setStyleSheet("font-size: 20px;"
                                            "font-family: Garet;")
        signal_one_button = QPushButton("Update Label", self)
        signal_one_button.setGeometry(100, 200, 200, 50)
        signal_one_button.clicked.connect(self.update_label)

    def update_label(self):
        signal_one_name = self.signal_one_label.text()
        print(f"Clicked {signal_one_name}")



    def import_signal(self):
        pass




def main():
    app = QApplication(sys.argv)  # create new app object
    window = MainWindow()  # create new window object
    window.show()
    sys.exit(app.exec_())  # app.exec_() waits for user to close window


if __name__ == "__main__":  # script is being run directly not imported
    main()
