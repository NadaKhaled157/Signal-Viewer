import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QWidget, QVBoxLayout
import pyqtgraph as pg


class NewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("RADAR SIGNAL")
        self.setGeometry(0, 0, 1000, 1000)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        # polar_graph_label = QLabel()
        # polar_graph_label.setGeometry(0, 0, 1000, 1000)
        # polar_graph_label.setStyleSheet()
        # polar_graph_layout = QtWidgets.QVBoxLayout(polar_graph_label)
        # polar_plot_widget = pg.PlotWidget()
        # polar_graph_layout.addWidget(polar_plot_widget)
        fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
        # fig.patch.set_facecolor('white')
        # ax.set_facecolor('black')
        # ax.plot(theta, r)
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        canvas.draw()


def main():
    app = QApplication(sys.argv)
    signal_window = NewWindow()
    signal_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
