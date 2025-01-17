# Real-time Biosignal Monitor

This project is a multi-port, multi-channel signal viewer developed using Python and Qt. It is designed to allow users to load, visualize, and manipulate various biosignals in real-time. The application provides powerful tools for signal viewing, manipulation, gluing, and exporting, tailored to both rectangular and polar views.

## Features 🛠️

### Signal Viewing 🖥️

- **File and Real-time Signal Access**: Users can open signal files from their local system or connect to live websites that emit real-time signals.
- **Multiple Graphs**: The application supports two identical graphs that can display different signals simultaneously.
- **Linked Graphs**: Users can link the graphs to synchronize time frames, signal speed, and zoom levels.
- **Polar Graphs**: A non-rectangular graph is available for displaying signals in polar view.
- **Cine Mode**: All signals are displayed in cine mode, enabling users to view signals running through time.

### Signal Manipulation 🔧

The application provides a variety of tools for manipulating signals via a user-friendly interface:

- **Signal Customization**: Change signal colors, add labels, and adjust titles.
- **Signal Visibility**: Show or hide signals within the graphs.
- **Cine Speed Control**: Adjust the playback speed of signals.
- **Zooming and Scrolling**: Zoom in/out and pan through the signals for detailed analysis.
- **Playback Controls**: Pause, play, or rewind signals at your convenience.
- **Graph Movement**: Move signals between different graphs seamlessly.
  
https://github.com/user-attachments/assets/00ea744b-635a-45f2-95c5-3ab777212801

### Signal Linking 
- Ensure that both graphs are synchronized, maintaining linked behavior across all manipulations.
  
https://github.com/user-attachments/assets/b1f6b817-f26d-4de9-9a92-8776109b99fe 

### Signal Gluing 🔗

- **Cut and Glue**: Users can select specific segments of signals from the rectangular graphs and combine them into a third graph.
- **Customizable Glue Parameters**: Fine-tune the glue operation with options such as window start, size, signal gap/overlap, and interpolation order.

https://github.com/user-attachments/assets/694763d4-208c-464d-867f-b404b35ef1dd 

### Exporting and Reporting 📑

- **Report Generation**: After performing glue operations, users can generate detailed reports that include snapshots of the glued signal graph and data statistics.
- **PDF Export**: Reports are generated in PDF format with a structured layout, including tables for data statistics.

https://github.com/user-attachments/assets/6d6e9d4b-bcb3-4009-bec5-ab0406fe1aa8  

### Polar and Rectangular Views

The application distinguishes between two types of signal display modes:

1. **Rectangular View**: Signals are displayed using traditional rectangular graphs, ideal for standard time-domain signals.
2. **Polar View**: A specialized non-rectangular graph is used to visualize signals in polar coordinates, which is helpful for certain types of biosignal analysis.

https://github.com/user-attachments/assets/074b28ec-2d54-4fb9-bff5-58b80fce8743 
### Live Signal Monitoring 📡

- Users can connect to real-time websites (e.g., YouTube subscriber counts) and visualize dynamic fluctuations in their favorite creator's subscriber numbers.
  
https://github.com/user-attachments/assets/f11d0315-6128-4fd5-850c-8c54ad1a8ddb

---




## System Requirements ⚙️

- Python 3.7 or higher.
- Libraries:
  - `numpy`
  - `matplotlib`
  - `PyQt5`
  - `pyqtgraph`
  - `pandas`
  - `scipy`
  - `unofficial-livecounts-api`
  - `FPDF`

---


## Installation 📥

1. Clone this repository:
   ```bash
   git clone https://github.com/NadaKhaled157/Signal-Viewer.git
   
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulator:
   ```bash
   python MainWindow.py
   ```

---
## Acknowledgments :
This project was supervised by Dr. Tamer Basha & Eng. Omar, who provided invaluable guidance and expertise throughout its development as a part of the Digital Signal Processing course at Cairo University Faculty of Engineering.



---

## Team Members
<div align="center">
  <table style="border-collapse: collapse; border: none;">
    <tr>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/b8b8ea9d-ccb6-4ad0-b900-8e48ef2113a8" alt="Enjy Ashraf" width="150" height="150"><br>
        <a href="https://github.com/enjyashraf18"><b>Enjy Ashraf</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/5de3e403-7fce-4000-95d2-e9f07e0d78cf" alt="Nada Khaled" width="150" height="150"><br>
        <a href="https://github.com/NadaKhaled157"><b>Nada Khaled</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/4b1f5180-2250-49ae-869f-4d00fb89447a" alt="Habiba Alaa" width="150" height="150"><br>
        <a href="https://github.com/habibaalaa123"><b>Habiba Alaa</b></a>
      </td>
      <td align="center" style="border: none;">
        <img src="https://github.com/user-attachments/assets/567fd220-acc8-4094-bfe0-5939a0048ca9" alt="Shahd Ahmed" width="150" height="150"><br>
        <a href="https://github.com/Shahd-A-Mahmoud"><b>Shahd Ahmed</b></a>
      </td>
    </tr>
  </table>
</div>




---



