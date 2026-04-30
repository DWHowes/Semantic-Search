import spacy as sp
from spacy_layout import spaCyLayout

import pandas as pd

import os
import json

class PDFlayout():
    def __init__(self)->None:
        nlp = sp.blank("en")
        self.layout = spaCyLayout(nlp)

## PRIVATE METHODS
    def __parse_layout(self, fname:str)->None:
        # Parsing the layout of the PDF file can take some time (5-10 minutes)
        self.doc = self.layout(fname)

    # Save the pandas dataframe containing the processed data to disk
    def __save_df(self, df:pd.DataFrame, jsonname:str)->None:
        # Delete the JSON file if it already exists
        if os.path.exists(jsonname):
            os.remove(jsonname)

        df.to_json(jsonname, orient="records", indent=2)
   
    # Create a pandas dataframe of the list of text spans from the text extracted from the PDF
    # Each row contains the text of the span and the layout information
    def __create_span_list(self, jsonname:str)->None:
        doc_db = pd.DataFrame(columns = ["layout", "text"])

        layout = []
        text = []
        for span in self.doc.spans["layout"]:
            if span.label_ == 'text':
                layout.append(span._.layout)
                text.append(span.text)

        doc_db['layout'] = layout
        doc_db['text'] = text        

        self.__save_df(doc_db, jsonname)

    # PUBLIC METHODS
    def process_pdf(self, fname:str, jsonname:str)->None:
        self.__parse_layout(fname)
        self.__create_span_list(jsonname)
