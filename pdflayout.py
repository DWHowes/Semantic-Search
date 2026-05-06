from PySide6.QtCore import (QFile, 
                            QFileInfo, 
                            QThread,
                            Signal,
                            )

import spacy as sp
from spacy_layout import spaCyLayout

from sentence_transformers import SentenceTransformer
import numpy as np

import pandas as pd

# import os
# import json

JSON_EXT = ".json"
NUMPY_EXT = ".npy"

class PDFlayout(QThread):
    # Define signals to send data back to the main thread
    progress_update = Signal(str)

    def __init__(self, file_path:str)->None:
        super().__init__()
        self.doc_path = file_path
        self.pdf = QFileInfo(file_path).fileName()
        self.path = QFileInfo(file_path).filePath()
        self.base_name = QFileInfo(file_path).baseName()
        self.json_name = self.base_name + JSON_EXT
        self.npyDB_name = self.base_name + NUMPY_EXT

    def run(self):
        self.progress_update.emit("Loading model...")
        # Load spaCy and spacy-layout
        nlp = sp.blank("en")
        self.layout = spaCyLayout(nlp)
        
        # Process the content of the PDF
        self.progress_update.emit(f"Processing layout for: {self.pdf} - this may take some time")
        self.doc = self.layout(self.pdf)

        # Save the parsed file to disk
        self.create_span_list()

        # Generate and save the SBERT embeddings for later use in queries
        self.save_embeddings()
              
        # Emit finished
        self.finished.emit()

    # def parse_layout(self, fname:str)->None:
    #     # Parsing the layout of the PDF file can take some time (5-10 minutes)
    #     self.doc = self.layout(fname)

    def save_embeddings(self):
        # Generate and save the SBERT embedding vectors
        self.progress_update.emit(f"Generating SBERT embeddings for: {self.pdf}")
        df = pd.read_json(self.json_name)
        model = SentenceTransformer('msmarco-distilbert-base-v2')
        embeddings = model.encode_document(df.get('text').tolist())
        self.progress_update.emit(f"Saving to {self.npyDB_name}...")
        np.save(self.npyDB_name, embeddings)

    # Save the pandas dataframe containing the processed data to disk
    def save_df(self, df:pd.DataFrame)->None:
        # Delete the JSON file if it already exists
        if QFileInfo.exists(self.json_name):
            QFile.remove(self.json_name)

        df.to_json(self.json_name, orient="records", indent=2)
   
    # Create a pandas dataframe of the list of text spans from the text extracted from the PDF
    # Each row contains the text of the span and the layout information
    def create_span_list(self)->None:
        doc_db = pd.DataFrame(columns = ["layout", "text"])

        layout = []
        text = []
        for span in self.doc.spans["layout"]:
            if span.label_ == 'text':
                layout.append(span._.layout)
                text.append(span.text)

        doc_db['layout'] = layout
        doc_db['text'] = text        

        self.save_df(doc_db)

    # PUBLIC METHODS
    # def process_pdf(self, fname:str, jsonname:str)->None:
    #     self.__parse_layout(fname)
    #     self.__create_span_list(jsonname)
