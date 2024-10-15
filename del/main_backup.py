# import sys
# import time
# import requests
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
# from PIL import Image
# import pandas as pd
# import pyqtgraph as pg
#
# import re
# from selenium import webdriver
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.edge.options import Options
#
#
# screen_width, screen_height = pyautogui.size()
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
#     snapshot_path = "../Snapshots/snapshot.png"
#     snapshot.save(snapshot_path)
#     pdf = canvas.Canvas("../Reports/example.pdf", pagesize=A4)
#     pdf.setTitle("Sample PDF")
#     # pdf.drawString(200, 800, "Hello, user!")
#     pdf.drawImage(snapshot_path, 70, 500, 350, 150)
#     pdf.save()
#
#
# class MainWindow(QMainWindow):  # inherits from QMainWindow
#     def __init__(self):  # constructor
#         super().__init__()  # calls parent init to ensure proper initialization
#         self.setWindowTitle("BIOSIGNAL")
#         self.setGeometry(0, 0, 1860, 950)
#         self.setWindowIcon(QIcon("../images/app icon.png"))
#         self.initUI()
#
#         #live plotting attributes
#         self.connected = False
#         self.driver = None
#         self.latitude_data = []
#         self.longitude_data = []
#         self.latitude = None
#         self.longitude = None
#         # self.live_plotting()
#         # self.channel_two()
#
#     def initUI(self):
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
#
#         channel_two_label = QLabel(self)
#         channel_two_label.setGeometry(380, 520, 1100, 350)
#         channel_two_label.setStyleSheet("background-color: #f5f5f5;"
#                                         "border: 2px solid #212434")
#
#         channel_two_layout = QtWidgets.QVBoxLayout(channel_two_label)
#         self.plot_widget = pg.PlotWidget()
#         channel_two_layout.addWidget(self.plot_widget)
#
#         import_icon = QPixmap("import_icon.png")
#         # link_channels_button.setPixmap(import_icon)
#         # link_channels_button.setScaledContents(True)
#
#         self.signal_one_label = QLineEdit(self)
#         self.signal_one_label.setGeometry(100, 100, 200, 40)
#         self.signal_one_label.setStyleSheet("font-size: 20px;"
#                                             "font-family: Garet;")
#         signal_one_button = QPushButton("Update Label", self)
#         signal_one_button.setGeometry(100, 200, 200, 50)
#         signal_one_button.clicked.connect(self.update_label)
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
#         button = QPushButton("Test Live", self)
#         button.setGeometry(1040, 2, 200, 50)
#         button.setStyleSheet("font-size: 30px;")
#         button.clicked.connect(self.test_live)
#
#     def test_live(self):
#         pass
#
#
#     def channel_two(self, status):
#         if status == 'connect':
#             self.connected = True
#             # self.live_plotting()
#             self.thread = threading.Thread(target=self.fetch_coordinates) #to run in parallel
#             self.plotting_thread = threading.Thread(target=self.live_plotting)
#             self.thread.start()
#             self.plotting_thread.start()
#             # self.live_plotting()
#         else:
#             self.connected = False
#             if self.driver:
#                 self.driver.quit()
#
#     def fetch_coordinates(self):
#         # response = requests.get("https://www.orbtrack.org/#/?satName=ISS%20(ZARYA)")
#         # response = requests.get("https://www.n2yo.com/")
#
#         # trying to hide browser window
#         options = Options()
#         # options.add_argument("--headless")
#         # options.add_argument('--disable-gpu')
#
#         service = Service("D:\\College\\Programs\\edgedriver_win64\\msedgedriver.exe")
#         self.driver = webdriver.Edge(service=service, options=options)
#         # driver.get('https://www.orbtrack.org/#/?satName=ISS%20(ZARYA)') #another website
#         self.driver.get("https://www.n2yo.com/")
#         time.sleep(2.7)
#         while self.connected:
#             latitude_element = self.driver.find_element(By.ID, 'satlat')
#             self.latitude = latitude_element.text
#             self.latitude_data.append(float(self.latitude))
#             # print(f"Current Latitude: {latitude}")
#             longitude_element = self.driver.find_element(By.ID, 'satlng')
#             self.longitude = longitude_element.text
#             self.longitude_data.append(float(self.longitude))
#             # print(f"Current Longitude: {longitude}")
#
#     def live_plotting(self):
#         while self.connected:
#             print(f"Current Latitude: {self.latitude}")
#             print(f"Current Longitude: {self.longitude}")
#
#             # # Sample data
#             # x = [1, 2, 3, 4, 5]
#             # y = [10, 20, 30, 40, 50]
#             # self.plot_widget.plot([float(self.latitude)], [float(self.longitude)], pen=pg.mkPen(color='r', width=2), symbol='o', symbolBrush='b')
#             #
#             # self.plot_widget.plot(self.latitude_data, self.longitude_data, pen=pg.mkPen(color='r', width=2), symbol='o',symbolBrush='b')
#             # # Set specific coordinates for the plot
#             # self.plot_widget.setXRange(0, 6)
#             # self.plot_widget.setYRange(0, 60)
#             #
#             # # Add labels
#             # self.plot_widget.setLabel('left', 'Value')
#             # self.plot_widget.setLabel('bottom', 'Index')
#
#
#
#     def update_label(self):
#         signal_one_name = self.signal_one_label.text()
#         print(f"Clicked {signal_one_name}")
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