from fpdf import FPDF
import os


class ExportToPdf(FPDF):
    def __init__(self, signal_one_statistics, signal_two_statistics):
        super().__init__()
        self.add_page()
        # self.export_signal()
        self.statistics_table(signal_one_statistics, title="Signal One Statistics")
        self.statistics_table(signal_two_statistics, title="Signal Two Statistics")
        self.save_pdf()

    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Signal Label Report', 0, 1, 'C')  # pass signal label as a variable
        self.ln()

    # def export_signal(self, channel_number):  # IN PROGRESS
    #     if channel_number == 1:
    #         bbox = (380, 160, 1500, 535)
    #         # signal_name = signal_one_name
    #     elif channel_number == 2:
    #         bbox = (380, 500, 1500, 1060)
    #         # signal_name = signal_two_name
    #     else:
    #         bbox = (380, 160, 1500, 1070)
    #     # snapshot = pyautogui.screenshot()
    #     # snapshot_path = "Snapshots/snapshot.png"
    #     # snapshot.save(snapshot_path)
    #     snapshot = ImageGrab.grab(bbox=bbox)
    #     snapshot.show()
    #     snapshot_path = "Snapshots/snapshot.png"
    #     snapshot.save(snapshot_path)
    #     pdf = canvas.Canvas("Reports/example.pdf", pagesize=A4)
    #     pdf.setTitle("Sample PDF")
    #     # pdf.drawString(200, 800, "Hello, user!")
    #     pdf.drawImage(snapshot_path, 70, 500, 350, 150)
    #     pdf.save()

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
        self.ln(20)


    def save_pdf(self):
        counter = 1
        file_name = 'Signal Glue Report.pdf'
        while os.path.exists(f"Reports/{file_name}"):
            file_name = f"Signal Glue Report{counter}.pdf"
            counter = counter+1
        self.output(f"Reports/{file_name}")

        # self.set_title('Signal Glue Report.pdf')
        # self.save_pdf()

# statistics = {'Mean': 1, 'Median': 22, 'STD': 3}
# statistics2 = {'Mean': 11, 'Median': 22, 'STD': 3}
# pdf = ExportToPdf(statistics, statistics2)
# pdf.add_page()

# pdf.statistics_table(statistics)
# pdf.output('Reports/SignalLabel.pdf')  # use signal label as a variable
