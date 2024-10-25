from fpdf import FPDF
import os
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np


def save_image(glued_plot):
    exporter = pg.exporters.ImageExporter(glued_plot.plotItem)
    counter = 2
    image_name = "glued_plot1.png"
    while os.path.exists(f"Reports/Images/{image_name}"):
        image_name = f"glued_plot{counter}.png"
        counter = counter + 1
    exporter.export(f"Reports/Images/{image_name}")

    # self.image('Reports/Images/glued_plot.png', x=20, y=150, w=170, h=70)


class ExportToPdf(FPDF):
    def __init__(self, all_channel_one_signals, all_channel_two_signals, all_glued_signals,
                 glued_images_count):
        super().__init__()
        # self.first_page = True
        self.all_channel_one_signal_stats = [all_channel_one_signals[i].signalStatistics()
                                             for i in range(0, len(all_channel_one_signals))]
        self.all_channel_one_signal_stats = np.array(self.all_channel_one_signal_stats)
        self.all_channel_two_signal_stats = [all_channel_two_signals[i].signalStatistics()
                                             for i in range(0, len(all_channel_one_signals))]
        self.all_channel_two_signal_stats = np.array(self.all_channel_two_signal_stats)

        print(f"ALL CH1 STATS: {self.all_channel_one_signal_stats}")
        print(f"ALL CH2 STATS: {self.all_channel_two_signal_stats}")
        self.all_glued_signals = all_glued_signals
        self.glued_images_count = glued_images_count
        self.pages_count = 1

        self.add_pages()

    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, f'Glued Signal Report ({self.pages_count})', 0, 1, 'C')  # pass signal label as a variable
        self.ln()

    def add_pages(self):
        count = self.glued_images_count
        i = 0
        while count:
            self.add_page()
            self.pages_count += 1
            # Formatting original signal statistics
            signal_one_stats = {
                "Mean": round(np.mean(self.all_channel_one_signal_stats[i][0]), 3),
                "Median": np.median(self.all_channel_one_signal_stats[i][1]),
                "STD": np.std(self.all_channel_one_signal_stats[i][2]),
                "MIN": np.min(self.all_channel_one_signal_stats[i][3]),
                "MAX": np.max(self.all_channel_one_signal_stats[i][4])
            }
            signal_two_stats = {
                "Mean": round(np.mean(self.all_channel_two_signal_stats[i][0]), 3),
                "Median": np.median(self.all_channel_two_signal_stats[i][1]),
                "STD": np.std(self.all_channel_two_signal_stats[i][2]),
                "MIN": np.min(self.all_channel_two_signal_stats[i][3]),
                "MAX": np.max(self.all_channel_two_signal_stats[i][4])
            }
            glued_signal_stats = {
                "Mean": round(np.mean(self.all_glued_signals[i]), 3),
                "Median": np.median(self.all_glued_signals[i]),
                "STD": np.std(self.all_glued_signals[i]),
                "MIN": np.min(self.all_glued_signals[i]),
                "MAX": np.max(self.all_glued_signals[i])
            }
            self.statistics_table(signal_one_stats, title="Signal One Statistics")
            self.statistics_table(signal_two_stats, title="Signal Two Statistics")
            self.statistics_table(glued_signal_stats, title="Glued Signal Statistics")
            self.add_image(i)
            count -= 1
            i += 1

    def statistics_table(self, signal_statistics, title):  # pass dictionary of statistics (mean, median, std, ...etc)
        total_width = len(signal_statistics) * 30  # number of stats * size
        start_position = (self.w - total_width) / 2

        self.set_font('Arial', 'B', 12)
        if title:
            self.cell(0, 10, title, 0, 1, 'C')

        self.set_x(start_position)
        for key in signal_statistics:
            self.cell(30, 10, str(key), 1, 0, 'C')

        self.ln()

        self.set_font('Arial', '', 12)
        self.set_x(start_position)
        for value in signal_statistics.values():
            self.cell(30, 10, str(value), 1, 0, 'C')
        self.ln(10)

    def add_image(self, i):
        images_directory = 'Reports/Images/'
        all_images = os.listdir(images_directory)
        try:
            all_images.sort(key=lambda x: int(x[10:-4]))  # Sort based on image number
        except Exception as e:
            print(f"error parsing: {e}")
        latest_image_name = all_images[-1] if all_images else None
        latest_image = latest_image_name.split('t')[1]
        latest_image_number = int(latest_image.split('.')[0])
        images_count = self.glued_images_count
        self.image(f'Reports/Images/glued_plot{latest_image_number - images_count + i + 1}.png', x=20, y=140,
                   w=170, h=70)
