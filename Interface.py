# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton
)
from PySide6.QtCore import (
    Qt
)

from Scraper import ScraperWorker
#from Utils   import get_panic_color, calculate_days_remaining


class DontPanic(QMainWindow):
    def __init__(self):
        super().__init__()

        #Main window init
        self.setWindowTitle("Don't Panic! - TLM")
        self.setMinimumSize(640, 480) #SD resolution

        # Central Widget & Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Don't Panic header
        self.header = QLabel("Don't Panic!")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 40px; font-weight: bold; color: #00bcd4")
        self.layout.addWidget(self.header)

        # Add Data table
        self.table = QTableWidget(0,2)
        self.table.setHorizontalHeaderLabels(["Assignment", "Due Date"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

        # Add action button
        self.panic_button = QPushButton("SCAN FOR DANGER")
        self.panic_button.clicked.connect(self.start_scraping)
        self.layout.addWidget(self.panic_button)

        # Status Label
        self.status_label = QLabel("Status: Ready!")
        self.layout.addWidget(self.status_label)


    def update_table(self, data):
        self.table.setRowCount(0)
        for row_index, (name, date) in enumerate(data):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(date))

    def start_scraping(self):
        self.panic_button.setEnabled(False)
        self.panic_button.setText("GETTING DATES... Stay Calm")

        self.status_label.setText("Status: Initialising...")
        self.worker = ScraperWorker()

        # Connect signals from scraper to UI
        self.worker.status_update.connect(self.status_label.setText)
        self.worker.data_received.connect(self.update_table)

        self.worker.finished.connect(self.on_scraping_finished)

        self.worker.start()

    def on_scraping_finished(self):
        # Re-enable button
        self.panic_button.setEnabled(True)
        self.panic_button.setText("SCAN FOR DANGER")





