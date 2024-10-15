import sys
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class DataFetcher(QThread):
    data_signal = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.connected = False
        self.latitude_data = []
        self.longitude_data = []

    def run(self):
        options = Options()
        service = Service("D:\\College\\Programs\\edgedriver_win64\\msedgedriver.exe")
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.get("https://www.n2yo.com/")
        time.sleep(2.7)
        self.connected = True
        while self.connected:
            latitude_element = self.driver.find_element(By.ID, 'satlat')
            longitude_element = self.driver.find_element(By.ID, 'satlng')
            try:
                latitude = float(latitude_element.text)
                self.latitude_data.append(latitude)
                longitude = float(longitude_element.text)
                self.longitude_data.append(longitude)
            except:
                continue
            # if latitude and longitude:
            self.data_signal.emit(latitude, longitude)
            time.sleep(1)  # Adjust the sleep time as needed

    def stop(self):
        self.connected = False
        if self.driver:
            self.driver.quit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Real-Time Plotting with PyQtGraph")
        self.resize(800, 600)

        self.plot_widget = pg.PlotWidget()
        self.latitude_plot = self.plot_widget.plot(pen='r', name="Latitude")
        self.longitude_plot = self.plot_widget.plot(pen='b', name="Longitude")

        self.button = QPushButton("Connect Live", self)
        self.button.setGeometry(620, 2, 200, 50)
        self.button.setStyleSheet("font-size: 30px;")
        self.button.clicked.connect(self.channel_two)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.data_fetcher = DataFetcher()
        self.data_fetcher.data_signal.connect(self.update_plot)

    def channel_two(self):
        if not self.data_fetcher.isRunning():
            self.data_fetcher.start()
            self.button.setText("Disconnect")
        else:
            self.data_fetcher.stop()
            self.button.setText("Connect Live")

    def update_plot(self, latitude, longitude):
        self.latitude_plot.setData(self.data_fetcher.latitude_data)
        self.longitude_plot.setData(self.data_fetcher.longitude_data)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
