import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cine Mode: Moving Object")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a button to start the animation
        self.start_button = QPushButton("Start Animation", self)
        self.start_button.clicked.connect(self.start_animation)
        layout.addWidget(self.start_button)

        # Create a PyQtGraph plot widget
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Define coordinates (latitude and longitude)
        self.coordinates = [
            (51.46807, -20.89408),
            (51.46900, -20.89500),
            (51.47000, -20.89600),
            (51.47100, -20.89700),
            (51.47200, -20.89800),
        ]

        # Prepare the plot
        self.plot_widget.setTitle("Cine Mode: Moving Object")
        self.plot_widget.setLabel('left', 'Latitude')
        self.plot_widget.setLabel('bottom', 'Longitude')
        self.plot_widget.setXRange(-180, 180)
        self.plot_widget.setYRange(-90, 90)

        # Initialize the marker
        self.marker = pg.ScatterPlotItem(pen='r', brush='r', size=10)
        self.plot_widget.addItem(self.marker)

        # Animation variables
        self.index = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_marker)

    def start_animation(self):
        self.index = 0  # Reset index
        self.timer.start(500)  # Update every 500 ms

    def update_marker(self):
        if self.index < len(self.coordinates):
            lat, lon = self.coordinates[self.index]
            self.marker.setData([lon], [lat])  # Update marker position
            self.index += 1
        else:
            self.timer.stop()  # Stop the animation when done

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PlotWindow()
    main_window.show()
    sys.exit(app.exec_())