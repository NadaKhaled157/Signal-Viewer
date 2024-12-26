# Real-time Biosignal Monitor
<div align = "justify"> This project is a multi-port, multi-channel signal viewer built with Python and Qt. It is designed to allow users to open and view various medical signals, manipulate them, and perform signal gluing operations. The application has the following features:


## Signal Viewing:

*   Users can open signal files from their PC or connect to websites that emit signals in real-time.
*   The application has two identical graphs that can display different signals.
*   Users can link the two graphs to display the same time frames, signal speed, and zoom level.
*   The application also includes a non-rectangular graph for displaying signals in polar view.
*   All signals are displayed in cine mode (running signal through time).

## Signal Manipulation:

*   Users can manipulate signals using UI elements, including:
    *   Changing color
    *   Adding labels/titles
    *   Showing/hiding signals
    *   Controlling cine speed
    *   Zooming in/out
    *   Pausing/playing/rewinding
    *   Scrolling/panning
    *   Moving signals between graphs

## Signal Glue:

*   Users can cut parts of signals from the rectangular graphs and glue them together in the third graph.
*   The glue operation is customizable with parameters such as window start and size, signal gap/overlap, and interpolation order.

## Exporting and Reporting:

*   Users can create reports of the glue operation, including snapshots of the glued graph and data statistics.
*   The reports are generated as PDF files with a well-organized layout and tables for data statistics.

The project aims to provide a comprehensive and user-friendly tool for viewing, manipulating, and analyzing various medical signals. </div>
