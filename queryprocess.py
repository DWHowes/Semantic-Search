import torch
import pandas as pd
import numpy as np

from PySide6.QtCore import QThread, Signal, QObject

from sentence_transformers import SentenceTransformer

class ProcessQuery(QThread):
    finished = Signal(pd.DataFrame)
    progress = Signal(str)

    def __init__(self, json_df:pd.DataFrame, embedding_db:np.ndarray, querystr:str)->None:
        super().__init__()

        self.embedder = SentenceTransformer("msmarco-distilbert-base-v2")
        self.corpus = json_df.get('text').tolist()      
        self.embeddings = embedding_db
        self.querystr = querystr

    def run(self)->pd.DataFrame:
        cut_off = 0

        # Encode the query
        self.progress.emit("Generating query embeddings...")
        query_embedding = self.embedder.encode_query(self.querystr, convert_to_tensor=True)

        # Use cosine-similarity and torch.topk to create an ordered dataframe
        self.progress.emit("Generating similarity scores...")
        similarity_scores = self.embedder.similarity(query_embedding, self.embeddings)[0]
        scores, indices = torch.topk(similarity_scores, k=len(self.corpus))

        ordered_df = pd.DataFrame(columns=["reptext", "srcindex"])
        reptext = []
        src_index = []

        for score, idx in zip(scores, indices):
            if score > cut_off:
                match_str = f"[{score:.4f}] " + " ".join(self.corpus[idx].split()[:7])
                reptext.append(match_str)
                src_index.append(idx.item())

        ordered_df['reptext'] = reptext
        ordered_df['srcindex'] = src_index

        self.finished.emit(ordered_df)
