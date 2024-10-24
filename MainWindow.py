from main import *
from MainWindowUI import Ui_MainWindow
from GlueOptions import GlueOptions
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.glue_window = None
        print("UI setup complete")  # Add this line
        if hasattr(self.ui, 'glueButton'):
            print("Glue button exists")  # Add this line
            self.ui.glueButton.setEnabled(True)
            # self.ui.glueButton.clicked.connect(self.glue_options)
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
        self.allow_drawing = False
        self.capture_button = QPushButton("capture", self)
        self.capture_button.clicked.connect(self.capture_rectangle)
        self.capture_button.hide()

        self.delete_button = QPushButton("delete", self)
        self.delete_button.clicked.connect(self.delete_rectangle)
        self.delete_button.hide()
    def mousePressEvent(self, event):
        print(f"Mouse Pressed at: {event.pos()}")
        click_on_rect = False
        if event.buttons() & Qt.LeftButton and self.allow_drawing :
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
        if event.buttons() & Qt.LeftButton and self.begin and self.captured_cnt < 2 and self.allow_drawing:
            self.destination = event.pos()
            self.update_temp_rectangle()
    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton and not self.selected_rect and self.allow_drawing:
            rect = QRect(self.begin, self.destination)
            if rect.width() > 10 and rect.height() > 10:
                self.create_rectangle(rect)
                self.selected_rect = len(self.rectangles) - 1
                self.show_buttons(event.pos())
                self.capture_rectangle()
                print(f"Rectangle created from: {self.begin} to {self.destination}")  # Log rectangle coordinates
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
        # self.capture_button.move(pos + QPoint(15, 30))
        # self.capture_button.show()
        # self.capture_button.raise_()
        self. delete_button.move(pos+ QPoint(15, 30))
        self.delete_button.show()
        self.delete_button.raise_()

    def determine_viewer(self, rect):

        rect_center= rect.y()

        ch1_center = self.ui.Channel1Viewer.geometry().y()
        ch2_center = self.ui.Channel2Viewer.geometry().y()
        print(f"Channel1Viewer Geometry: {self.ui.Channel1Viewer.geometry()}")  # Log geometry of Channel1Viewer
        print(f"Channel2Viewer Geometry: {self.ui.Channel2Viewer.geometry()}")


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

# adjustment
            viewer_offset_x = current_viewer.geometry().x()
            adjusted_begin_x = self.begin.x() - viewer_offset_x -57
            adjusted_destination_x = self.destination.x() - viewer_offset_x-57

            self.captured_cnt += 1
            if self.captured_cnt == 1:
                self.portion_x1, self.portion_y1 = self.get_intersection(adjusted_begin_x, adjusted_destination_x,
                                                                         current_viewer)
#                print(f"Captured portion 1: end {self.portion_x1[-1]}, begin {self.portion_x1[0]}")

            elif self.captured_cnt == 2:
                self.portion_x2, self.portion_y2 = self.get_intersection(adjusted_begin_x, adjusted_destination_x,
                                                                         current_viewer)
 #               print(f"Captured portion 2: end {self.portion_x2[-1]}, begin {self.portion_x2[0]}")

            # Reset begin and destination points
            self.begin, self.destination = QPoint(), QPoint()
            self.capture_button.hide()
            self.delete_button.hide()
            # print(f"Adjusted Begin: {adjusted_begin_x}, Adjusted Destination: {adjusted_destination_x}")
            # print(f"Portion X1: {self.portion_x1[0]}")
            # print(f"Portion X2: {self.portion_x2[0]}")

            if hasattr(self, 'portion_x1') and hasattr(self, 'portion_y1') and hasattr(self, 'portion_x2') and hasattr(
                    self, 'portion_y2') and self.captured_cnt == 2:
                print("Portions are available")
                self.glue_window = GlueOptions(self.portion_x1, self.portion_y1, self.portion_x2, self.portion_y2,
                                          self.toBeGluedSignals, self)
                self.glue_window.finished.connect(self.delete_all_rectangles)

                self.glue_window.exec_()

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

    def delete_all_rectangles(self):
        self.delete_rectangle()
        for i, (_, _) in enumerate(self.rectangles):
            rect_frame, captured = self.rectangles[i]
            if captured:
                self.captured_cnt -= 1
            rect_frame.setParent(None)
            del self.rectangles[i]

    def get_intersection(self, x1Rectangle, x2Rectangle, current_viewer):
        min_old_range_window, max_old_range_window = 0, self.ui.width()
        min_new_range_x_axis, max_new_range_x_axis = current_viewer.plot_graph.getAxis('bottom').range

        mapped_x1_rect = ((x1Rectangle - min_old_range_window) / (max_old_range_window - min_old_range_window)) * (
                max_new_range_x_axis - min_new_range_x_axis) + min_new_range_x_axis
        mapped_x2_rect = ((x2Rectangle - min_old_range_window) / (max_old_range_window - min_old_range_window)) * (
                max_new_range_x_axis - min_new_range_x_axis) + min_new_range_x_axis

        signals_checked_id = self.ui.get_checked_signal_id(current_viewer)
        signal = None
        if len(signals_checked_id) == 1 :
            signal = self.ui.get_signal_by_id(signals_checked_id[0], current_viewer)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning: You must select <b>one</b> signal per channel to glue.")
            msg.setWindowTitle("Selection Error")
            msg.setWindowIcon(QIcon("Deliverables/error_icon.png"))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.delete_rectangle()
            return [], []
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
        self.allow_drawing = True



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