# from fpdf import FPDF
# import os
# import pyqtgraph as pg
# import pyqtgraph.exporters
# import numpy as np
#
#
# def save_image(glued_plot):
#     exporter = pg.exporters.ImageExporter(glued_plot.plotItem)
#     counter = 2
#     image_name = "glued_plot1.png"
#     while os.path.exists(f"Reports/Images/{image_name}"):
#         image_name = f"glued_plot{counter}.png"
#         counter = counter + 1
#     exporter.export(f"Reports/Images/{image_name}")
#
#     # self.image('Reports/Images/glued_plot.png', x=20, y=150, w=170, h=70)
#
#
# class ExportToPdf(FPDF):
#     def __init__(self, signal_one_statistics, signal_two_statistics, glued_signal_values, all_glued_signals,
#                  glued_images_count):
#         super().__init__()
#         self.first_page = True
#         self.add_page()
#         self.glued_images_count = glued_images_count
#         self.all_glued_signals = all_glued_signals
#         glued_signal_values = np.array(glued_signal_values)
#         for i in range(0,glued_images_count):
#             print(f"ALL CH1 SIGNALS: {signal_one_statistics[i].signalStatistics()}\n")
#             # print(f"ALL CH2 SIGNALS: {signal_two_statistics}")
#         # all_glued_signals = np.array(all_glued_signals)
#         # self.export_signal()
#         # self.signal_one_stats = {
#         #     "Mean": round(signal_one_statistics[0], 3),
#         #     "Median": round(signal_one_statistics[1], 3),
#         #     "STD": round(signal_one_statistics[2], 3),
#         #     "MIN": round(signal_one_statistics[3], 3),
#         #     "MAX": round(signal_one_statistics[4], 3)
#         # }
#         # self.signal_two_stats = {
#         #     "Mean": round(signal_two_statistics[0], 3),
#         #     "Median": round(signal_two_statistics[1], 3),
#         #     "STD": round(signal_two_statistics[2], 3),
#         #     "MIN": round(signal_two_statistics[3], 3),
#         #     "MAX": round(signal_two_statistics[4], 3)
#         # }
#         # self.glued_signal_stats = {
#         #     "Mean": round(np.mean(glued_signal_values), 3),
#         #     "Median": round(np.median(glued_signal_values), 3),
#         #     "STD": round(np.std(glued_signal_values), 3),
#         #     "MIN": round(np.min(glued_signal_values), 3),
#         #     "MAX": round(np.max(glued_signal_values), 3)
#         # }
#         # self.statistics_table(self.signal_one_stats, title="Signal One Statistics")
#         self.ln()
#         # self.statistics_table(self.signal_two_stats, title="Signal Two Statistics")
#         self.ln()
#         # self.statistics_table(self.glued_signal_stats, title="Glued Signal Statistics")
#         # if len(glued_plot.listDataItems()) > 0:
#         #     save_image(glued_plot)
#         self.add_images_to_pdf()
#         # self.save_pdf()
#         # count = self.glued_images_count
#         # i = 0
#         # while count > 0:
#         #     self.add_page()
#         #     self.glued_signal_stats = {
#         #         "Mean": round(np.mean(all_glued_signals[i]), 3),
#         #         "Median": round(np.median(all_glued_signals[i]), 3),
#         #         "STD": round(np.std(all_glued_signals[i]), 3),
#         #         "MIN": round(np.min(all_glued_signals[i]), 3),
#         #         "MAX": round(np.max(all_glued_signals[i]), 3)
#         #     }
#         #     self.statistics_table(self.glued_signal_stats, title="Glued Signal Statistics")
#         #     i = i + 1
#         #     count = count - 1
#
#         print(all_glued_signals)
#
#     def header(self):
#         if self.first_page == True:
#             self.set_font('Arial', 'B', 14)
#             self.cell(0, 10, 'Glued Signal Report', 0, 1, 'C')  # pass signal label as a variable
#             self.ln()
#             self.first_page = False
#
#     def statistics_table(self, signal_statistics, title):  # pass dictionary of statistics (mean, median, std, ...etc)
#         total_width = len(signal_statistics) * 30  # number of stats * size
#         start_position = (self.w - total_width) / 2
#
#         self.set_font('Arial', 'B', 12)
#         if title:
#             self.cell(0, 10, title, 0, 1, 'C')
#
#         self.set_x(start_position)
#         for key in signal_statistics:
#             self.cell(30, 10, str(key), 1, 0, 'C')
#
#         self.ln()
#
#         self.set_font('Arial', '', 12)
#         self.set_x(start_position)
#         for value in signal_statistics.values():
#             self.cell(30, 10, str(value), 1, 0, 'C')
#         self.ln(10)
#
#     def add_images_to_pdf(self):
#         images_directory = 'Reports/Images/'
#         all_images = os.listdir(images_directory)
#
#         try:
#             all_images.sort(key=lambda x: int(x[10:-4]))  # Sort based on image number
#         except Exception as e:
#             print(f"error parsing: {e}")
#
#         latest_image_name = all_images[-1] if all_images else None
#         latest_image = latest_image_name.split('t')[1]
#         latest_image_number = int(latest_image.split('.')[0])
#
#         i = 1
#         j = 0
#         y_position = 130  # Starting y-position for the first table
#         images_count = self.glued_images_count
#         first_glue = True
#         while self.glued_images_count > 0:
#             # Check if there's space for both the table and image, otherwise start a new page
#             if y_position + 120 > 270:  # 140 accounts for both the table and the image height
#                 self.add_page()
#                 y_position = 30  # Reset y-position on the new page
#                 first_glue = True
#             self.glued_signal_stats = {
#                 "Mean": round(np.mean(self.all_glued_signals[j]), 3),
#                 "Median": round(np.median(self.all_glued_signals[j]), 3),
#                 "STD": round(np.std(self.all_glued_signals[j]), 3),
#                 "MIN": round(np.min(self.all_glued_signals[j]), 3),
#                 "MAX": round(np.max(self.all_glued_signals[j]), 3)
#             }
#             if not first_glue:
#                 self.ln(90)
#             self.statistics_table(self.glued_signal_stats, title=f"Glued Signal ({i}) Statistics")
#             y_position += 20
#             self.image(f'Reports/Images/glued_plot{latest_image_number - images_count + i}.png', x=20, y=y_position,
#                        w=170, h=70)
#
#             y_position += 100  # Adjust to account for image height and margin
#             i += 1
#             j += 1
#             self.glued_images_count -= 1
#             first_glue = False
#             print(f"glued count: {self.glued_images_count}")
#
#     # def save_pdf(self):
#     #     counter = 2
#     #     file_name = 'Signal Glue Report1.pdf'
#     #     while os.path.exists(f"Reports/{file_name}"):
#     #         file_name = f"Signal Glue Report{counter}.pdf"
#     #         counter = counter+1
#     #     self.output(f"Reports/{file_name}")
#
#     # self.set_title('Signal Glue Report.pdf')
#     # self.save_pdf()
#
# # statistics = {'Mean': 1, 'Median': 22, 'STD': 3}
# # statistics2 = {'Mean': 11, 'Median': 22, 'STD': 3}
# # pdf = ExportToPdf(statistics, statistics2)
# # pdf.add_page()
#
# # pdf.statistics_table(statistics)
# # pdf.output('Reports/SignalLabel.pdf')  # use signal label as a variable
