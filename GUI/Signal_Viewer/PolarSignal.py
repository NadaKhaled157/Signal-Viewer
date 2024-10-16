import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt


class PolarWindow(QMainWindow):
    def __init__(self, timestamps, signal_values, signal_label):
        super().__init__()
        self.time = timestamps
        self.signal_values = signal_values
        self.signal_label = signal_label
        self.theta = 2 * np.pi * self.time / max(self.time)  # normalize time to (0,2pi)

        self.radar_radius = 1
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "polar"}, facecolor='black')

        # layout carries canvas which carries the plot
        self.canvas = FigureCanvas(self.fig)  # bridge between PyQt5 and matplotlib
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color:black;")
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)  # layout arranges widgets vertically
        self.layout.addWidget(self.canvas)  # adds canvas that has the plot to the layout
        self.layout_two = QVBoxLayout()

        # Signal Drawing
        self.signal, = self.ax.plot([], [], 'r-')  # initialize signal
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, frames=5*len(self.time),
                                           interval=50, repeat=False)
        self.init_ui()
        self.init_plot()

    def init_ui(self):
        self.setWindowTitle("Signal in Polar View")
        self.setGeometry(0, 0, 1000, 1000)
        window_icon = QIcon('D:/College/Third year/First Term/DSP/Tasks/Task 1/Signal-Viewer/GUI/Deliverables/nonpolar.png')
        self.setWindowIcon(window_icon)

        self.signal_label = QLabel(f'{self.signal_label}')  # GET SIGNAL LABEL FROM MAIN WINDOW
        self.signal_label.setStyleSheet("color:white;")
        label_font = QFont('Arial', 15)  # GET FONT USED IN MAIN WINDOW
        self.signal_label.setFont(label_font)
        self.signal_label.setFixedSize(500, 100)
        self.signal_label.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.signal_label, alignment=Qt.AlignHCenter)
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_plot(self):
        self.ax.xaxis.grid(True, color='grey')
        self.ax.yaxis.grid(True, color='grey')
        self.ax.spines['polar'].set_color('grey')
        self.ax.set_ylim(-0.7, 2)  # radius range
        self.ax.set_yticks(np.linspace(-0.7, 2, 10))  # number of circles
        self.ax.set_thetagrids(range(0, 360, 20))  # radial lines
        self.ax.set_facecolor('black')
        self.ax.xaxis.set_tick_params(labelcolor='white')
        self.ax.yaxis.set_tick_params(labelcolor='white')

    def update_plot(self, frame):
        # frame is required by FuncAnimation
        current_time = self.theta[:frame]
        value_to_plot = self.signal_values[:frame]
        self.signal.set_data(current_time, value_to_plot)
        return self.signal,


# def main():
#     app = QApplication(sys.argv)
#     signal_window = RadarWindow()
#     signal_window.show()
#     sys.exit(app.exec_())
#
#
# if __name__ == "__main__":
#     main()
