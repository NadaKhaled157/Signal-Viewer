# import sys
# import time
# # import requests
# import threading
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QFileDialog
# from PyQt5.QtGui import QIcon, QFont, QPixmap
# from PyQt5.QtCore import Qt  # alignment
#
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# import pyautogui
# import pyscreenshot as ImageGrab
# import pandas as pd
# import pyqtgraph as pg
#
# from LiveSignal import DataFetcher, mercator_map_projection
# from LiveSignal import FetchData
#
# screen_width, screen_height = pyautogui.size()
#
#
# def take_snapshot(channel_number):
#     if channel_number == 1:
#         bbox = (380, 160, 1500, 535)
#         # signal_name = signal_one_name
#     elif channel_number == 2:
#         bbox = (380, 500, 1500, 1060)
#         # signal_name = signal_two_name
#     else:
#         bbox = (380, 160, 1500, 1070)
#
#     # snapshot = pyautogui.screenshot()
#     # snapshot_path = "Snapshots/snapshot.png"
#     # snapshot.save(snapshot_path)
#
#     snapshot = ImageGrab.grab(bbox=bbox)
#     snapshot.show()
#     snapshot_path = "Snapshots/snapshot.png"
#     snapshot.save(snapshot_path)
#     pdf = canvas.Canvas("Reports/example.pdf", pagesize=A4)
#     pdf.setTitle("Sample PDF")
#     # pdf.drawString(200, 800, "Hello, user!")
#     pdf.drawImage(snapshot_path, 70, 500, 350, 150)
#     pdf.save()
#
#
# class MainWindow(QMainWindow):  # inherits from QMainWindow
#     def __init__(self):  # constructor
#         super().__init__()  # calls parent init to ensure proper initialization
#         self.plot_widget_one = None
#         self.plot_widget_two = None
#         self.latitude_plot = None
#         self.longitude_plot = None
#         self.thread = None
#         self.data_fetcher = DataFetcher()
#         self.data_fetcher.data_signal.connect(self.update_plot)
#
#         self.fetch_count = FetchData()
#         self.fetch_count.signal.connect(self.update_count)
#
#         self.times = []
#         self.subscriber_counts = []
#         self.start_time = time.time()
#
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle("BIOSIGNAL")
#         self.setGeometry(0, 0, 1860, 950)
#         self.setWindowIcon(QIcon("images/app icon.png"))
#
#         menu_bar_label = QLabel(self)
#         menu_bar_label.setGeometry(0, 0, 1860, 55)
#         menu_bar_label.setStyleSheet("background-color: #f0f0f0;")
#
#         import_button = QPushButton("Imp", self)
#         import_button.setGeometry(5, 2, 50, 50)
#         import_button.setStyleSheet("background-color: #fafafa")
#         import_button.clicked.connect(self.import_signal)
#         # snapshot_button.setIcon(QIcon("import_icon.png"))
#
#         snapshot_button = QPushButton("1", self)
#         snapshot_button.setGeometry(60, 2, 50, 50)
#         snapshot_button.setStyleSheet("background-color: #fafafa")
#         snapshot_button.clicked.connect(lambda: take_snapshot(1))
#         # snapshot_button.setIcon(QIcon("snapshot_icon.png"))
#
#         # link_channels_button = QPushButton("Link Channels ", self)
#         # link_channels_button.setFont(QFont("Garet", 8))
#         # link_channels_button.setGeometry(115, 2, 200, 50)
#         # link_channels_button.setStyleSheet("background-color: #fafafa")
#         # link_channels_button.setStyleSheet("color:#3f446f;"
#         #                                   "background-color:white;"
#         #                                   "font-weight:bold;")
#         # link_channels_button.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#         # label.setAlignment(Qt.AlignLeft)
#         # label.setAlignment(Qt.AlignVCenter)  # vertical alignment (default)
#         # label.setAlignment(Qt.AlignCenter)  # center vertically & horizontally
#
#         snapshot_two_button = QPushButton("2", self)
#         snapshot_two_button.setGeometry(320, 2, 50, 50)
#         snapshot_two_button.setStyleSheet("background-color: #fafafa")
#         snapshot_two_button.clicked.connect(lambda: take_snapshot(2))
#         # snapshot_button.setIcon(QIcon("snapshot_icon.png"))
#
#         left_section_label = QLabel(self)
#         left_section_label.setGeometry(15, 70, 300, 850)
#         left_section_label.setStyleSheet("background-color: #fafafa;")
#
#         middle_section_label = QLabel(self)
#         middle_section_label.setGeometry(330, 70, 1200, 850)
#         middle_section_label.setStyleSheet("background-color: #fafafa;")
#
#         right_section_label = QLabel(self)
#         right_section_label.setGeometry(1545, 70, 300, 850)
#         right_section_label.setStyleSheet("background-color: #fafafa;")
#
#         channel_one_label = QLabel(self)
#         channel_one_label.setGeometry(380, 120, 1100, 350)
#         channel_one_label.setStyleSheet("background-color: #f5f5f5;"
#                                         "border: 2px solid #212434")
#         channel_one_layout = QtWidgets.QVBoxLayout(channel_one_label)
#         self.plot_widget_one = pg.PlotWidget()
#         channel_one_layout.addWidget(self.plot_widget_one)
#
#         channel_two_label = QLabel(self)
#         channel_two_label.setGeometry(380, 520, 1100, 350)
#         channel_two_label.setStyleSheet("background-color: #f5f5f5;"
#                                         "border: 2px solid #212434")
#         channel_two_layout = QtWidgets.QVBoxLayout(channel_two_label)
#         self.plot_widget_two = pg.PlotWidget()
#         channel_two_layout.addWidget(self.plot_widget_two)
#         self.latitude_plot = self.plot_widget_two.plot(pen='r', name="Latitude")
#         self.longitude_plot = self.plot_widget_two.plot(pen='b', name="Longitude")
#
#         import_icon = QPixmap("import_icon.png")
#         # link_channels_button.setPixmap(import_icon)
#         # link_channels_button.setScaledContents(True)
#
#         signal_one_label = QLineEdit(self)
#         signal_one_label.setGeometry(100, 100, 200, 40)
#         signal_one_label.setStyleSheet("font-size: 20px;"
#                                        "font-family: Garet;")
#         signal_one_button = QPushButton("Update Label", self)
#         signal_one_button.setGeometry(100, 200, 200, 50)
#         # signal_one_button.clicked.connect(self.update_label)
#
#         button = QPushButton("click meee ", self)
#         button.setGeometry(400, 2, 200, 50)
#         button.setStyleSheet("font-size: 30px;")
#         button.clicked.connect(self.on_click)
#
#         button = QPushButton("Connect Live", self)
#         button.setGeometry(620, 2, 200, 50)
#         button.setStyleSheet("font-size: 30px;")
#         button.clicked.connect(lambda: self.channel_two('connect'))
#
#         button = QPushButton("Disconnect", self)
#         button.setGeometry(840, 2, 200, 50)
#         button.setStyleSheet("font-size: 30px;")
#         button.clicked.connect(lambda: self.channel_two('disconnect'))
#
#         button = QPushButton("Subscriber", self)
#         button.setGeometry(1060, 2, 200, 50)
#         button.setStyleSheet("font-size: 30px;")
#         button.clicked.connect(lambda: self.live_connection('connect'))
#
#         button = QPushButton("no count", self)
#         button.setGeometry(1280, 2, 200, 50)
#         button.setStyleSheet("font-size: 30px;")
#         button.clicked.connect(lambda: self.live_connection('disconnect'))
#
#         self.data_fetcher.data_signal.connect(self.update_plot)
#         self.fetch_count.signal.connect(self.update_count)
#
#     def live_connection(self, status):
#         if status == "connect":
#             self.fetch_count.connected = True
#             self.thread = threading.Thread(target=self.fetch_count.fetch_data)
#             self.thread.start()
#         else:
#             self.fetch_count.connected = False
#
#     def channel_two(self, status):
#         if status == 'connect':
#             self.data_fetcher.connected = True
#             self.thread = threading.Thread(target=self.data_fetcher.fetch_data)
#             self.thread.start()
#         else:
#             self.data_fetcher.connected = False
#             if self.data_fetcher.driver:
#                 self.data_fetcher.driver.quit()
#
#     def update_plot(self):
#         x_coordinate, y_coordinate = mercator_map_projection(self.data_fetcher.longitude_data,
#                                                              self.data_fetcher.latitude_data)
#         self.plot_widget_two.plot(x_coordinate, y_coordinate, pen=pg.mkPen(color='r', width=2), symbol='o',
#                                   symbolBrush='b')
#         # Setting axis labels to original longitude and latitude values for readability
#         self.plot_widget_two.getAxis('bottom').setTicks([[(x_coordinate[i], str(self.data_fetcher.longitude_data[i]))
#                                                           for i in range(len(self.data_fetcher.longitude_data))]])
#         self.plot_widget_two.getAxis('left').setTicks([[(y_coordinate[i], str(self.data_fetcher.latitude_data[i]))
#                                                         for i in range(len(self.data_fetcher.latitude_data))]])
#
#     # def update_count(self):
#     #     subscriber_count = self.fetch_count.subscriber_count
#     #     print(f"subscriber count from inside update_count: {subscriber_count}")
#     #     self.plot_widget_two.plot(1, subscriber_count, pen=pg.mkPen(color='r', width=2), symbol='o',
#     #                               symbolBrush='b')
#
#     # def update_count(self):
#     #     subscriber_count = self.fetch_count.subscriber_count
#     #     print(f"Subscriber count from inside update_count: {subscriber_count}")
#     #     self.plot_widget_two.clear()  # Clear previous plots if needed
#     #     self.plot_widget_two.plot([1], [subscriber_count], pen=pg.mkPen(color='r', width=2), symbol='o',
#     #                               symbolBrush='b')
#
    # def update_count(self):
    #     subscriber_count = self.fetch_count.subscriber_count
    #     current_time = time.time() - self.start_time  # Calculate elapsed time
    #
    #     self.times.append(current_time)
    #     self.subscriber_counts.append(subscriber_count)
    #
    #     self.plot_widget_two.clear()  # Clear previous plots
    #     self.plot_widget_two.plot(self.times, self.subscriber_counts, pen=pg.mkPen(color='r', width=2), symbol='o',
    #                               symbolBrush='b')
    #
    #     # Set axis labels
    #     self.plot_widget_two.setLabel('left', 'Subscribers')
    #     self.plot_widget_two.setLabel('bottom', 'Time')
    #
    #     # Set Y-axis range to highlight small changes
    #     if self.subscriber_counts:
    #         y_min = min(self.subscriber_counts) - 10  # Adjust as needed for clarity
    #         y_max = max(self.subscriber_counts) + 10
    #         self.plot_widget_two.setYRange(y_min, y_max)
    #         self.plot_widget_two.setXRange(0, max(self.times) + 5)
    #
    #     # Format x-axis to show time
    #     self.plot_widget_two.getAxis('bottom').setTicks(
    #         [[(t, time.strftime("%H:%M:%S", time.gmtime(t))) for t in self.times]])
    #
    #     # Optional: Format y-axis ticks for clarity
    #     self.plot_widget_two.getAxis('left').setTicks(
    #         [[(count, str(count)) for count in range(int(y_min), int(y_max) + 1, 5)]])
    #
    #     self.plot_widget_two.repaint()  # Force a refresh of the plot
#
#     # def update_label(self):
#     #     signal_one_name = self.signal_one_label.text()
#     #     print(f"Clicked {signal_one_name}")
#
#     # def on_click(self):
#     #     print("button clicked")
#     #     print(self.open_file())
#
#     # def open_file(self):
#     #     filename = QFileDialog.getOpenFileName()
#     #     path = filename[0]
#     #     print(path)
#     #
#     #     x_data = []
#     #     y_data = []
#     #
#     #     file = open(path, "r")
#     #     read = file.readlines()
#     #
#     #     for line in read:
#     #         line = line.strip()
#     #         print(line)
#     #         if line:
#     #             x, y = line.split(',')
#     #             x_data.append(float(x))
#     #             y_data.append(float(y))
#     #
#     #     print ("x data:", x_data)
#     #     print("y data:", y_data)
#     #     return x_data, y_data
#
#     def on_click(self):
#         print("Button clicked")
#         x_data, y_data = self.open_file()
#         if x_data is not None and y_data is not None:
#             print("x data:", x_data)
#             print("y data:", y_data)
#
#     def open_file(self):
#         filename = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
#         path = filename[0]
#
#         if path:
#             data = pd.read_csv(path)
#             x = data.iloc[:, 0].values
#             y = data.iloc[:, 1].values
#             return x, y
#         else:
#             print("No file selected")
#             return None, None
#
#     def import_signal(self):
#         pass
#
#
# def main():
#     app = QApplication(sys.argv)  # create new app object
#     window = MainWindow()  # create new window object
#     window.show()
#     sys.exit(app.exec_())  # app.exec_() waits for user to close window
#
#
# if __name__ == "__main__":  # script is being run directly not imported
#     main()
