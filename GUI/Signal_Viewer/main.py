import random
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QWidget, QFileDialog, QVBoxLayout, QSlider, QCheckBox
import pandas as pd
import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class SignalObject:
    def __init__(self, x_data, y_data, plot_widget, color, signalNumber, signalId):
        self.x = x_data
        self.y = y_data
        self.signalId = signalId
        self.color = color
        self.signalNumber = signalNumber
        self.plot_widget = plot_widget
        self.index = 0
        self.time = []
        self.magnitude = []
        self.showSignal = True
        
        # line will be plotted
        self.line = self.plot_widget.plot([], [], pen=pg.mkPen(color=self.color, width=2.5), name=f"signal{str(self.signalNumber)}")

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
            else:
                self.plot_widget.setXRange(self.x[0], self.x[399]) # this to make the graph as the first appearance



            # scroll if more than 400 points are plotted
            # if len(self.time) > 400:
            #     self.plot_widget.setXRange(self.time[-400], self.time[-1])
            # else:
            #     self.plot_widget.setXRange(self.x[0], self.x[399])
    def signalStatistics(self):
        pass

class SignalCine(QtWidgets.QFrame):
    def __init__(self, parent, x, y, width, height):
        super().__init__(parent)
        
        # Set geometry and layout
        self.setGeometry(QtCore.QRect(x, y, width, height))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)

        # signals
        self.signalsChannel1 = []  # list of object"signal"
        self.signalsChannel2 = []
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
        self.plot_graph.showGrid(x=True, y=True)
        self.main_layout.addWidget(self.plot_graph)


        # rewindSignalButton = QPushButton("Rewind", self)
        # rewindSignalButton.setStyleSheet("font-size: 30px;")
        # rewindSignalButton.clicked.connect(self.rewindSignal)
        # self.main_layout.addWidget(rewindSignalButton)

        # zoomInButton = QPushButton("Zoom In", self)
        # zoomInButton.setStyleSheet("font-size: 30px;")
        # zoomInButton.clicked.connect(lambda: self.zoom(zoomIn=True))
        # self.main_layout.addWidget(zoomInButton)

        # zoomOutButton = QPushButton("Zoom Out", self)
        # zoomOutButton.setStyleSheet("font-size: 30px;")
        # zoomOutButton.clicked.connect(lambda: self.zoom(zoomIn=False))
        # self.main_layout.addWidget(zoomOutButton)

        # # Second graph
        # self.plot_graph2 = pg.PlotWidget()
        # legend2 = self.plot_graph2.addLegend(offset=(-30, 0.5))
        # legend2.setBrush(QBrush(QColor(128, 128, 128, 70)))
        # self.plot_graph2.showGrid(x=True, y=True)
        # self.main_layout.addWidget(self.plot_graph2)

        # Timer for updating the plot
        self.defaultSpeed = 25
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.defaultSpeed)
        self.timer.timeout.connect(self.updateSignals)

        # Slider to control speed
        # self.slider = QSlider(Qt.Horizontal)
        # self.slider.setMinimum(1)
        # self.slider.setMaximum(50)
        # self.slider.setValue(self.defaultSpeed)
        # self.slider.valueChanged.connect(self.changeSpeed)
        # self.main_layout.addWidget(self.slider)





    def updateSignals(self):
        for signal in self.signalsChannel1:
            signal.update()
        for signal in self.signalsChannel2:
            signal.update()

    def uploadSignal(self):
        print("Button clicked")
        x, y = self.open_file()
        if x is not None and y is not None:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            while color in self.used_color:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.used_color.add(color)
            self.signalId += 1
            signal = SignalObject(x, y, self.plot_graph, color, len(self.signalsChannel1)+1, self.signalId)
            self.signalsChannel1.append(signal)
            # Dynamically creation of checkboxes
            
            channel_1_Selected = QCheckBox(f"signal{self.signalId} ch1")
            channel_2_Selected = QCheckBox(f"signal{self.signalId} ch2")
            self.checkbox_layout.addWidget(channel_1_Selected)
            self.checkbox_layout.addWidget(channel_2_Selected)
            channel_1_Selected.setChecked(True)
            channel_1_Selected.stateChanged.connect(lambda state, s_id=signal.signalId: self.selectChannel1StateChanged(s_id,state))
            channel_2_Selected.stateChanged.connect(lambda state, s_id=signal.signalId: self.selectChannel2StateChanged(s_id,state))

            yMin, yMax = min(y), max(y)
            self.plot_graph.plotItem.vb.setLimits(xMin=0, xMax=x[-1], yMin=yMin, yMax=yMax)
           # self.rewindSignal()
            self.timer.start()
            print("x data:", x)
            print("y data:", y)

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
        for signal in self.signalsChannel1:
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
        self.defaultSpeed = 50-value
        self.timer.setInterval(self.defaultSpeed)
        print(self.defaultSpeed)
        return

    def selectChannel1StateChanged(self, id, state):
        if state == Qt.Unchecked:  # ch 1 is unchecked
            for signal in self.signalsChannel1:
                if signal.signalId == id:
                    self.plot_graph.removeItem(signal.line)  # remove from ch 1
                    signal.showSignal = False
                    break
        elif state == Qt.Checked:  # ch 1 is checked
            for signal in self.signalsChannel1:
                if signal.signalId == id and signal.line not in self.plot_graph.listDataItems():
                    signal.line.setData(signal.time, signal.magnitude)  # reshow the signal
                    self.plot_graph.addItem(signal.line)  # readd to the plot
                    signal.showSignal = True
                    break

    def selectChannel2StateChanged(self, id, state):
        signalRelated2Id = None
        if state == Qt.Checked:  # ch 2 is checked
            for signal in self.signalsChannel2:
                if signal.signalId == id and signal.line not in self.plot_graph2.listDataItems(): # then it was existed so we need to reshoe
                    signal.line.setData(signal.time, signal.magnitude)  # reshow the signal in Plot
                    signal.showSignal = True
                    self.plot_graph2.addItem(signal.line)
                    return
            for signal in self.signalsChannel1: # here there is no id with that , so we need to create new signal object
                if signal.signalId == id:
                    signalRelated2Id = signal
                    break
            if signalRelated2Id is not None:
                signal = SignalObject(signalRelated2Id.x, signalRelated2Id.y, self.plot_graph2, signalRelated2Id.color,
                                      len(self.signalsChannel2) + 1, id)
                signal.showSignal = True
                self.signalsChannel2.append(signal)
                yMin, yMax = min(signalRelated2Id.y), max(signalRelated2Id.y)
                self.plot_graph2.plotItem.vb.setLimits(xMin=0, xMax=signalRelated2Id.x[-1], yMin=yMin, yMax=yMax)
                signal.line.setData(signalRelated2Id.time, signalRelated2Id.magnitude)
                self.plot_graph2.addItem(signal.line)
        else:  # ch2 2 is unchecked
            for signal in self.signalsChannel2:
                if signal.signalId == id:
                    self.plot_graph2.removeItem(signal.line)  # remove from ch 2
                    signal.showSignal = False
                    break

    def zoom(self,zoomIn=True):
        # Get the current view range
        x_range, y_range = self.plot_graph.viewRange()

        self.min_x_range = 0.1  
        self.max_x_range = 10   
        self.min_y_range = 0.1  
        self.max_y_range = 50   

        
        x_center = (x_range[0] + x_range[1]) / 2
        y_center = (y_range[0] + y_range[1]) / 2
        zoom_factor = 0.8  
        
        if zoomIn:
            new_x_range = [(x_center - (x_center - x_range[0]) * zoom_factor),
                        (x_center + (x_range[1] - x_center) * zoom_factor)]
            new_y_range = [(y_center - (y_center - y_range[0]) * zoom_factor),
                        (y_center + (y_range[1] - y_center) * zoom_factor)]
        else:
            new_x_range = [(x_center - (x_center - x_range[0]) / zoom_factor),
                        (x_center + (x_range[1] - x_center) / zoom_factor)]
            new_y_range = [(y_center - (y_center - y_range[0]) / zoom_factor),
                        (y_center + (y_range[1] - y_center) / zoom_factor)]

        new_x_span = new_x_range[1] - new_x_range[0]
        new_y_span = new_y_range[1] - new_y_range[0]

        # Apply limits to x-axis
        if new_x_span < self.min_x_range:
            new_x_range = [x_center - self.min_x_range / 2, x_center + self.min_x_range / 2]
            
        elif new_x_span > self.max_x_range:
            new_x_range = [x_center - self.max_x_range / 2, x_center + self.max_x_range / 2]

        # Apply limits to y-axis
        if new_y_span < self.min_y_range:
            new_y_range = [y_center - self.min_y_range / 2, y_center + self.min_y_range / 2]
            
        elif new_y_span > self.max_y_range:
            new_y_range = [y_center - self.max_y_range / 2, y_center + self.max_y_range / 2]

        self.plot_graph.setXRange(new_x_range[0], new_x_range[1], padding=0)
        self.plot_graph.setYRange(new_y_range[0], new_y_range[1], padding=0)
        




# Start the application
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main = SignalCine()
    main.show()
    sys.exit(app.exec_())



#
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
# from PyQt5.QtCore import Qt, QPoint, QRect
# from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPen, QColor
#
#
# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.window_width, self.window_height = 1200, 800
#         self.setMinimumSize(self.window_width, self.window_height)
#
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#
#         self.pix = QPixmap(self.rect().size())
#         self.pix.fill(Qt.white)
#         # da hena initializes begin w destination to null points
#         self.begin, self.destination = QPoint(), QPoint()
#         self.rectangles = []
#         self.selected_rect = None
#
#         self.capture_button = QPushButton("capture", self)
#         self.capture_button.clicked.connect(self.capture_rectangle)
#         self.capture_button.hide()
#
#         self.delete_button = QPushButton("delete", self)
#         self.delete_button.clicked.connect(self.delete_rectangle)
#         self.delete_button.hide()
#
#
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.drawPixmap(QPoint(), self.pix)
#
#         for i, (rect, color, captured) in enumerate(self.rectangles):
#             if i == self.selected_rect:
#                 painter.setPen(QPen(Qt.blue, 2, Qt.DashLine))
#             else:
#                 painter.setPen(QPen(color, 2))
#
#             painter.setBrush(QBrush(color if captured else QColor(0, 0, 255, 50)))
#             painter.drawRect(rect.normalized())
#
#
#         if not self.begin.isNull() and not self.destination.isNull():
#             rect = QRect(self.begin, self.destination)
#             painter.setPen(QPen(QColor(0, 0, 255), 2))
#             painter.setBrush(QBrush(QColor(0, 0, 255, 50)))
#             painter.drawRect(rect.normalized())
#
#     def mousePressEvent(self, event):
#         click_on_rect = False
#         if event.buttons() & Qt.LeftButton:
#             clicked_point = event.pos()
#             for i, (rect, _, _) in enumerate(self.rectangles):
#                 if rect.contains(clicked_point):
#                     self.selected_rect = i
#                     click_on_rect = True
#                     self.show_buttons(clicked_point)
#
#             if not click_on_rect:
#                 self.begin = event.pos()
#                 self.destination = self.begin
#                 self.selected_rect = None
#                 self.capture_button.hide()
#                 self.delete_button.hide()
#
#             self.update()
#
#     def mouseMoveEvent(self, event):
#         if event.buttons() & Qt.LeftButton and self.begin:
#             self.destination = event.pos()
#             self.update()
#
#     def mouseReleaseEvent(self, event):
#         if event.button() & Qt.LeftButton and not self.selected_rect:
#             rect = QRect(self.begin, self.destination)
#             print(f'Starting Point: ({self.begin.x()}, {self.begin.y()}), Final Destination: ({self.destination.x()}, {self.destination.y()})')
#
#             if rect.width() >10 and rect.height()>10:
#                 self.rectangles.append((rect, QColor(0, 0, 255), False)) # false ely hwa msh captured lsa w yeb2a blue
#                 self.selected_rect = len(self.rectangles) - 1
#                 self.show_buttons(event.pos())
#
#
#             self.begin, self.destination = QPoint(), QPoint()
#             self.update()
#
#     # print(
#     #     f'Starting Point: ({self.begin.x()}, {self.begin.y()}), Final Destination: ({self.destination.x()}, {self.destination.y()})')
#     # painter.setPen(QPen(QColor(0, 255, 0), 2))
#     # painter.setBrush(QBrush(QColor(0, 255, 0, 50)))
#     # painter.drawRect(rect.normalized())
#
#     def show_buttons(self, pos):
#         self.capture_button.move(pos + QPoint(15, 30))
#         self.capture_button.show()
#         self. delete_button.move(pos+ QPoint(130, 30))
#         self.delete_button.show()
#
#
#     def capture_rectangle(self):
#         if self.selected_rect is not None:
#             rect, _, _ = self.rectangles[self.selected_rect]
#             self.rectangles[self.selected_rect] = (rect, QColor(0, 255, 0, 50), True) # false ely hwa captured
#             self.capture_button.hide()
#             self.delete_button.hide()
#             self.update()
#
#     def delete_rectangle(self):
#         if self.selected_rect is not None:
#             del self.rectangles[self.selected_rect]
#             self.capture_button.hide()
#             self.delete_button.hide()
#             self.selected_rect = None
#             self.update()
#
#
# if __name__ == '__main__':
#
#
#     app = QApplication(sys.argv)
#     app.setStyleSheet('''
# 		QWidget {
# 			font-size: 30px;
# 		}
# 	''')
#
#     myApp = MyApp()
#     myApp.show()
#
#     try:
#         sys.exit(app.exec_())
#     except SystemExit:
#         print('Closing Window...')
#
#
#
#
