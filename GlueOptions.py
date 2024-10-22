from main import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from ExportToPdf import save_image
class GlueOptions(QDialog):
    def __init__(self, portionx1, portiony1, portionx2, portiony2,gluedSignals, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("signal Gluer")
        self.setWindowIcon(QIcon("Deliverables/app icon.png.png"))
        self.portion_x1 = portionx1
        self.portion_y1 = portiony1
        self.portion_x2 = portionx2
        self.portion_y2 = portiony2
        self.interpolation_order = "linear"
        self.gluedSignals = gluedSignals
        self.glued_count = 0
        self.glued_lists = np.array()
        self.glued_x = []
        self.glued_y = []
        self.setStyleSheet("background-color: #181818;")
        self.setFixedSize(800, 600)

        # Main layout for the QDialog
        self.main_glue_options_layout = QVBoxLayout(self)
        shift_buttons_layout = QHBoxLayout()
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

        # Buttons to shift signal 2 left and right
        shift_right_signal2_button = QPushButton(self)
        icon_right = QIcon("Deliverables/move_right-removebg-preview.png")
        shift_right_signal2_button.setIcon(icon_right)
        shift_right_signal2_button.setFixedSize(40, 40)
        shift_right_signal2_button.setGeometry(680, 285, 300, 300)
        shift_right_signal2_button.clicked.connect(self.shiftRightSignal2)
        shift_right_signal2_button.setStyleSheet("font-size: 20px; border-radius: 20px; background-color: gray; ")
        shift_buttons_layout.addWidget(shift_right_signal2_button)

        shift_left_signal2_button = QPushButton(self)
        icon_left = QIcon("Deliverables/move_left-removebg-preview.png")
        shift_left_signal2_button.setIcon(icon_left)
        shift_left_signal2_button.setFixedSize(40,40)
        shift_left_signal2_button.setGeometry(600, 285, 300, 300)
        shift_left_signal2_button.clicked.connect(self.shiftLeftSignal2)
        shift_left_signal2_button.setStyleSheet("font-size: 20px; border-radius: 20px; background-color: gray;")
        shift_buttons_layout.addWidget(shift_left_signal2_button)


        save_glue_button = QPushButton("Save", self)
        icon_save = QIcon("Deliverables/save_icon2.jfif")
        save_glue_button.setIcon(icon_save)
        save_glue_button.setStyleSheet("background-color:gray; border-radius:20px; color:white;")
        save_glue_button.setFixedSize(170, 40)
        save_glue_button.setGeometry(350, 550, 400, 400)
        save_glue_button.clicked.connect(lambda: self.save_glue(self.plot_graph_glued_signal))

        # Input for shift amount
        self.shift_amount_input = QLineEdit(self)
        self.shift_amount_input.setPlaceholderText("0.01")
        self.shift_amount_input.setStyleSheet("background-color: gray; border : none")
        self.shift_amount_input.setFixedSize(30, 30)
        self.shift_amount_input.setGeometry(645, 290, 400, 400)
        shift_buttons_layout.addWidget(self.shift_amount_input)

        # Plotting the signals
        self.line_signal1 = self.plot_graph_glue_options.plot(self.portion_x1, self.portion_y1,
                                                              pen=pg.mkPen(color="red", width=2.5))
        self.line_signal2 = self.plot_graph_glue_options.plot(self.portion_x2, self.portion_y2,
                                                              pen=pg.mkPen(color="blue", width=2.5))

        # Set the default shift amount
        self.shift_amount = 0.01
        self.combo_order.currentIndexChanged.connect(self.showGluedSignal)
        self.intial_glue_x , self.intial_glue_y = self.signal_glue(self.portion_x1, self.portion_y1,self.portion_x2, self.portion_y2, self.interpolation_order)
        self.plot_graph_glued_signal.plot(self.intial_glue_x, self.intial_glue_y, pen=pg.mkPen(color="green", width=2.5))


    def shiftRightSignal2(self):
        self.updateShiftAmount()
        self.portion_x2 = np.array(self.portion_x2) + self.shift_amount
        self.line_signal2.setData(self.portion_x2, self.portion_y2)
        self.showGluedSignal()



    def submit(self):
        interpolation_order = self.combo_order.currentText()
        self.interpolation_order = interpolation_order


    def shiftLeftSignal2(self):
        self.updateShiftAmount()
        self.portion_x2 = np.array(self.portion_x2) - self.shift_amount
        self.line_signal2.setData(self.portion_x2, self.portion_y2)
        self.showGluedSignal()

    def updateShiftAmount(self):
        if self.shift_amount_input.text() == "":
            self.shift_amount = 0.01
        else:
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
                intersection, initial_index, final_index = self.x_interp(portion_x1, portion_x2)
                interp_y_func1 = interp1d(portion_x1, portion_y1, kind=order)
                interp_y_func2 = interp1d(portion_x2, portion_y2, kind=order)
                y1_interp = interp_y_func1(intersection)
                y2_interp = interp_y_func2(intersection)
                y_interp = (y1_interp + y2_interp) / 2

                self.glued_x = np.concatenate(
                    [portion_x1[:initial_index], intersection, portion_x2[final_index:]])
                self.glued_y = np.concatenate(
                    [portion_y1[:initial_index], y_interp, portion_y2[final_index:]])
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
                intersection, initial_index, final_index = self.x_interp(portion_x2, portion_x1)
                interp_y_func2 = interp1d(portion_x2, portion_y2, kind=order)
                interp_y_func1 = interp1d(portion_x1, portion_y1, kind=order)
                y1_interp = interp_y_func1(intersection)
                y2_interp = interp_y_func2(intersection)
                y_interp = (y1_interp + y2_interp) / 2

                self.glued_x = np.concatenate(
                    [portion_x2[:initial_index], intersection, portion_x1[final_index:]])
                self.glued_y = np.concatenate(
                    [portion_y2[:initial_index], y_interp, portion_y1[final_index:]])
                return self.glued_x, self.glued_y

    def x_interp(self, x, y):
        intersection = set(x) & set(y)
        print(intersection)
        initial_index = 0
        final_index = 0

        for i, val in enumerate(x):
            if val == min(intersection):
                initial_index = i
                break

        for i, val in enumerate(y):
            if val == max(intersection):
                final_index = i
                break

        x_list = set(x[initial_index:] + y[:final_index])
        return sorted(x_list), initial_index, final_index

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
        self.plot_graph_glued_signal.clear()
        self.plot_graph_glued_signal.plot(self.glued_x, self.glued_y, pen=pg.mkPen(color="green", width=2.5))
        self.glued_lists.append(self.glued_y)

    def gap_or_overlap(self, range, begin, end):
        gap = False
        if abs(end - begin) >= range:
            gap = True
        return gap