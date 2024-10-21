from PyQt5.QtWidgets import  QColorDialog
from ChannelEditor import ChannelEditor
from SignalEditWindow import SignalEditor
from main import *
from PolarSignal import PolarWindow
from LiveSignal import DataFetcher
from ExportToPdf import ExportToPdf, save_image
import time
import threading
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout

class GlueOptions(QDialog):
    def __init__(self, portionx1, portiony1, portionx2, portiony2,gluedSignals, main_window):
        super().__init__()
        self.main_window = main_window
        self.portion_x1 = portionx1
        self.portion_y1 = portiony1
        self.portion_x2 = portionx2
        self.portion_y2 = portiony2
        self.interpolation_order = "linear"
        self.gluedSignals = gluedSignals
        self.glued_x = []
        self.glued_y = []
        self.setStyleSheet("background-color: #181818;")
        self.setFixedSize(800, 600)
        self.glued_count = 0

        # Main layout for the QDialog
        self.main_glue_options_layout = QVBoxLayout(self)
        shift_buttons_layout = QHBoxLayout()
        # glued_signal_layout = QHBoxLayout()
        # shift_amount_layout = QHBoxLayout()
        # update_shift_layout = QHBoxLayout()
        graph1_layout = QVBoxLayout()
        graph2_layout = QVBoxLayout()

        # Graph showing both signals
        self.plot_graph_glue_options = pg.PlotWidget()
        self.plot_graph_glue_options.showGrid(x=True, y=True)
        self.plot_graph_glue_options.setFixedHeight(200)
        graph1_layout.addWidget(self.plot_graph_glue_options)

        # Second graph for showing the glued signal
        self.plot_graph_glued_signal = pg.PlotWidget()
        self.plot_graph_glued_signal.setFixedHeight(200)
        self.plot_graph_glued_signal.showGrid(x=True, y=True)
        graph2_layout.addWidget(self.plot_graph_glued_signal)

        # Add the graph layouts to the main layout
        self.main_glue_options_layout.addLayout(graph1_layout)
        self.main_glue_options_layout.addLayout(graph2_layout)

        # Interpolation order label and combo box
        self.label_order = QLabel('Interpolation order:')
        self.combo_order = QComboBox(self)
        self.combo_order.addItems(['linear', 'cubic', 'quadratic'])
        self.combo_order.setStyleSheet(" background-color: gray; ")
        self.combo_order.setGeometry(40, 285, 110, 30)

        shift_buttons_layout.addWidget(self.label_order)
        shift_buttons_layout.addWidget(self.combo_order)

        # # Graph showing both signals
        # self.plot_graph_glue_options = pg.PlotWidget()
        # self.plot_graph_glue_options.showGrid(x=True, y=True)
        # self.main_glue_options_layout.addWidget(self.plot_graph_glue_options)

        # Buttons to shift signal 2 left and right
        shift_right_signal2_button = QPushButton("Shift Right", self)
        shift_right_signal2_button.setFixedSize(100, 30)
        shift_right_signal2_button.setGeometry(680, 285, 300, 300)
        shift_right_signal2_button.clicked.connect(self.shiftRightSignal2)
        shift_right_signal2_button.setStyleSheet("font-size: 20px; border-radius: 10px; background-color: white; ")
        shift_buttons_layout.addWidget(shift_right_signal2_button)

        shift_left_signal2_button = QPushButton("Shift Left", self)
        shift_left_signal2_button.setFixedSize(100, 30)
        shift_left_signal2_button.setGeometry(510, 285, 300, 300)
        shift_left_signal2_button.clicked.connect(self.shiftLeftSignal2)
        shift_left_signal2_button.setStyleSheet("font-size: 20px; border-radius: 10px; background-color: white;")
        shift_buttons_layout.addWidget(shift_left_signal2_button)

        # Button to show the glued signal
        show_glued_signal_button = QPushButton("Show Glued Signal", self)
        show_glued_signal_button.setFixedSize(170, 40)
        show_glued_signal_button.setGeometry(290, 550, 400, 400)
        show_glued_signal_button.clicked.connect(self.showGluedSignal)
        show_glued_signal_button.setStyleSheet("font-size: 20px; border-radius: 10px; background-color: white;")
        shift_buttons_layout.addWidget(show_glued_signal_button)
        save_glue_button = QPushButton("Save Signal", self)
        save_glue_button.setFixedSize(170, 40)
        save_glue_button.setGeometry(400, 550, 400, 400)
        # save_glue_button.clicked.connect(lambda: save_image(self.plot_graph_glued_signal))
        save_glue_button.clicked.connect(lambda: self.save_glue(self.plot_graph_glued_signal))

        # Input for shift amount
        self.shift_amount_input = QLineEdit(self)
        self.shift_amount_input.setPlaceholderText("1")
        self.shift_amount_input.setStyleSheet("background-color: white;")
        self.shift_amount_input.setFixedSize(30, 30)
        self.shift_amount_input.setGeometry(630, 285, 400, 400)
        shift_buttons_layout.addWidget(self.shift_amount_input)

        # # Second graph for showing the glued signal
        # self.plot_graph_glued_signal = pg.PlotWidget()
        # self.plot_graph_glued_signal.showGrid(x=True, y=True)
        # self.main_glue_options_layout.addWidget(self.plot_graph_glued_signal)


        # Plotting the signals
        self.line_signal1 = self.plot_graph_glue_options.plot(self.portion_x1, self.portion_y1,
                                                              pen=pg.mkPen(color="red", width=2.5))
        self.line_signal2 = self.plot_graph_glue_options.plot(self.portion_x2, self.portion_y2,
                                                              pen=pg.mkPen(color="blue", width=2.5))

        # Set the default shift amount
        self.shift_amount = 1

    def shiftRightSignal2(self):
        self.updateShiftAmount()
        self.portion_x2 = np.array(self.portion_x2) + self.shift_amount
        self.line_signal2.setData(self.portion_x2, self.portion_y2)

    def submit(self):
        interpolation_order = self.combo_order.currentText()
        self.interpolation_order = interpolation_order

    def shiftLeftSignal2(self):
        self.updateShiftAmount()
        self.portion_x2 = np.array(self.portion_x2) - self.shift_amount
        self.line_signal2.setData(self.portion_x2, self.portion_y2)

    def updateShiftAmount(self):
        new_shift_amount = float(self.shift_amount_input.text())
        self.shift_amount = new_shift_amount

    def signal_glue(self, portion_x1, portion_y1, portion_x2, portion_y2, order):
        portion_x1 = portion_x1.tolist()
        portion_x2 = portion_x2.tolist()
        portion_y1 = portion_y1.tolist()
        portion_y2 = portion_y2.tolist()

        interp_y_func = lambda arguments: None
        x_interp = []
        total_range = (abs(portion_x1[-1] - portion_x1[0])) + (abs(portion_x2[-1] - portion_x2[0]))

        print("signal 1 came first")
        print(portion_x1[0], portion_x2[0])

        if portion_x1[0] < portion_x2[0]:
            print("signal 1 el as8ar")
            gap = self.gap_or_overlap(total_range, portion_x1[0], portion_x2[-1])
            if gap:
                x_list = portion_x1 + portion_x2
                y_list = portion_y1 + portion_y2
                x_interp = np.linspace(portion_x1[-1] + 1e-6,
                                       portion_x2[0] - 1e-6)  # Make sure to use a consistent size
                interp_y_func = interp1d(x_list, y_list, kind=order)
                y_interp = interp_y_func(x_interp)

                # Use np.concatenate to ensure correct concatenation
                self.glued_x = np.concatenate([portion_x1, x_interp, portion_x2])
                self.glued_y = np.concatenate([portion_y1, y_interp, portion_y2])
                return self.glued_x, self.glued_y
            else:
                intersection = list(set(portion_x1) & set(portion_x2))
                x_list = portion_x1[:-len(intersection)] + portion_x2[len(intersection):]
                y_list = portion_y1[:-len(intersection)] + portion_y2[len(intersection):]
                x_interp = np.linspace(portion_x2[0] + 1e-6,
                                       portion_x1[-1] - 1e-6)  # Make sure to use a consistent size
                interp_y_func = interp1d(x_list, y_list, kind=order)
                y_interp = interp_y_func(x_interp)

                self.glued_x = np.concatenate(
                    [portion_x1[:-len(intersection)], x_interp, portion_x2[len(intersection):]])
                self.glued_y = np.concatenate(
                    [portion_y1[:-len(intersection)], y_interp, portion_y2[len(intersection):]])

                print(self.glued_x)
                return self.glued_x, self.glued_y

        elif portion_x2[0] < portion_x1[0]:
            print("signal 2 el as8ar")
            gap = self.gap_or_overlap(total_range, portion_x2[0], portion_x1[-1])
            if gap:
                x_list = portion_x2 + portion_x1
                y_list = portion_y2 + portion_y1
                x_interp = np.linspace(portion_x2[-1] + 1e-6, portion_x1[0] - 1e-6, num=100)
                interp_y_func = interp1d(x_list, y_list, kind=order)
                y_interp = interp_y_func(x_interp)

                self.glued_x = np.concatenate([portion_x2, x_interp, portion_x1])
                self.glued_y = np.concatenate([portion_y2, y_interp, portion_y1])
                return self.glued_x, self.glued_y
            else:
                intersection = list(set(portion_x1) & set(portion_x2))
                x_list = portion_x2[:-len(intersection)] + portion_x1[len(intersection):]
                y_list = portion_y2[:-len(intersection)] + portion_y1[len(intersection):]
                x_interp = np.linspace(portion_x1[0] + 1e-6,
                                       portion_x2[-1] - 1e-6)  # Make sure to use a consistent size
                interp_y_func = interp1d(x_list, y_list, kind=order)
                y_interp = interp_y_func(x_interp)

                self.glued_x = np.concatenate(
                    [portion_x1[:-len(intersection)], x_interp, portion_x2[len(intersection):]])
                self.glued_y = np.concatenate(
                    [portion_y1[:-len(intersection)], y_interp, portion_y2[len(intersection):]])

                print(self.glued_x)
                return self.glued_x, self.glued_y
    def save_glue(self, glued_plot_image):
        save_image(glued_plot_image)
        self.glued_count = self.glued_count + 1
        print("Glue Image Saved")



    def showGluedSignal(self):
        self.submit()
        size = 0
        self.glued_x, self.glued_y = self.signal_glue(self.portion_x1, self.portion_y1, self.portion_x2, self.portion_y2,
                                            self.interpolation_order)
        if len(self.glued_x) < len(self.glued_y):
            size = len(self.glued_x)
        else:
            size = len(self.glued_y)
        self.glued_x = self.glued_x[0:size]
        self.glued_y = self.glued_y[0: size]
        self.plot_graph_glued_signal.plot(self.glued_x, self.glued_y, pen=pg.mkPen(color="green", width=2.5))

    def gap_or_overlap(self, range, begin, end):
        gap = False
        if abs(end - begin) >= range:
            gap = True
        return gap
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("UI setup complete")  # Add this line
        if hasattr(self.ui, 'glueButton'):
            print("Glue button exists")  # Add this line
            self.ui.glueButton.setEnabled(True)
            self.ui.glueButton.clicked.connect(self.glue_options)
            print("Glue button connected")  # Add this line
        else:
            print("Glue button does not exist")  # Add this line
        self.portion_x1 = []
        self.portion_y1 = []
        self.portion_x2 = []
        self.portion_y2 = []
        self.toBeGluedSignals = []

        self.begin, self.destination = QPoint(), QPoint()
        self.rectangles = []
        self.selected_rect = None
        self.captured_cnt = 0
        self.temp_rect = None
        self.capture_button = QPushButton("capture", self)
        self.capture_button.clicked.connect(self.capture_rectangle)
        self.capture_button.hide()

        self.delete_button = QPushButton("delete", self)
        self.delete_button.clicked.connect(self.delete_rectangle)
        self.delete_button.hide()
    def mousePressEvent(self, event):
        click_on_rect = False
        if event.buttons() & Qt.LeftButton:
            clicked_point = event.pos()
            for i, (rect_frame, captured) in enumerate(self.rectangles):
                if rect_frame.geometry().contains(clicked_point):
                    self.selected_rect = i
                    click_on_rect = True
                    self.show_buttons(clicked_point)

            if not click_on_rect:
                self.begin = event.pos()
                self.destination = self.begin
                self.selected_rect = None
                self.capture_button.hide()
                self.delete_button.hide()
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.begin and self.captured_cnt < 2:
            self.destination = event.pos()
            self.update_temp_rectangle()
    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton and not self.selected_rect:
            rect = QRect(self.begin, self.destination)
            if rect.width() > 10 and rect.height() > 10:
                self.create_rectangle(rect)
                self.selected_rect = len(self.rectangles) - 1
                self.show_buttons(event.pos())
            self.update()
    def update_temp_rectangle(self):
        if hasattr(self, 'temp_frame'):
            self.temp_frame.setGeometry(QRect(self.begin, self.destination).normalized())
        else:
            self.temp_frame = QFrame(self)
            self.temp_frame.setGeometry(QRect(self.begin, self.destination).normalized())
            self.temp_frame.setStyleSheet("background-color: rgba(0, 0, 255, 50); border: 2px solid blue;")
            self.temp_frame.show()
    def create_rectangle(self, rect):
        if hasattr(self, 'temp_frame'):
            self.temp_frame.setParent(None)
            del self.temp_frame

        rect_frame = QFrame(self)
        rect_frame.setGeometry(rect.normalized())
        rect_frame.setStyleSheet("background-color: rgba(0, 0, 255, 50); border: 2px dashed blue;")
        rect_frame.show()

        self.rectangles.append((rect_frame, False))
    def show_buttons(self, pos):
        print("iam in the showwwww")
        self.capture_button.move(pos + QPoint(15, 30))
        self.capture_button.show()
        self.capture_button.raise_()
        self. delete_button.move(pos+ QPoint(130, 30))
        self.delete_button.show()
        self.delete_button.raise_()

    def determine_viewer(self, rect):

        rect_center= rect.y()

        ch1_center = self.ui.Channel1Viewer.geometry().y()
        ch2_center = self.ui.Channel2Viewer.geometry().y()


        # Return the viewer with the most overlap
        if abs(rect_center-ch1_center) < abs(rect_center-ch2_center):
            return self.ui.Channel1Viewer
        else:
            return self.ui.Channel2Viewer

    def capture_rectangle(self):
        if self.selected_rect is not None and self.captured_cnt < 2:
            rect_frame, captured = self.rectangles[self.selected_rect]
            rect_frame.setStyleSheet("background-color: rgba(0, 255, 0, 50); border: 2px solid green;")
            self.rectangles[self.selected_rect] = (rect_frame, True)

            # Determine which viewer the rectangle belongs to
            rect = QRect(self.begin, self.destination).normalized()
            current_viewer = self.determine_viewer(rect)

            self.captured_cnt += 1
            if self.captured_cnt == 1:
                self.portion_x1, self.portion_y1 = self.get_intersection(self.begin.x(), self.destination.x(),
                                                                         current_viewer)
                print(f" captured end{self.portion_x1[-1]}, begin {self.portion_x1[0]}")

            elif self.captured_cnt == 2:
                self.portion_x2, self.portion_y2 = self.get_intersection(self.begin.x(), self.destination.x(),
                                                                         current_viewer)
                print(f" captured end{self.portion_x2[-1]}, begin {self.portion_x2[0]}")

            self.begin, self.destination = QPoint(), QPoint()
            self.capture_button.hide()
            self.delete_button.hide()

            self.update()
    def delete_rectangle(self):
        if self.selected_rect is not None:
            rect_frame, captured = self.rectangles[self.selected_rect]
            if captured:
                self.captured_cnt -= 1
            rect_frame.setParent(None)
            del self.rectangles[self.selected_rect]
            self.capture_button.hide()
            self.delete_button.hide()
            self.selected_rect = None

    def get_intersection(self, x1Rectangle, x2Rectangle, current_viewer):
        min_old_range_window, max_old_range_window = 0, self.ui.width()
        min_new_range_x_axis, max_new_range_x_axis = current_viewer.plot_graph.getAxis('bottom').range

        mapped_x1_rect = ((x1Rectangle - min_old_range_window) / (max_old_range_window - min_old_range_window)) * (
                max_new_range_x_axis - min_new_range_x_axis) + min_new_range_x_axis
        mapped_x2_rect = ((x2Rectangle - min_old_range_window) / (max_old_range_window - min_old_range_window)) * (
                max_new_range_x_axis - min_new_range_x_axis) + min_new_range_x_axis

        signal = current_viewer.signalsChannel[-1]  # we need to determine which signal we will take the glaw of it
        self.toBeGluedSignals.append(signal)
        signal_xdata = signal.x
        signal_ydata = signal.y
        initial_index, final_index = 0, 0
        for i, pnt in enumerate(signal_xdata):
            if pnt >= mapped_x1_rect and not initial_index:
                initial_index = i
            if pnt >= mapped_x2_rect:
                final_index = i
                break
        portion_datax = signal_xdata[initial_index: final_index]
        portion_datay = signal_ydata[initial_index: final_index]
        print(f" inter end{portion_datax[-1]}, begin {portion_datax[0]}")
        return portion_datax , portion_datay


    def glue_options(self):
        print("Glue options method called in MyMainWindow")
        if hasattr(self, 'portion_x1') and hasattr(self, 'portion_y1') and hasattr(self, 'portion_x2') and hasattr(self, 'portion_y2'):
            print("Portions are available")
            glue_window = GlueOptions(self.portion_x1, self.portion_y1, self.portion_x2, self.portion_y2,self.toBeGluedSignals, self)
            glue_window.exec_()


class Ui_MainWindow(QtWidgets.QMainWindow):
        def setupUi(self, MainWindow):

                #Window Setup
                app_icon =  QtGui.QIcon('../Deliverables/app icon.png')
                MainWindow.setWindowIcon(app_icon)
                MainWindow.setObjectName("Signal Viewer")
                MainWindow.setFixedSize(1379, 870)
                MainWindow.setMouseTracking(False)
                MainWindow.setStyleSheet("\n"
        "background-color: rgb(42, 42, 42);")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")

                self.signalEditingWindows = []
                self.signals = [];
                self.signalID = 0;
                self.signalEditorID=0;
                self.isSyncEnabled = False 

                # LIVE SIGNAL VARIABLES
                self.thread = None
                self.fetch_subscriber_count = DataFetcher()
                self.fetch_subscriber_count.live_signal.connect(self.update_count)
                self.timestamps = []
                self.subscriber_counts = []
                self.start_time = time.time()


                self.horizontalSliderChannel1 = QtWidgets.QSlider(self.centralwidget)
                self.horizontalSliderChannel1.setGeometry(QtCore.QRect(390, 410, 611, 16))
                self.horizontalSliderChannel1.setStyleSheet("QSlider::groove:horizontal {\n"
                                                            "    height: 5px;\n"
                                                            "    background: white;  \n"
                                                            "    border-radius: 3px;    \n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider::handle:horizontal {\n"
                                                            "    background: #000000;  \n"
                                                            "    border: 1px solid #333333;\n"
                                                            "    width: 10px;\n"
                                                            "    height: 10px;\n"
                                                            "    border-radius: 6px;    \n"
                                                            "    margin: -4px 0;       \n"
                                                            "}\n"
                                                            "")
                self.horizontalSliderChannel1.setOrientation(QtCore.Qt.Horizontal)
                self.horizontalSliderChannel1.setObjectName("horizontalSliderChannel1")

                self.verticalSliderChannel1 = QtWidgets.QSlider(self.centralwidget)

                self.verticalSliderChannel1.setGeometry(QtCore.QRect(1050, 110, 16, 261))
                self.verticalSliderChannel1.setStyleSheet("QSlider::groove:vertical {\n"
                                                          "    width: 6px;\n"
                                                          "    background: white;  \n"
                                                          "    border-radius: 3px;   \n"
                                                          "}\n"
                                                          "\n"
                                                          "QSlider::handle:vertical {\n"
                                                          "    background: #000000;   \n"
                                                          "    border: 1px solid #333333;\n"
                                                          "    width: 10px;\n"
                                                          "    height: 10px;\n"
                                                          "    border-radius: 5px;    \n"
                                                          "    margin: 0 -4px;       \n"
                                                          "}\n"
                                                          "")
                self.verticalSliderChannel1.setOrientation(QtCore.Qt.Vertical)
                self.verticalSliderChannel1.setObjectName("verticalSliderChannel1")
                # Channel 2 controls
                self.verticalSliderChannel2 = QtWidgets.QSlider(self.centralwidget)
                self.verticalSliderChannel2.setGeometry(QtCore.QRect(1050, 510, 16, 261))
                self.verticalSliderChannel2.setStyleSheet("QSlider::groove:vertical {\n"
                                                          "    width: 6px;\n"
                                                          "    background: white;  \n"
                                                          "    border-radius: 3px;   \n"
                                                          "}\n"
                                                          "\n"
                                                          "QSlider::handle:vertical {\n"
                                                          "    background: #000000;   \n"
                                                          "    border: 1px solid #333333;\n"
                                                          "    width: 10px;\n"
                                                          "    height: 10px;\n"
                                                          "    border-radius: 5px;    \n"
                                                          "    margin: 0 -4px;       \n"
                                                          "}\n"
                                                          "")
                self.verticalSliderChannel2.setOrientation(QtCore.Qt.Vertical)
                self.verticalSliderChannel2.setObjectName("verticalSliderChannel2")
                self.horizontalSliderChannel2 = QtWidgets.QSlider(self.centralwidget)
                self.horizontalSliderChannel2.setGeometry(QtCore.QRect(390, 810, 611, 16))
                self.horizontalSliderChannel2.setStyleSheet("QSlider::groove:horizontal {\n"
                                                            "    height: 5px;\n"
                                                            "    background: white;  \n"
                                                            "    border-radius: 3px;    \n"
                                                            "}\n"
                                                            "\n"
                                                            "QSlider::handle:horizontal {\n"
                                                            "    background: #000000;  \n"
                                                            "    border: 1px solid #333333;\n"
                                                            "    width: 10px;\n"
                                                            "    height: 10px;\n"
                                                            "    border-radius: 6px;    \n"
                                                            "    margin: -4px 0;       \n"
                                                            "}\n"
                                                            "")
                self.horizontalSliderChannel2.setOrientation(QtCore.Qt.Horizontal)
                self.horizontalSliderChannel2.setObjectName("horizontalSliderChannel2")

                #Channel Viewer Setup
                self.Channel1Viewer = SignalCine(self.centralwidget,290, 100, 731, 281,self.horizontalSliderChannel1,self.verticalSliderChannel1)
                self.Channel2Viewer = SignalCine(self.centralwidget,290, 500, 731, 281,self.horizontalSliderChannel2,self.verticalSliderChannel2)


                self.Channel1Editor = ChannelEditor(self.centralwidget, 1090, 100, 261, 281, "Channel 1", self.Channel1Viewer)
                self.Channel2Editor = ChannelEditor(self.centralwidget, 1090, 500, 261, 281, "Channel 2", self.Channel2Viewer)

                #signal controls
                self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
                self.scrollArea.setGeometry(QtCore.QRect(0, 60, 271, 800))
                self.scrollArea.setWidgetResizable(True)  # Ensure the scroll area resizes automatically
                self.scrollArea.setStyleSheet("background-color: rgb(42, 42, 42); border:0px;")
                scrollbar = QScrollBar()
                scrollbar.setStyleSheet("""
            QScrollBar:vertical {
                border: 1px solid #999999;
                background: #f9f9f9;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
            }
        """)
                self.scrollArea.setVerticalScrollBar(scrollbar)
                self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

                self.scrollAreaWidgetContents = QtWidgets.QWidget()
                self.scrollAreaWidgetContents.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)

                self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
                self.scrollArea.setWidget(self.scrollAreaWidgetContents)
                
                
                # self.Signal1EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 1")
                # self.Signal2EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 2")
                # self.Signal3EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 3")
                # self.Signal4EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 4")
                # self.Signal5EditingWindow = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 251, "Signal 5")


                # # Add them to the layout
                # self.verticalLayout.addWidget(self.Signal1EditingWindow)
                # self.verticalLayout.addWidget(self.Signal2EditingWindow)
                # self.verticalLayout.addWidget(self.Signal3EditingWindow)
                # self.verticalLayout.addWidget(self.Signal4EditingWindow)
                # self.verticalLayout.addWidget(self.Signal5EditingWindow)


                



                #Taskbar Setup
                self.TaskBar = QtWidgets.QFrame(self.centralwidget)
                self.TaskBar.setGeometry(QtCore.QRect(-1, 0, 1381, 51))
                self.TaskBar.setStyleSheet("background-color: rgb(24, 24, 24);")
                self.TaskBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.TaskBar.setFrameShadow(QtWidgets.QFrame.Raised)
                self.TaskBar.setObjectName("TaskBar")
                self.UploadButton = QtWidgets.QPushButton(self.TaskBar)
                self.UploadButton.setGeometry(QtCore.QRect(350, 10, 121, 28))
                self.UploadButton.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font-size: 15px;\n"
        "background-color:transparent;\n"
        "font-weight:800;")
                icon5 = QtGui.QIcon()
                icon5.addPixmap(QtGui.QPixmap("../Deliverables/downloads.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.UploadButton.setIcon(icon5)
                self.UploadButton.setIconSize(QtCore.QSize(20, 20))
                self.UploadButton.setObjectName("UploadButton")
                self.UploadButton.clicked.connect(self.createSignalEditor)

                # LIVE SIGNAL BUTTONS

                self.ConnectToWebsite = QtWidgets.QPushButton(self.TaskBar)
                self.ConnectToWebsite.setGeometry(QtCore.QRect(500, 10, 171, 28))
                self.ConnectToWebsite.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font-size: 15px;\n"
        "background-color:transparent;\n"
        "font-weight:800;")
                self.ConnectToWebsite.clicked.connect(lambda: self.live_connection('connect'))
                icon6 = QtGui.QIcon()
                icon6.addPixmap(QtGui.QPixmap("../Deliverables/world-wide-web.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ConnectToWebsite.setIcon(icon6)

                self.DisconnectFromWebsite = QtWidgets.QPushButton(self.TaskBar)
                self.DisconnectFromWebsite.setGeometry(QtCore.QRect(670, 10, 171, 28))
                self.DisconnectFromWebsite.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                    "font-size: 15px;\n"
                                                    "background-color:transparent;\n"
                                                    "font-weight:800;")
                self.DisconnectFromWebsite.clicked.connect(lambda: self.live_connection('disconnect'))
                icon12 = QtGui.QIcon()
                icon12.addPixmap(QtGui.QPixmap(
                    "../Deliverables/disconnect_icon.png"),
                                QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.DisconnectFromWebsite.setIcon(icon12)
                #

                self.DisconnectFromWebsite.setIconSize(QtCore.QSize(20, 20))
                self.DisconnectFromWebsite.setObjectName("DisconnectFromWebsite")
                self.ExportButton = QtWidgets.QPushButton(self.TaskBar)
                self.ExportButton.setGeometry(QtCore.QRect(860, 10, 141, 31))
                self.ExportButton.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font-size: 15px;\n"
        "background-color:transparent;\n"
        "font-weight:800;")

                self.ExportButton.clicked.connect(lambda: self.save_report(GlueOptions.glue_window.gluedSignals[0],self.gluedSignals[1]),
                                                  self.glued_count)
                icon7 = QtGui.QIcon()
                icon7.addPixmap(QtGui.QPixmap("../Deliverables/share (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ExportButton.setIcon(icon7)
                self.ExportButton.setIconSize(QtCore.QSize(20, 20))
                self.ExportButton.setObjectName("ExportButton")

                self.Separator = QtWidgets.QFrame(self.centralwidget)
                self.Separator.setGeometry(QtCore.QRect(290, 450, 750, 20))
                self.Separator.setStyleSheet("color: rgb(255, 255, 255);")
                self.Separator.setFrameShape(QtWidgets.QFrame.HLine)
                self.Separator.setFrameShadow(QtWidgets.QFrame.Sunken)
                self.Separator.setObjectName("separator")

                #Channel 1 controls
                self.PlayChannel1 = QtWidgets.QPushButton(self.centralwidget)
                self.PlayChannel1.setGeometry(QtCore.QRect(300, 400, 31, 31))
                self.PlayChannel1.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font-size: 15px;\n"
        "background-color:rgb(24,24,24);\n"
        "font-weight:800;\n"
        "border-radius: 15px;")
                self.PlayChannel1.setText("")
                icon8 = QtGui.QIcon()
                icon8.addPixmap(QtGui.QPixmap("../Deliverables/play-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.PlayChannel1.setIcon(icon8)
                self.PlayChannel1.setIconSize(QtCore.QSize(25, 25))
                self.PlayChannel1.setObjectName("PlayChannel1")
                self.PlayChannel1.clicked.connect(self.Channel1Viewer.playSignal)

                self.PauseChannel1 = QtWidgets.QPushButton(self.centralwidget)
                self.PauseChannel1.setGeometry(QtCore.QRect(340, 400, 31, 31))
                self.PauseChannel1.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font-size: 15px;\n"
        "background-color:rgb(24,24,24);\n"
        "font-weight:800;\n"
        "border-radius: 15px;")
                self.PauseChannel1.setText("")
                icon9 = QtGui.QIcon()
                icon9.addPixmap(QtGui.QPixmap("../Deliverables/video-pause-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.PauseChannel1.setIcon(icon9)
                self.PauseChannel1.setIconSize(QtCore.QSize(25, 25))
                self.PauseChannel1.setObjectName("PauseChannel1")
                self.PauseChannel1.clicked.connect(self.Channel1Viewer.pauseSignal)

                self.LinkChannels = QtWidgets.QPushButton(self.centralwidget)
                self.LinkChannels.setGeometry(QtCore.QRect(1080, 425, 141, 41))
                self.LinkChannels.setStyleSheet("background-color: rgb(24, 24, 24);\n"
        "color: rgb(255, 255, 255);\n"
        "border: 1px;\n"
        "border-radius: 20px;\n"
        "font-weight:800;")
                self.icon10 = QtGui.QIcon()
                self.icon10.addPixmap(QtGui.QPixmap("D:\\College\\Third year\\First Term\\DSP\\Tasks\\Task 1\\Signal-Viewer\\GUI\\Deliverables/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.LinkChannels.setIcon(self.icon10)
                self.LinkChannels.setCheckable(True)
                self.LinkChannels.setObjectName("LinkChannels")
                self.LinkChannels.toggled.connect(self.linkTwoChannels)

                self.glueButton = QtWidgets.QPushButton(self.centralwidget)
                self.glueButton.setGeometry(QtCore.QRect(1225, 425, 131, 41))
                self.glueButton.setStyleSheet("background-color: rgb(24, 24, 24);\n"
        "color: rgb(255, 255, 255);\n"
        "border: 1px;\n"
        "border-radius: 20px;\n"
        "font-weight:800;")
                icon11 = QtGui.QIcon()
                icon11.addPixmap(QtGui.QPixmap("../Deliverables/glue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.glueButton.setIcon(icon11)
                self.glueButton.setObjectName("GlueButton")
                self.glueButton.clicked.connect(MainWindow.glue_options)


                self.PauseChannel2 = QtWidgets.QPushButton(self.centralwidget)
                self.PauseChannel2.setGeometry(QtCore.QRect(340, 800, 31, 31))
                self.PauseChannel2.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font-size: 15px;\n"
        "background-color:rgb(24,24,24);\n"
        "font-weight:800;\n"
        "border-radius: 15px;")
                self.PauseChannel2.setText("")
                self.PauseChannel2.setIcon(icon9)
                self.PauseChannel2.setIconSize(QtCore.QSize(25, 25))
                self.PauseChannel2.setObjectName("PauseChannel2")
                self.PauseChannel2.clicked.connect(self.Channel2Viewer.pauseSignal)

                self.PlayChannel2 = QtWidgets.QPushButton(self.centralwidget)
                self.PlayChannel2.setGeometry(QtCore.QRect(300, 800, 31, 31))
                self.PlayChannel2.setStyleSheet("color: rgb(255, 255, 255);\n"
        "font-size: 15px;\n"
        "background-color:rgb(24,24,24);\n"
        "font-weight:800;\n"
        "border-radius: 15px;")
                self.PlayChannel2.setText("")
                self.PlayChannel2.setIcon(icon8)
                self.PlayChannel2.setIconSize(QtCore.QSize(25, 25))
                self.PlayChannel2.setObjectName("PlayChannel2")
                self.PlayChannel2.clicked.connect(self.Channel2Viewer.playSignal)
                
                
                self.Channel1Viewer.raise_()
                self.Channel1Editor.raise_()
                # self.Channel2Viewer.raise_()
                self.TaskBar.raise_()
                self.Separator.raise_()
                self.PlayChannel1.raise_()
                self.PauseChannel1.raise_()
                self.horizontalSliderChannel1.raise_()
                self.verticalSliderChannel1.raise_()
                self.LinkChannels.raise_()
                self.verticalSliderChannel2.raise_()
                self.horizontalSliderChannel2.raise_()
                self.PauseChannel2.raise_()
                self.PlayChannel2.raise_()
                self.Channel2Editor.raise_()
                MainWindow.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)
        def temp_glue_function(self):
            print("iam the clicked that in the ui main window")
        def update_temp_rectangle(self):
            if hasattr(self, 'temp_frame'):
                self.temp_frame.setGeometry(QRect(self.begin, self.destination).normalized())
            else:
                self.temp_frame = QFrame(self)
                self.temp_frame.setGeometry(QRect(self.begin, self.destination).normalized())
                self.temp_frame.setStyleSheet("background-color: rgba(0, 0, 255, 50); border: 2px solid blue;")
                self.temp_frame.show()

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "Signal Viewer"))
                self.UploadButton.setText(_translate("MainWindow", "Upload File"))
                self.ConnectToWebsite.setText(_translate("MainWindow", "Connect to website"))
                self.DisconnectFromWebsite.setText(_translate("MainWindow", "Disconnect"))
                self.ExportButton.setText(_translate("MainWindow", "Export to PDF"))
                self.LinkChannels.setText(_translate("MainWindow", " Link channels"))
                self.glueButton.setText(_translate("MainWindow","Combine"))
                
        def linkTwoChannels(self,checked):
                self.isSyncEnabled = checked
                if checked:
                        # Button is toggled ON

                        self.LinkChannels.setStyleSheet("background-color: green;\n"
                                                        "color: white;\n"
                                                        "border: 1px;\n"
                                                        "border-radius: 20px;\n"
                                                        "font-weight:800;")
                        # Change icon when toggled ON (if you have a different icon for this state)
                        iconOn = QtGui.QIcon()
                        iconOn.addPixmap(QtGui.QPixmap("../Deliverables/unlink.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        self.LinkChannels.setIcon(iconOn)
                        self.LinkChannels.setText("Unlink channels")
                        self.Channel1Viewer.rewindSignal()
                        self.Channel2Viewer.rewindSignal()

                        # Disconnect any existing connections from Play/Pause buttons
                        self.PlayChannel1.clicked.disconnect()
                        self.PlayChannel2.clicked.disconnect()
                        self.PauseChannel1.clicked.disconnect()
                        self.PauseChannel2.clicked.disconnect()
                        self.Channel1Editor.zoomInButton.clicked.disconnect()
                        self.Channel1Editor.zoomOutButton.clicked.disconnect()
                        self.Channel2Editor.zoomInButton.clicked.disconnect()
                        self.Channel2Editor.zoomOutButton.clicked.disconnect()
                        self.Channel1Editor.RewindButton.clicked.disconnect()
                        self.Channel2Editor.RewindButton.clicked.disconnect()
                        self.Channel1Editor.SpeedSlider.valueChanged.disconnect()
                        self.Channel2Editor.SpeedSlider.valueChanged.disconnect()

                        # Connect to the linked play/pause functions
                        # Connect to the wrapped play/pause functions
                        self.PlayChannel1.clicked.connect(self.wrappedPlay)
                        self.PlayChannel2.clicked.connect(self.wrappedPlay)
                        self.PauseChannel1.clicked.connect(self.wrappedPause)
                        self.PauseChannel2.clicked.connect(self.wrappedPause)
                        
                        self.Channel1Editor.zoomInButton.clicked.connect(self.wrappedZoomIn)
                        self.Channel1Editor.zoomOutButton.clicked.connect(self.wrappedZoomOut)
                        self.Channel2Editor.zoomInButton.clicked.connect(self.wrappedZoomIn)
                        self.Channel2Editor.zoomOutButton.clicked.connect(self.wrappedZoomOut)
                        self.Channel1Editor.RewindButton.clicked.connect(self.wrappedRewind)
                        self.Channel2Editor.RewindButton.clicked.connect(self.wrappedRewind)
                        
                        self.Channel1Editor.SpeedSlider.valueChanged.connect(self.syncSliders)
                        self.Channel2Editor.SpeedSlider.valueChanged.connect(self.syncSliders)

                else:
                        # Button is toggled OFF (revert to original state)
                        self.LinkChannels.setStyleSheet("background-color: rgb(24, 24, 24);\n"
                                                        "color: rgb(255, 255, 255);\n"
                                                        "border: 1px;\n"
                                                        "border-radius: 20px;\n"
                                                        "font-weight:800;")
                        # Revert to the original icon
                        self.LinkChannels.setIcon(self.icon10)
                        self.LinkChannels.setText("link channels")
                        self.Channel1Viewer.rewindSignal()
                        self.Channel2Viewer.rewindSignal()

                        self.PlayChannel1.clicked.disconnect()
                        self.PlayChannel2.clicked.disconnect()
                        self.PauseChannel1.clicked.disconnect()
                        self.PauseChannel2.clicked.disconnect()
                        self.Channel1Editor.zoomInButton.clicked.disconnect()
                        self.Channel1Editor.zoomOutButton.clicked.disconnect()
                        self.Channel2Editor.zoomInButton.clicked.disconnect()
                        self.Channel2Editor.zoomOutButton.clicked.disconnect()
                        self.Channel1Editor.RewindButton.clicked.disconnect()
                        self.Channel2Editor.RewindButton.clicked.disconnect()
                        self.Channel1Editor.SpeedSlider.valueChanged.disconnect()
                        self.Channel2Editor.SpeedSlider.valueChanged.disconnect()
                        
                        self.PlayChannel1.clicked.connect(self.Channel1Viewer.playSignal)
                        self.PlayChannel2.clicked.connect(self.Channel2Viewer.playSignal)
                        self.PauseChannel1.clicked.connect(self.Channel1Viewer.pauseSignal)
                        self.PauseChannel2.clicked.connect(self.Channel2Viewer.pauseSignal)

                        self.Channel1Editor.zoomInButton.clicked.connect(lambda: self.Channel1Viewer.zoom(zoomIn=True))
                        self.Channel1Editor.zoomOutButton.clicked.connect(lambda: self.Channel1Viewer.zoom(zoomIn=False))
                        self.Channel2Editor.zoomInButton.clicked.connect(lambda: self.Channel2Viewer.zoom(zoomIn=True))
                        self.Channel2Editor.zoomOutButton.clicked.connect(lambda: self.Channel2Viewer.zoom(zoomIn=False))
                        self.Channel1Editor.RewindButton.clicked.connect(self.Channel1Viewer.rewindSignal)
                        self.Channel2Editor.RewindButton.clicked.connect(self.Channel2Viewer.rewindSignal)
                        self.Channel1Editor.SpeedSlider.valueChanged.connect(self.Channel1Viewer.changeSpeed)
                        self.Channel2Editor.SpeedSlider.valueChanged.connect(self.Channel2Viewer.changeSpeed)


        def wrappedPlay(self):
        
                self.Channel1Viewer.playSignal()
                self.Channel2Viewer.playSignal()
        def wrappedPause(self):
        
                self.Channel1Viewer.pauseSignal()
                self.Channel2Viewer.pauseSignal()

        def wrappedZoomIn(self):
               self.Channel1Viewer.zoom(zoomIn=True)
               self.Channel2Viewer.zoom(zoomIn=True)

        def wrappedZoomOut(self):
               self.Channel1Viewer.zoom(zoomIn=False)
               self.Channel2Viewer.zoom(zoomIn=False)
        
        def wrappedRewind(self):
               self.Channel1Viewer.rewindSignal()
               self.Channel2Viewer.rewindSignal()

        

        def syncSliders(self, value):
                
                print(f"syncSliders called with value: {value}, isSyncEnabled: {self.isSyncEnabled}")
                if self.isSyncEnabled:
                        sender = self.sender()
                        if sender == self.Channel1Editor.SpeedSlider:
                                self.Channel2Editor.SpeedSlider.blockSignals(True)
                                self.Channel2Editor.SpeedSlider.setValue(value)
                                self.Channel2Editor.SpeedSlider.blockSignals(False)
                        elif sender == self.Channel2Editor.SpeedSlider:
                                self.Channel1Editor.SpeedSlider.blockSignals(True)
                                self.Channel1Editor.SpeedSlider.setValue(value)
                                self.Channel1Editor.SpeedSlider.blockSignals(False)
                        self.wrappedChangeSpeed(value)

        def wrappedChangeSpeed(self,value):

                # Apply the speed change to both viewers
               self.Channel1Viewer.changeSpeed(value)
               self.Channel2Viewer.changeSpeed(value)

        def createSignalEditor(self):
               
               signal = self.Channel1Viewer.uploadSignal()
               if signal is not None:
                        self.signalID+=1
                        self.signalEditorID+=1
                        self.signals.append(signal)
                        signalEditor = SignalEditor(self.scrollAreaWidgetContents, 0, 0, 231, 350, f"Signal {str(self.signalID)}",self.signalEditorID)
                        self.verticalLayout.addWidget(signalEditor)
                        self.signalEditingWindows.append(signalEditor)
                        signalEditor.setVisible(True)
                        self.scrollArea.update()
                        # self.scrollArea.adjustSize()
                        # self.scrollAreaWidgetContents.updateGeometry()
                        # self.scrollArea.updateGeometry()
                        # self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

               signalEditor.ColorButton.clicked.connect(lambda : self.changeColor(signalEditor.ID))
               signalEditor.renameTextField.returnPressed.connect(lambda : self.rename(signalEditor.ID))
               signalEditor.nonpolarButton.clicked.connect(lambda: self.show_polar_view(signal.x, signal.y, signal.name, signal.color)) # From Nada
               signalEditor.channel1Checkbox.setChecked(True)
               signalEditor.channel1Checkbox.stateChanged.connect(lambda state, s_id=signal.signalId: self.selectChannel1StateChanged(s_id, state))
               signalEditor.channel2Checkbox.stateChanged.connect(lambda state, s_id=signal.signalId: self.selectChannel2StateChanged(s_id, state))

        def selectChannel1StateChanged(self, id, state):
                if state == Qt.Unchecked:  # ch 1 is unchecked
                        for signal in self.Channel1Viewer.signalsChannel:
                                if signal.signalId == id:
                                        self.Channel1Viewer.plot_graph.removeItem(signal.line)  # remove from ch 1
                                        signal.showSignal = False
                                        break
                elif state == Qt.Checked:  # ch 1 is checked
                        for signal in self.Channel1Viewer.signalsChannel:
                                if signal.signalId == id and signal.line not in self.Channel1Viewer.plot_graph.listDataItems():
                                        signal.line.setData(signal.time, signal.magnitude)  # reshow the signal
                                        self.Channel1Viewer.plot_graph.addItem(signal.line)  # readd to the plot
                                        signal.showSignal = True
                                        break

        def selectChannel2StateChanged(self, id, state):
                signalRelated2Id = None
                if state == Qt.Checked:  # ch 2 is checked
                        for signal in self.Channel2Viewer.signalsChannel:
                                if signal.signalId == id and signal.line not in self.Channel2Viewer.plot_graph.listDataItems():  # then it was existed so we need to reshoe
                                        signal.line.setData(signal.time, signal.magnitude)  # reshow the signal in Plot
                                        signal.showSignal = True
                                        self.Channel2Viewer.plot_graph.addItem(signal.line)
                                        return
                        for signal in self.Channel1Viewer.signalsChannel:  # here there is no id with that , so we need to create new signal object
                                if signal.signalId == id:
                                        signalRelated2Id = signal
                                        break
                        if signalRelated2Id is not None:
                                signal = SignalObject(signalRelated2Id.x, signalRelated2Id.y, (self.Channel2Viewer).plot_graph,
                                                      signalRelated2Id.color,
                                                      signalRelated2Id.name, id)
                                self.Channel2Viewer.plot_graph.addItem(signal.line)
                                self.Channel2Viewer.signalsChannel.append(signal)
                                self.signals.append(signal)
                                signal.showSignal = True


                                yMin, yMax = min(signalRelated2Id.y), max(signalRelated2Id.y)
                                self.Channel2Viewer.plot_graph.plotItem.vb.setLimits(xMin=0, xMax=signalRelated2Id.x[-1], yMin=yMin,
                                                                       yMax=yMax)
                                self.Channel2Viewer.playSignal()

                else:  # ch2 2 is unchecked
                        for signal in self.Channel2Viewer.signalsChannel:
                                if signal.signalId == id:
                                        self.Channel2Viewer.plot_graph.removeItem(signal.line)  # remove from ch 2
                                        signal.showSignal = False
                                        break


        def rename(self,signalEditorId):
                signal = None
                entered_text = None
                for signal in self.Channel1Viewer.signalsChannel:
                      if signal.signalId == signalEditorId:
                             signalEditor = self.signalEditingWindows[signal.signalId-1]
                             entered_text = signalEditor.renameTextField.text()
                             if entered_text.strip():
                                signal.label = entered_text
                                signalEditor.SignalLabel.setText(entered_text)
                                signal.rename_signal(entered_text)
                                break
                for signal in self.Channel2Viewer.signalsChannel:
                      if signal.signalId == signalEditorId:
                             signalEditor = self.signalEditingWindows[signal.signalId-1]
                             entered_text = signalEditor.renameTextField.text()
                             if entered_text.strip():
                                signal.label = entered_text
                                signalEditor.SignalLabel.setText(entered_text)
                                signal.rename_signal(entered_text)
                                break
                             
                # for i, plot_item in enumerate(signal.plot_widget.listDataItems()):
                #         if (plot_item.getData()[1] == signal.y[:len(plot_item.getData()[1])]).all():
                #                 if entered_text.strip():
                #                         self.Channel1Viewer.legend.removeItem(plot_item) 
                #                         self.Channel1Viewer.legend.addItem(plot_item,signal.label)
                #                         break

        def changeColor(self,signalEditorID):
                color = QColorDialog.getColor()
                
                if color.isValid():
                        signal = None
                        # Apply the selected color to the signal
                        for signal in self.Channel1Viewer.signalsChannel:
                               if signal.signalId == signalEditorID:
                                      signal.color = color
                                      signal.change_color(color)
                                      break
                        for signal in self.Channel2Viewer.signalsChannel:
                               if signal.signalId == signalEditorID:
                                      signal.color = color
                                      signal.change_color(color)
                                      break
                               
        # NADA'S ADDITION
        def show_polar_view(self, timestamps, signal_values, signal_label, signal_color):
                signal_window = PolarWindow(timestamps, signal_values, signal_label, signal_color)
                signal_window.show()

        def live_connection(self, status):
                if status == "connect":
                        self.fetch_subscriber_count.connected = True
                        self.thread = threading.Thread(target=self.fetch_subscriber_count.fetch_data)
                        self.thread.start()
                else:
                        self.fetch_subscriber_count.connected = False

        def update_count(self):
                # Change plot_widget_two to whatever it is called in the new UI

                subscriber_count = self.fetch_subscriber_count.subscriber_count
                elapsed_time = time.time() - self.start_time

                self.timestamps.append(elapsed_time)
                self.subscriber_counts.append(subscriber_count)

                self.Channel1Viewer.plot_graph.clear()  # not sure if this is necessary
                self.Channel1Viewer.plot_graph.plot(self.timestamps, self.subscriber_counts, pen=pg.mkPen(color='g', width=2),
                                          symbol='o',
                                          symbolBrush='w')

                # Set axis labels
                self.Channel1Viewer.plot_graph.setLabel('left', 'Subs Count')
                self.Channel1Viewer.plot_graph.setLabel('bottom', 'Time (sec)')

                # Set Y-axis range
                # if self.subscriber_counts:
                #         y_min = min(self.subscriber_counts) - 10
                #         y_max = max(self.subscriber_counts) + 10
                        # self.Channel1Viewer.plot_graph.setYRange(y_min, y_max)
                        # self.Channel1Viewer.plot_graph.setXRange(0, max(self.timestamps) + 5)

                # # Format x-axis to show time
                # self.Channel1Viewer.plot_graph.getAxis('bottom').setTicks(
                #         [[(t, time.strftime("%H:%M:%S", time.gmtime(t))) for t in self.timestamps]])
                #
                # # Format y-axis points
                # self.Channel1Viewer.plot_graph.getAxis('left').setTicks(
                #         [[(count, str(count)) for count in
                #           range(int(y_min), int(y_max) + 1, 5)]])  # every 5 subscribers

                # self.plot_widget_two.repaint() #I think this is useless

        # def export_to_pdf(self, signal_one_statistics, signal_two_statistics, glued_plot):
        #         pdf = ExportToPdf(signal_one_statistics, signal_two_statistics, glued_plot)
        def save_report(self, signal_one, signal_two):
            print("Inside Export PDF")
            signal1, signal2 = self.gluedSignals[0], self.gluedSignals[1]
            pdf = ExportToPdf(signal1.signalStatistics(), signal2.signalStatistics(), self.glued_y,
                              self.glued_count)


             


if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyMainWindow()
    #MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.ui = ui
    MainWindow.show()
    sys.exit(app.exec_())
