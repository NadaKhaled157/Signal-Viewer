# import sys
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


class DataFetcher(QThread):
    data_signal = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.connected = False
        self.driver = None
        self.latitude_data = []
        self.longitude_data = []

    def fetch_data(self):
        options = Options()
        # options.add_argument("--headless")
        # options.add_argument('--disable-gpu')
        service = Service("D:\\College\\Programs\\edgedriver_win64\\msedgedriver.exe")
        self.driver = webdriver.Edge(service=service, options=options)
        # self.driver.get('https://www.orbtrack.org/#/?satName=ISS%20(ZARYA)') #another website
        self.driver.get("https://www.n2yo.com/")
        time.sleep(2.7)

        while self.connected:
            # latitude_element = self.driver.find_element(By.ID, 'satLat')
            # longitude_element = self.driver.find_element(By.ID, 'satLon')
            latitude_element = self.driver.find_element(By.ID, 'satlat')
            longitude_element = self.driver.find_element(By.ID, 'satlng')
            try:
                latitude = float(latitude_element.text)
                print(f"Latitude: {latitude}")
                self.latitude_data.append(latitude)
                longitude = float(longitude_element.text)
                print(f"Longitude: {longitude}")
                self.longitude_data.append(longitude)
            except:
                continue
            # if latitude and longitude:
            self.data_signal.emit(latitude, longitude)
            time.sleep(1)

def mercator_map_projection(longitude, latitude):
    earth_radius = 6378137
    x_coordinate = earth_radius * np.radians(longitude)
    y_coordinate = earth_radius * np.log(np.tan(np.pi/4 + np.radians(latitude)/2))
    return x_coordinate, y_coordinate


