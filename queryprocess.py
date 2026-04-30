import torch
import pandas as pd

from sentence_transformers import SentenceTransformer

class ProcessQuery:
    def __init__(self, jsonfile:str)->None:
        self.embedder = SentenceTransformer("msmarco-distilbert-base-v2")
        # Import Dataset
        df = pd.read_json(jsonfile)
        self.corpus = df.get('text').tolist()       
        self.corpus_embeddings = self.embedder.encode_document(self.corpus, convert_to_tensor=True) 

    def query(self, querystr:str)->pd.DataFrame:
        cut_off = 0

        # Encode the query
        query_embedding = self.embedder.encode_query(querystr, convert_to_tensor=True)

        # Use cosine-similarity and torch.topk to create an ordered dataframe
        similarity_scores = self.embedder.similarity(query_embedding, self.corpus_embeddings)[0]
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

        return ordered_df
