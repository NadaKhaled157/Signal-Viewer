# MAKE IT SO THAT THE LIVE SIGNAL IS PLOTTED LIKE OTHER SIGNALS SO THE CONTROLS WORK ON IT AUTOMATICALLY ??
# WILL LIVE SIGNAL BE SCROLLABLE AFTER CONNECTING IT TO UI ??

import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from unofficial_livecounts_api.youtube import YoutubeAgent


class DataFetcher(QThread):
    live_signal = pyqtSignal(float)
    error_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.subscriber_count = None
        self.connected = False
        self.agent = YoutubeAgent()
        self.channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"  # MrBeast Channel
        self.error_signal.connect(self.show_popup)

    def fetch_data(self):
        try:
            while self.connected:
                metrics = self.agent.fetch_channel_metrics(query=self.channel_id)
                self.subscriber_count = metrics.follower_count
                print(f"Live Subscriber Count for MrBeast: {self.subscriber_count}")

                # Emit the signal here to update the main window
                self.live_signal.emit(self.subscriber_count)

                time.sleep(2)
        except Exception as e:  # to disconnect (REMOVE?)
            print(f"Error: {e}")
            self.error_signal.emit()

    def show_popup(self):
        error_message = QMessageBox()
        error_message.setWindowTitle("Error")
        error_icon = QIcon("Deliverables/error_icon.png")
        error_message.setWindowIcon(error_icon)
        error_message.setText("There was an error fetching subscriber count. Please try again later.")
        error_message.setStandardButtons(QMessageBox.Ok)
        error_message.exec_()

