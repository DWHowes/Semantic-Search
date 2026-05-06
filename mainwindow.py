from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QLabel, QTableWidgetItem, QHeaderView
from PySide6.QtGui import QShortcut, QKeySequence, QCloseEvent, QAction
from PySide6.QtCore import QPoint, Slot
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

import pandas as pd
import numpy as np

import os
from functools import partial

from generated_files.MainWindow import Ui_MainWindow
from recentfiles import RecentFiles
from pdflayout import PDFlayout
from queryprocess import ProcessQuery
from myview import MyPdfView
from layoutstatusdlg import LayoutStatusDialog

STATUS_TEXT_BASE = "Open File: "
JSON_EXT = ".json"
NUMPY_EXT = ".npy"
CLOSE_NAME = "Close Application"
CLOSE_QUERY = "Are you sure you wish to proceed?"
MISSING_FILE = "The associated JSON file or SBERT embeddings file for this PDF can not be found. Clicking OK launches the file selection dialog so those files can be recreated."

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize class variables
        self.pdf_json = None
        self.file_path = None
        self.file_name = None
        self.json_name = None
        self.json_file = None
        self.embeddings_name = None
        self.embeddings = None

        # Initialize the status bar text
        self.status_label = QLabel(STATUS_TEXT_BASE)

        # Open the recent file list
        self.exe_dir = os.getcwd()
        self.recent_files = RecentFiles(self.exe_dir)

        # Initialize application classes
        self.ui = Ui_MainWindow()
        self.document = QPdfDocument(self)

        # Set up the application layout
        self.ui.setupUi(self)

        # Set up the PDF viewer
        self.viewer = MyPdfView(self.ui.pdfView)
        self.viewer.setGeometry(0, 0, self.ui.pdfView.geometry().width(), self.ui.pdfView.geometry().height())
        self.viewer.setPageMode(QPdfView.PageMode.MultiPage)
        self.viewer.setZoomMode(QPdfView.ZoomMode.FitInView)

        # Set up the status bar
        self.ui.statusbar.addWidget(self.status_label)

        # Set up menu and toolbar actions
        self.ui.actionOpen_PDF_Tbar.triggered.connect(self.open_PDF)
        self.ui.actionClose_App_Tbar.triggered.connect(self.close_app)
        self.ui.actionOpen_PDF.triggered.connect(self.open_PDF)
        self.ui.actionClose.triggered.connect(self.close_app)

        # Set up query text field and search button actions
        self.ui.editQuery.returnPressed.connect(self.ui.btnSearch.clicked)
        self.ui.btnSearch.clicked.connect(self.query)

        # Add CTRL-HOME and CTRL-END keyboard shortcuts for the PDF viewer
        shortcut_home = QShortcut(QKeySequence("Ctrl+Home"), self)
        shortcut_end = QShortcut(QKeySequence("Ctrl+End"), self)
        shortcut_home.activated.connect(self.home)
        shortcut_end.activated.connect(self.end)

        # Load the recent file list
        self.update_recent_files()

        # Disable the text entry field and the search button until a pdf file is loaded
        self.ui.editQuery.setDisabled(True)
        self.ui.btnSearch.setDisabled(True)

        # Hide the vertical and horizontal headers.
        # Connect the trigger function 
        self.ui.tblResults.verticalHeader().hide()
        self.ui.tblResults.horizontalHeader().hide()
        self.ui.tblResults.cellClicked.connect(self.on_cell_clicked)

        # Connect text changed for the text entry field
        self.ui.editQuery.textChanged.connect(self.on_text_changed)

        # Make the application a fixed size.
        self.setFixedSize(1300, 1200)

    @Slot(str)

    # Open a file selected from the recent file list
    def open_selected_file(self, path:str):
        self.file_path = path

        self.load_viewer()

        # Open the associated JSON file and embeddings file, and enable the query text field
        if  os.path.isfile(self.json_name) and os.path.isfile(self.embeddings_name):
            self.load_saved_layout()
        else:
            # Display a warning message if the associated JSON file or embeddings file cannot be found, 
            # and open the file dialog to select the PDF file again when the user clicks OK on the warning message box.
            QMessageBox.warning(self, 
                                "File Not Found", 
                                MISSING_FILE, 
                                QMessageBox.StandardButton.Ok)
            self.open_PDF()

    # When a row in the result table is selected, go to the correct page and pass the
    # bounding box data to the pdf viewer.
    def on_cell_clicked(self, row, _):
        item = self.ui.tblResults.item(row, 1)
        if item:
            self.gotopage(self.json_file.iloc[int(item.text()), 0]["page_no"]-1)
            self.viewer.setLayout(self.json_file.iloc[int(item.text()), 0])

    # Update the content of the query text box when something is typed.
    def on_text_changed(self)->None:
        if len(self.ui.editQuery.text()) > 0:
            self.ui.btnSearch.setDisabled(False)
        else:
            self.ui.btnSearch.setDisabled(True)

    # Loads the recent files json file from disk
    # Connect the trigger to open a file selected from the recent file list
    def update_recent_files(self)->None:
        self.ui.menuOpen_Recent.clear()
        rct_files = self.recent_files.get_recent_file_list()
        for f_path in rct_files:
            self.actionOpenRecent = QAction(f_path, self)
            self.ui.menuOpen_Recent.addAction(self.actionOpenRecent)
            self.actionOpenRecent.triggered.connect(partial(self.open_selected_file, f_path))

    # Process the query entered in the text box, updating the content of the results table.
    def query(self)->None:
        self.query_thread = ProcessQuery(self.json_file, self.embeddings, self.ui.editQuery.text())

        # Connect slots for proper termination of thread and closing of the status dialog when processing is finished
        self.query_thread.finished.connect(self.query_thread.quit)
        self.query_thread.finished.connect(self.query_thread.deleteLater)
        # Connect the finished signal to the on_finished method to update the results table when 
        # processing is complete.
        self.query_thread.finished.connect(self.on_finished)
        
        self.query_thread.start()

    def on_finished(self, query_df:pd.DataFrame)->None:
        self.ui.tblResults.setRowCount(query_df.shape[0])
        self.ui.tblResults.setColumnCount(query_df.shape[1])

        for row_idx, row_data in query_df.iterrows():
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.ui.tblResults.setItem(row_idx, col_idx, item)  

        self.ui.tblResults.hideColumn(1)  
        self.ui.tblResults.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # Set the current cell to the first result in the table, and trigger the cellClicked 
        # signal to update the PDF viewer with the bounding box data for that result.
        target_row = 0
        target_col = 0
        self.ui.tblResults.setCurrentCell(target_row, target_col)  # Set visual focus
        self.ui.tblResults.cellClicked.emit(target_row, target_col) # Trigger slots        
    
    def clear_content(self)->None:
        self.ui.editQuery.clear()
        self.ui.tblResults.clearContents()
        self.ui.tblResults.setRowCount(0)
        self.viewer.clearLayout()

    # Load the PDF viewer.
    def load_viewer(self)->None:
        self.status_label.setText(STATUS_TEXT_BASE+self.file_path)
        # Add the opened file to the recent file list
        self.recent_files.add_recent_file(self.file_path)
        self.update_recent_files()

        # Clear the (1) edit field, (2) query result table, (3) PDF viewer
        self.clear_content()

        # Attach the document to the pdf viewer. 
        self.viewer.setDocument(self.document)

        # Load the PDF document and attach it to the view
        self.document.load(self.file_path)    

        # Save the file path and file name separately for later use
        directory = os.path.dirname(self.file_path)
        self.file_name = os.path.basename(self.file_path)
        self.json_name = os.path.splitext(self.file_name)[0]+JSON_EXT
        self.embeddings_name = os.path.splitext(self.file_name)[0]+NUMPY_EXT

        # Change the current working directory to the source directory for the pdf file
        # This is where the parsed json and embeddings files are stored
        os.chdir(directory)

    # Open the PDF file selected in the Open File dialog box.
    def open_PDF(self):
        # Open a file dialog to select a single file
        self.file_path, _ = QFileDialog.getOpenFileName(self, 
                                                        "Open PDF File", 
                                                        "", 
                                                        "PDF Files (*.pdf)"
                                                        )        

        if self.file_path:
            self.load_viewer()
            # If a matching json file or embeddings file doesn't exist in the CWD, parse the PDF 
            # using spacy-layout and save the json and embeddings files. This  is only done the 
            # first time the PDF file is loaded 
            # These files are used to perform the semantic search
            if not os.path.isfile(self.json_name) or not os.path.isfile(self.embeddings_name):
                self.create_layout()
            # If both the json file and the embeddings file already exist, load them and enable 
            # the query text field
            else:
                self.load_saved_layout()

    # Load the saved json file and numpy file containing the parsed layout information and the 
    # SBERT embedding vectors, respectively.
    def load_saved_layout(self):
        self.json_file = pd.read_json(self.json_name)
        self.embeddings = np.load(self.embeddings_name)
        self.ui.editQuery.setDisabled(False)

    # Create the layout of the PDF file using spacy-layout.
    # Processing of the PDF file is done in a separate thread to avoid blocking the main application, 
    # and a status dialog is used to display status information about the processing of the PDF file.
    def create_layout(self):
        self.statusDlg = LayoutStatusDialog(self)
        self.statusDlg.show()

        self.layout = PDFlayout(self.file_path)

        # Connect slot the status dialog to display thread status information
        self.layout.progress_update.connect(self.statusDlg.update_status)

        # Connect slots for proper termination of thread
        self.layout.finished.connect(self.layout.quit)
        self.layout.finished.connect(self.layout.deleteLater)
        self.layout.finished.connect(self.statusDlg.close)
        # Connect slots to load the generated json file and numpy file, and enable the query text field when 
        # processing is finished
        self.layout.finished.connect(lambda: setattr(self, 'json_file', pd.read_json(self.json_name)))
        self.layout.finished.connect(lambda: setattr(self, 'embeddings', np.load(self.embeddings_name)))
        self.layout.finished.connect(lambda: self.ui.editQuery.setDisabled(False))
        
        self.layout.start()

        self.ui.editQuery.setDisabled(True)
    
    # Go to the first page of the PDF file.
    def home(self)->None:
        if self.file_path:
            self.gotopage(0)

    # Go the the last page of the PDF file.
    def end(self)->None:
        if self.file_path:
            self.gotopage(self.document.pageCount() - 1)

    # Go to the specified page of the PDF file.
    def gotopage(self, page:int)->None:
        nav = self.viewer.pageNavigator()
        nav.jump(page, QPoint(), nav.currentZoom())

    # Close the application using the application close button (X) in the upper-right corner of the app.
    def closeEvent(self, event:QCloseEvent)->None:
        reply = QMessageBox.question(self, 
                                     CLOSE_NAME, 
                                     CLOSE_QUERY,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            super().closeEvent(event)
            self.recent_files.save_recent_file_list()
            event.accept()
        elif reply == QMessageBox.StandardButton.No:
            event.ignore()

    # Close the application using the close button on the toolbar or selecting close from the menu.
    def close_app(self)->None:
        reply = QMessageBox.question(self, 
                                     CLOSE_NAME, 
                                     CLOSE_QUERY,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.recent_files.save_recent_file_list()
            exit()
        