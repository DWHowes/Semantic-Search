import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow

TITLE = "Semantic Search Using SBERT"

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowTitle(TITLE)
    window.show()
        
    sys.exit(app.exec())