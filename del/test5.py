import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.running = True

    def initUI(self):
        self.setWindowTitle('Satellite Tracker')
        self.setGeometry(100, 100, 200, 100)

        self.disconnect_button = QPushButton('Disconnect', self)
        self.disconnect_button.clicked.connect(self.disconnect)

        layout = QVBoxLayout()
        layout.addWidget(self.disconnect_button)
        self.setLayout(layout)

    def disconnect(self):
        self.running = False

def fetch_coordinates(app):
    options = Options()
    service = Service("D:\\College\\Programs\\edgedriver_win64\\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)
    driver.get("https://www.n2yo.com/")

    while app.running:
        latitude_element = driver.find_element(By.ID, 'satlat')
        latitude = latitude_element.text
        print(f"Current Latitude: {latitude}")
        time.sleep(2.7)

    driver.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    fetch_coordinates(my_app)
    sys.exit(app.exec_())
