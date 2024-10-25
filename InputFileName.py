import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ExportToPdf import ExportToPdf


class InputFileName(QDialog):
    def __init__(self, signal_one_statistics, signal_two_statistics, glued_signal_values, all_glued_signals, glued_images_count):
        self.signal_one_statistics = signal_one_statistics
        self.signal_two_statistics = signal_two_statistics
        self.glued_signal_values = glued_signal_values
        self.all_glued_signals = glued_signal_values
        self.glued_images_count = glued_images_count
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PDF Name')
        self.setWindowIcon(QIcon("Deliverables/pdf_icon.png"))
        self.setFixedSize(350, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()

        self.label = QLabel('<b>Enter file name:</b>')
        layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        self.button = QPushButton('Save', self)
        self.button.clicked.connect(lambda: self.on_save())
        layout.addWidget(self.button)

        self.setLayout(layout)

    def center_on_screen(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screenGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_save(self):
        pdf = ExportToPdf(self.signal_one_statistics, self.signal_two_statistics, self.glued_signal_values, self.all_glued_signals, self.glued_images_count)
        self.file_name = self.textbox.text()
        if not self.file_name.endswith('.pdf'):
            self.file_name += '.pdf'
        pdf.output(f"Reports/{self.file_name}")
        self.accept()

# class MainApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Main Application')
#         self.setGeometry(100, 100, 400, 200)
#
#         layout = QVBoxLayout()
#
#         self.button = QPushButton('Open Custom Message Box', self)
#         self.button.clicked.connect(self.open_custom_message_box)
#         layout.addWidget(self.button)
#
#         self.setLayout(layout)
#
#     def open_custom_message_box(self):
#         dialog = InputFileName()
#         if dialog.exec_():
#             print("Accepted")
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_app = MainApp()
#     main_app.show()
#     sys.exit(app.exec_())
