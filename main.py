import random
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import QtCore, QtGui
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget, QFileDialog, \
    QVBoxLayout, QSlider, QCheckBox, QScrollBar, QVBoxLayout, QDialog, QComboBox, QLineEdit, QFrame
import pandas as pd
import sys
from PyQt5.QtCore import Qt, QPoint, QRect
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from scipy.interpolate import interp1d
from scipy import stats


class SignalObject:
    def __init__(self, x_data, y_data, plot_widget, color, name, signalId):
        self.name = name

        # line will be plotted

        self.x = x_data
        self.y = y_data
        self.signalId = signalId
        self.color = color
        self.plot_widget = plot_widget
        self.index = 0
        self.time = []
        self.magnitude = []
        self.showSignal = True

        # line will be plotted
        self.line = self.plot_widget.plot([], [], pen=pg.mkPen(color=self.color, width=2.5), name=self.name)

    def update(self):
        if self.index < len(self.x):
            self.time.append(self.x[self.index])
            self.magnitude.append(self.y[self.index])
            self.index += 1
            if self.showSignal:
                self.line.setData(self.time, self.magnitude)
                if len(self.time) > 400:
                    self.plot_widget.setXRange(self.time[-400], self.time[-1])
                else:
                    self.plot_widget.setXRange(self.x[0], self.x[399])

    def scrollSignalHorizontal(self, value):
        start = value
        end = min(start + 400, len(self.x) - 1)
        self.plot_widget.setXRange(self.x[start], self.x[end])

    def rename_signal(self, name):
        self.name = name  
        self.line.clear()
        self.plot_widget.legend.removeItem(self.line)
        self.line = self.plot_widget.plot(self.time, self.magnitude, pen=pg.mkPen(color=self.color, width=2.5),
                                          name=name)
    
    

    def change_color(self, color):

        self.color = color
        self.line.clear()
        self.plot_widget.legend.removeItem(self.line)
        self.line = self.plot_widget.plot(self.time, self.magnitude, pen=pg.mkPen(color=color, width=2.5),
                                          name=self.name)

        # scroll if more than 400 points are plotted
        # if len(self.time) > 400:
        #     self.plot_widget.setXRange(self.time[-400], self.time[-1])
        # else:
        #     self.plot_widget.setXRange(self.x[0], self.x[399])

    def signalStatistics(self):
        mean_value = np.mean(self.y)
        median_value = np.median(self.y)
        std_value = np.std(self.y)
        min_value = np.min(self.y)
        max_value = np.max(self.y)

        duration = self.x[-1] - self.x[0]
        return [mean_value, median_value, std_value, min_value, max_value, duration]


class SignalCine(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height, scrollBarHorizontal, scrollBarVertical):
        super().__init__(parent)

        # Set geometry and layout
        self.setGeometry(QtCore.QRect(x, y, width, height))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        # signals
        self.signalsChannel = []  # list of object"signal"
        self.used_color = set()  # to track the colored appeared
        self.signalId = 0
        # Set up the layout
        self.main_layout = QVBoxLayout(self)

        # Checkbox layout (Channel 1 & 2)
        self.checkbox_layout = QVBoxLayout()
        self.main_layout.addLayout(self.checkbox_layout)
        # First graph
        self.plot_graph = pg.PlotWidget()
        legend = self.plot_graph.addLegend(offset=(-30, 0.5))
        legend.setBrush(QBrush(QColor(128, 128, 128, 70)))
        self.plot_graph.legend = legend
        self.plot_graph.showGrid(x=True, y=True)
        self.main_layout.addWidget(self.plot_graph)
        # previous scroll bar values
        self.previous_scroll_value_vertical = 0
        self.previous_x_range = self.plot_graph.getAxis('bottom').range
        self.previous_y_range = self.plot_graph.getAxis('left').range
        # scroll bars
        self.scrollBarHorizontal = scrollBarHorizontal
        self.scrollBarHorizontal.setValue(0)  # Set the initial value
        self.scrollBarVertical = scrollBarVertical
        self.scrollBarVertical.valueChanged.connect(self.scrollSignalVertical)
        self.scrollBarHorizontal.valueChanged.connect(self.scrollSignalHorizontal)
        self.scrollBarVertical.setInvertedAppearance(True)

        ## the timer
        self.defaultSpeed = 25
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.defaultSpeed)
        self.timer.timeout.connect(self.updateSignals)

    def updateSignals(self):
        if self.scrollBarHorizontal.underMouse() == False and self.scrollBarVertical.underMouse() == False:
            self.detectRangeChange()
        for signal in self.signalsChannel:
            signal.update()
        self.plot_graph.update()

    def uploadSignal(self):
        print("Button clicked")
        x, y = self.open_file()
        if x is not None and y is not None:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            while color in self.used_color:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.used_color.add(color)
            self.signalId += 1
            signal = SignalObject(x, y, self.plot_graph, color, f"signal {len(self.signalsChannel) + 1}", self.signalId)
            self.signalsChannel.append(signal)

            # Set the scroll bar conditions
            self.scrollBarHorizontal.setRange(0, len(x) - 401)
            self.scrollBarHorizontal.setSingleStep(20)
            self.scrollBarHorizontal.setPageStep(100)

            yMin, yMax = min(y), max(y)
            self.plot_graph.plotItem.vb.setLimits(xMin=0, xMax=x[-1], yMin=yMin, yMax=yMax)

            # Set vertical slider range based on signal's full range
            self.scrollBarVertical.setRange(0, 100)  # Use 0-100 for percentage
            self.scrollBarVertical.setValue(0)  # Start at the bottom

            # Store the full y-range for later use
            self.full_y_range = (yMin, yMax)

            self.timer.start()
            print("x data:", x)
            print("y data:", y)
            return signal

    def detectRangeChange(self):
        #  print("iam here")
        x_range = self.plot_graph.getAxis('bottom').range
        y_range = self.plot_graph.getAxis('left').range
        if x_range != self.previous_x_range:
            signal = self.signalsChannel[-1]
            x_range_size = signal.x[-405] - signal.x[0]
            scroll_bar_range = self.scrollBarHorizontal.maximum() - self.scrollBarHorizontal.minimum()
            scroll_bar_value = int(((x_range[0] - signal.x[0]) / (x_range_size)) * scroll_bar_range)
            self.scrollBarHorizontal.setValue(scroll_bar_value)
            # print(self.scrollBarHorizontal.value())

        if y_range != self.previous_y_range:
            signal = self.signalsChannel[-1]
            y_range_size = max(signal.y) - min(signal.y)
            y_min, y_max = min(signal.y), max(signal.y)

            scroll_bar_range = self.scrollBarVertical.maximum() - self.scrollBarVertical.minimum()
            scroll_bar_value = int(((y_range[0] - min(signal.y)) / y_range_size) * scroll_bar_range)
            self.scrollBarVertical.setValue(scroll_bar_value)

        self.previous_x_range = x_range
        self.previous_y_range = y_range

    def scrollSignalHorizontal(self, value):
        if not self.scrollBarHorizontal.underMouse():
            return
        self.scrollBarHorizontal.setValue(value)
        for signal in self.signalsChannel:
            signal.scrollSignalHorizontal(value)

    def scrollSignalVertical(self, value):
        if not self.scrollBarVertical.underMouse():
            return

        # yMin, yMax = self.full_y_range
        yMin, yMax = self.plot_graph.getAxis('left').range
        total_range = yMax - yMin
        # view_range = total_range / 4  # Show 1/4 of the total range at a time
        # Invert the value calculation
        inverted_value = 100 - value

        # Calculate the new bottom of the view using the inverted value
        bottom = yMin + (total_range - 0) * (inverted_value / 100)

        # Set the new y-range
        self.plot_graph.setYRange(bottom, bottom + 0, padding=0)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        path = filename[0]

        if path:
            data = pd.read_csv(path)
            x = data.iloc[:, 0].values
            y = data.iloc[:, 1].values
            return x, y
        else:
            print("No file selected")
            return None, None

    def rewindSignal(self):
        self.timer.start()
        for signal in self.signalsChannel:
            signal.index = 0
            signal.time = []
            signal.magnitude = []
            signal.line.setData([], [])
        return

    def playSignal(self):
        self.timer.start()
        return

    def pauseSignal(self):
        self.timer.stop()
        return

    def changeSpeed(self, value):
        self.defaultSpeed = 50 - value
        self.timer.setInterval(self.defaultSpeed)
        print(self.defaultSpeed)
        return

    def zoom(self, zoomIn=True):
        
        # Get the ViewBox of the plot widget
        view_box = self.plot_graph.getViewBox()

        # Get the current range for both axes
        x_range, y_range = view_box.viewRange()

        # Factor for zooming: use 0.8 for zoom in, and 1.25 for zoom out
        zoom_factor = 0.8 if zoomIn else 1.25

        # Calculate the center of the current range
        x_center = (x_range[0] + x_range[1]) / 2
        y_center = (y_range[0] + y_range[1]) / 2

        # Calculate the new range for x-axis and y-axis, keeping the same zoom factor for both
        new_x_range = [
            x_center - (x_center - x_range[0]) * zoom_factor,
            x_center + (x_range[1] - x_center) * zoom_factor
        ]
        new_y_range = [
            y_center - (y_center - y_range[0]) * zoom_factor,
            y_center + (y_range[1] - y_center) * zoom_factor
        ]

        # Set the new range for both x and y axes
        view_box.setRange(xRange=new_x_range, yRange=new_y_range)





# Start the application
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main = SignalCine()
    main.show()
    sys.exit(app.exec_())



