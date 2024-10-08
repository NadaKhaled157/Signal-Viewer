import sys
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg

class DataThread(QThread):
    data_signal = pyqtSignal(np.ndarray)

    def run(self):
        while True:
            data = np.random.normal(size=100)  # Simulate data update
            self.data_signal.emit(data)
            time.sleep(0.1)  # Simulate delay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Real-Time Plotting with PyQtGraph")
        self.resize(800, 600)

        self.plot_widget = pg.PlotWidget()
        self.plot_data = self.plot_widget.plot()

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.data_thread = DataThread()
        self.data_thread.data_signal.connect(self.update_plot)
        self.data_thread.start()

    def update_plot(self, data):
        self.plot_data.setData(data)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
