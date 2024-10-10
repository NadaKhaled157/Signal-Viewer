import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from unofficial_livecounts_api.youtube import YoutubeAgent
import pyqtgraph as pg


class FetchData(QThread):
    signal = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.connected = False
        self.agent = YoutubeAgent()
        self.channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"  # MrBeast Channel

    def run(self):
        while self.connected:
            try:
                metrics = self.agent.fetch_channel_metrics(query=self.channel_id)
                subscriber_count = metrics.follower_count
                print(f"Live Subscriber Count for channel MrBeast: {subscriber_count}")
                self.signal.emit(subscriber_count)
                time.sleep(3)
            except Exception as e:
                print(f"Error fetching data: {e}")
                break


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fetch_count = FetchData()
        self.fetch_count.signal.connect(self.update_count)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 1400, 800)
        self.setWindowTitle("YouTube Live Subscriber Count")

        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setGeometry(50, 100, 1300, 600)
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('left', 'Subscriber Count')
        self.plot_widget.setLabel('bottom', 'Time')
        self.data = []

        button = QPushButton("Connect", self)
        button.setGeometry(1060, 2, 200, 50)
        button.setStyle

def main():
    app = QApplication(sys.argv)  # create new app object
    window = MainWindow()  # create new window object
    window.show()
    sys.exit(app.exec_())  # app.exec_() waits for user to close window


if __name__ == "__main__":  # script is being run directly not imported
    main()
