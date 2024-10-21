from main import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout
from ExportToPdf import save_image
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