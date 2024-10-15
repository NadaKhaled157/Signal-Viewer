import sys
import time
import threading
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QIcon
import pyqtgraph as pg
from LiveSignal import DataFetcher


# import pandas as pd
# import pyautogui
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# import pyscreenshot as ImageGrab

# screen_width, screen_height = pyautogui.size()


# def take_snapshot(channel_number):  # IN PROGRESS
#     if channel_number == 1:
#         bbox = (380, 160, 1500, 535)
#         # signal_name = signal_one_name
#     elif channel_number == 2:
#         bbox = (380, 500, 1500, 1060)
#         # signal_name = signal_two_name
#     else:
#         bbox = (380, 160, 1500, 1070)
#     # snapshot = pyautogui.screenshot()
#     # snapshot_path = "Snapshots/snapshot.png"
#     # snapshot.save(snapshot_path)
#     snapshot = ImageGrab.grab(bbox=bbox)
#     snapshot.show()
#     snapshot_path = "Snapshots/snapshot.png"
#     snapshot.save(snapshot_path)
#     pdf = canvas.Canvas("Reports/example.pdf", pagesize=A4)
#     pdf.setTitle("Sample PDF")
#     # pdf.drawString(200, 800, "Hello, user!")
#     pdf.drawImage(snapshot_path, 70, 500, 350, 150)
#     pdf.save()


class MainWindow(QMainWindow):  # inherits from QMainWindow
    def __init__(self):  # constructor
        super().__init__()  # calls parent init to ensure proper initialization
        self.plot_widget_one = None
        self.plot_widget_two = None
        self.thread = None
        self.fetch_subscriber_count = DataFetcher()
        self.fetch_subscriber_count.live_signal.connect(self.update_count)
        self.timestamps = []
        self.subscriber_counts = []
        self.start_time = time.time()
        self.init_ui()

    def init_ui(self):

        ####REPLACE WITH NEW UI#####
        self.setWindowTitle("BIOSIGNAL")
        self.setGeometry(0, 0, 1860, 950)
        self.setWindowIcon(QIcon("images/app icon.png"))

        channel_one_label = QLabel(self)
        channel_one_label.setGeometry(380, 120, 1100, 350)
        channel_one_label.setStyleSheet("background-color: #f5f5f5;"
                                        "border: 2px solid #212434")
        channel_one_layout = QtWidgets.QVBoxLayout(channel_one_label)
        self.plot_widget_one = pg.PlotWidget()
        channel_one_layout.addWidget(self.plot_widget_one)

        channel_two_label = QLabel(self)
        channel_two_label.setGeometry(380, 520, 1100, 350)
        channel_two_label.setStyleSheet("background-color: #f5f5f5;"
                                        "border: 2px solid #212434")
        channel_two_layout = QtWidgets.QVBoxLayout(channel_two_label)
        self.plot_widget_two = pg.PlotWidget()
        channel_two_layout.addWidget(self.plot_widget_two)

        button = QPushButton("Subscriber", self)
        button.setGeometry(1060, 2, 200, 50)
        button.setStyleSheet("font-size: 30px;")
        button.clicked.connect(lambda: self.live_connection('connect'))

        button = QPushButton("no count", self)
        button.setGeometry(1280, 2, 200, 50)
        button.setStyleSheet("font-size: 30px;")
        button.clicked.connect(lambda: self.live_connection('disconnect'))

        ####REPLACE WITH NEW UI#####

        self.fetch_subscriber_count.live_signal.connect(self.update_count)

    def live_connection(self, status):
        if status == "connect":
            self.fetch_subscriber_count.connected = True
            self.thread = threading.Thread(target=self.fetch_subscriber_count.fetch_data)
            self.thread.start()
        else:
            self.fetch_subscriber_count.connected = False

    # def update_count(self):
    #     subscriber_count = self.fetch_subscriber_count.subscriber_count
    #     elapsed_time = time.time() - self.start_time  # Change to full time?
    #
    #     self.timestamps.append(elapsed_time)
    #     self.subscriber_counts.append(subscriber_count)
    #
    #     self.plot_widget_two.plot(self.timestamps, self.subscriber_counts, pen=pg.mkPen(color='g', width=2), symbol='o',
    #                               symbolBrush='w')
    #
    #     self.plot_widget_two.setLabel('left', 'Subscribers Count')
    #     self.plot_widget_two.setLabel('bottom', 'Time')
    #
    #     # Set Y-axis range
    #     if self.subscriber_counts:
    #         y_min = min(self.subscriber_counts) - 10
    #         y_max = max(self.subscriber_counts) + 10
    #         self.plot_widget_two.setYRange(y_min, y_max)
    #         self.plot_widget_two.setXRange(0, max(self.timestamps) + 5)
    #
    #         # Format y-axis ticks
    #         self.plot_widget_two.getAxis('left').setTicks(
    #             [[(count, str(count)) for count in
    #               range(int(y_min), int(y_max) + 1, 5)]])  # Difference of 5 subscribers
    #
    #     # Format x-axis to show time
    #     self.plot_widget_two.getAxis('bottom').setTicks(
    #         [[(t, time.strftime("%H:%M:%S", time.gmtime(t))) for t in self.timestamps]])
    #
    #     self.plot_widget_two.repaint()

    def update_count(self):
        subscriber_count = self.fetch_subscriber_count.subscriber_count
        current_time = time.time() - self.start_time  # Calculate elapsed time

        self.timestamps.append(current_time)
        self.subscriber_counts.append(subscriber_count)

        self.plot_widget_two.clear()  # Clear previous plots
        self.plot_widget_two.plot(self.timestamps, self.subscriber_counts, pen=pg.mkPen(color='g', width=2), symbol='o',
                                  symbolBrush='w')

        # Set axis labels
        self.plot_widget_two.setLabel('left', 'Subscribers')
        self.plot_widget_two.setLabel('bottom', 'Time')

        # Set Y-axis range to highlight small changes
        if self.subscriber_counts:
            y_min = min(self.subscriber_counts) - 10  # Adjust as needed for clarity
            y_max = max(self.subscriber_counts) + 10
            self.plot_widget_two.setYRange(y_min, y_max)
            self.plot_widget_two.setXRange(0, max(self.timestamps) + 5)

        # Format x-axis to show time
        self.plot_widget_two.getAxis('bottom').setTicks(
            [[(t, time.strftime("%H:%M:%S", time.gmtime(t))) for t in self.timestamps]])

        # Optional: Format y-axis ticks for clarity
        self.plot_widget_two.getAxis('left').setTicks(
            [[(count, str(count)) for count in range(int(y_min), int(y_max) + 1, 5)]])

        self.plot_widget_two.repaint()  # Force a refresh of the plot


def main():
    app = QApplication(sys.argv)  # create new app object
    window = MainWindow()  # create new window object
    window.show()
    sys.exit(app.exec_())  # app.exec_() waits for user to close window


if __name__ == "__main__":  # script is being run directly not imported
    main()
