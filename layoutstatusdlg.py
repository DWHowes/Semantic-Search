from PySide6.QtCore import (Slot, 
                            Qt, 
                            QTimer, 
                            QElapsedTimer,
                            QTime,
                            )
from PySide6.QtWidgets import (QVBoxLayout, 
                               QLabel, 
                               QDialog, 
                               QProgressBar, 
                               )

# This dialog displays the status of the spaCy layout process, including a progress bar and elapsed time. 
# It is designed to be used in conjunction with a separate thread that performs the layout processing, 
# allowing for real-time updates without freezing the main application UI.

class LayoutStatusDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Remove the Close button from the title bar menu to prevent users from closing the dialog while 
        # the layout process is running.
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.setWindowTitle("SpaCy Layout Status")
        self.resize(300, 100)

        # Set up the layout and widgets for the dialog
        layout = QVBoxLayout()

        self.statusLabel = QLabel("Starting...", self)

        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)

        # Track and update elapsed time
        self.timerLabel = QLabel("Elapsed Time -", self)
        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_elapsed_time)
        self.update_timer.start(900)

        # Add widgets to the layout
        layout.addWidget(self.statusLabel)
        layout.addWidget(self.progress)
        layout.addWidget(self.timerLabel)

        # Set the layout for the dialog
        self.setLayout(layout)

    # Update the elapsed time display every 900 milliseconds to show how long the layout process has been running.
    def update_elapsed_time(self):
        elapsed_ms = self.elapsed_timer.elapsed()
        time_formatted = QTime.fromMSecsSinceStartOfDay(elapsed_ms).toString("mm:ss")
        self.timerLabel.setText(f"Elapsed Time - {time_formatted}")

    # Update the status label with the current status of the layout process. 
    # This method can be called from the layout processing thread to provide real-time feedback to the user.
    @Slot(str)
    def update_status(self, status):
        self.statusLabel.setText(status)
