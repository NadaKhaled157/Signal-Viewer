import time
from PyQt5.QtCore import QThread, pyqtSignal
from unofficial_livecounts_api.youtube import YoutubeAgent


class DataFetcher(QThread):
    live_signal = pyqtSignal(float)
    
    def __init__(self):
        super().__init__()
        self.subscriber_count = None
        self.connected = False
        self.agent = YoutubeAgent()
        self.channel_id = "UCX6OQ3DkcsbYNE6H8uQQuVA"  # MrBeast Channel

    def fetch_data(self):
        try:
            while self.connected:
                metrics = self.agent.fetch_channel_metrics(query=self.channel_id)
                self.subscriber_count = metrics.follower_count
                print(f"Live Subscriber Count for channel MrBeast: {self.subscriber_count}")

                # Emit the signal here to update the main window
                self.live_signal.emit(self.subscriber_count)

                time.sleep(2)
        except KeyboardInterrupt:  # To Disconnect (REMOVE?)
            print("Stopped fetching subscriber count.")
