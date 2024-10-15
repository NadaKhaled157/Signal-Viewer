import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class FetchThread(QThread):
    data_fetched = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super(FetchThread, self).__init__(parent)
        self.connected = False

    def run(self):
        options = Options()
        service = Service("D:\\College\\Programs\\edgedriver_win64\\msedgedriver.exe")
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.get("https://www.n2yo.com/")
        time.sleep(2.7)
        while self.connected:
            latitude_element = self.driver.find_element(By.ID, 'satlat')
            if latitude_element is not None:
                latitude = float(latitude_element.text)
                self.latitude_data.append(latitude)
            longitude_element = self.driver.find_element(By.ID, 'satlng')
            if longitude_element is not None:
                longitude = float(longitude_element.text)
                self.longitude_data.append(longitude)
            if latitude and longitude:
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
        self.setWindowTitle("Live Data Plotting")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.button = QPushButton("Connect Live", self)
        self.button.setStyleSheet("font-size: 30px;")
        self.button.clicked.connect(self.channel_two)
        self.layout.addWidget(self.button)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)
        self.plot = self.plot_widget.plot([], [], pen='r')

        self.latitude_data = []
        self.longitude_data = []

        self.fetch_thread = FetchThread()
        self.fetch_thread.data_fetched.connect(self.update_plot)

    def channel_two(self):
        if not self.fetch_thread.connected:
            self.fetch_thread.connected = True
            self.fetch_thread.start()
        else:
            self.fetch_thread.stop()

    def update_plot(self, latitude, longitude):
        self.latitude_data.append(latitude)
        self.longitude_data.append(longitude)
        self.plot.setData(self.longitude_data, self.latitude_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
