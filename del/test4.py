# import sys
# from PyQt5 import QtWidgets, QtGui
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QFileDialog
# import pyqtgraph as pg
#
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# # import pyautogui
# import pyscreenshot as ImageGrab
# import pandas as pd
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
# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("BIOSIGNAL")
#         self.setGeometry(0, 0, 1860, 950)
#         self.setWindowIcon(QtGui.QIcon("../images/app icon.png"))
#         self.initUI()
#         self.channel_one()
#
#     def initUI(self):
#         menu_bar_label = QtWidgets.QLabel(self)
#         menu_bar_label.setGeometry(0, 0, 1860, 55)
#         menu_bar_label.setStyleSheet("background-color: #f0f0f0;")
#
#         import_button = QtWidgets.QPushButton("Imp", self)
#         import_button.setGeometry(5, 2, 50, 50)
#         import_button.setStyleSheet("background-color: #fafafa")
#         import_button.clicked.connect(self.import_signal)
#
#         snapshot_button = QtWidgets.QPushButton("1", self)
#         snapshot_button.setGeometry(60, 2, 50, 50)
#         snapshot_button.setStyleSheet("background-color: #fafafa")
#         snapshot_button.clicked.connect(lambda: self.take_snapshot(1))
#
#         snapshot_two_button = QtWidgets.QPushButton("2", self)
#         snapshot_two_button.setGeometry(320, 2, 50, 50)
#         snapshot_two_button.setStyleSheet("background-color: #fafafa")
#         snapshot_two_button.clicked.connect(lambda: self.take_snapshot(2))
#
#         left_section_label = QtWidgets.QLabel(self)
#         left_section_label.setGeometry(15, 70, 300, 850)
#         left_section_label.setStyleSheet("background-color: #fafafa;")
#
#         middle_section_label = QtWidgets.QLabel(self)
#         middle_section_label.setGeometry(330, 70, 1200, 850)
#         middle_section_label.setStyleSheet("background-color: #fafafa;")
#
#         right_section_label = QtWidgets.QLabel(self)
#         right_section_label.setGeometry(1545, 70, 300, 850)
#         right_section_label.setStyleSheet("background-color: #fafafa;")
#
#         channel_one_label = QtWidgets.QLabel(self)
#         channel_one_label.setGeometry(380, 120, 1100, 350)
#         channel_one_label.setStyleSheet("background-color: #f5f5f5;"
#                                         "border: 2px solid #212434")
#
#         channel_two_label = QtWidgets.QLabel(self)
#         channel_two_label.setGeometry(380, 520, 1100, 350)
#         channel_two_label.setStyleSheet("background-color: grey;"
#                                         "border: 2px solid #212434")
#
#         # Create a layout for the dark grey box
#         channel_two_layout = QtWidgets.QVBoxLayout(channel_two_label)
#
#         # Create a PlotWidget instance
#         self.plot_widget = pg.PlotWidget()
#
#         # Add the PlotWidget to the layout
#         channel_two_layout.addWidget(self.plot_widget)
#
#         # Sample data
#         x = [1, 2, 3, 4, 5]
#         y = [10, 20, 30, 40, 50]
#
#         # Plot data
#         self.plot_widget.plot(x, y, pen=pg.mkPen(color='r', width=2), symbol='o', symbolBrush='b')
#
#         # Set specific coordinates for the plot
#         self.plot_widget.setXRange(0, 6)
#         self.plot_widget.setYRange(0, 60)
#
#         # Add labels
#         self.plot_widget.setLabel('left', 'Value')
#         self.plot_widget.setLabel('bottom', 'Index')
#
#         self.signal_one_label = QtWidgets.QLineEdit(self)
#         self.signal_one_label.setGeometry(100, 100, 200, 40)
#         self.signal_one_label.setStyleSheet("font-size: 20px;"
#                                             "font-family: Garet;")
#         signal_one_button = QtWidgets.QPushButton("Update Label", self)
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
#         # button.clicked.connect(live_signal)
#
#     def channel_one(self):
#         pass
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
# def main():
#     app = QApplication(sys.argv)  # create new app object
#     window = MainWindow()  # create new window object
#     window.show()
#     sys.exit(app.exec_())  # app.exec_() waits for user to close window
#
#
# if __name__ == "__main__":  # script is being run directly not imported
#     main()
