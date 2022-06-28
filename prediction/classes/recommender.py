# coding=utf-8

from sklearn.neighbors import NearestNeighbors
import pandas as pd
import pickle
import os
import warnings
import logging
warnings.filterwarnings("ignore", category=UserWarning)
from .cosmos_data_reader import CosmosDataReader

cr = CosmosDataReader()

class Recommender:

    def __init__(self, nb=5) -> None:
        """
        Tool to recommend nb articles to a reader, based on
        previous readings.
        """
        self.nb = nb
        self.embeddings = self.load_embeddings()
        self.model_pickle_file = './knn.pkl'
        self.model = self.load_model()

    def load_embeddings(self) -> pd.DataFrame:
        logging.warning('Loading embeddings...')
        embeddings = cr.get_embeddings()
        embeddings['article_id'] = embeddings['article_id'].astype(str)
        logging.warning('Embeddings loaded.')
        return embeddings

    def load_model(self, refresh=False):
        logging.warning('Loading model...')
        if (refresh
                or not os.path.isfile(self.model_pickle_file)
                or os.path.getsize(self.model_pickle_file) == 0):

            logging.warning('Model not found, instantiating a new one...')
            model = NearestNeighbors(n_neighbors=self.nb + 1) # +1 bc article itself is also returned
            logging.warning('Fitting model...')
            model.fit(self.embeddings.iloc[:, 1:])
            logging.warning('Model fitted.')
            logging.warning('Saving model...')
            with open(self.model_pickle_file, 'wb') as f:
                pickle.dump(model, f)
            logging.warning('Model saved.')

        else:
            logging.warning('Model found, loading...')
            with open(self.model_pickle_file, 'rb') as f:
                model = pickle.load(f)
    
        logging.warning('Model is ready.')
        return model

    def update_model(self):
        self.model = self.load_model(refresh=True)
    

    def recommend_from(self, articles_ids: list) -> list:
        """
        Return nb articles closest (by Euclidean distance) to articles that user liked.
        """
        # For each article, find nb closest articles (by embedding vector)

        article_vectors = self.embeddings[self.embeddings['article_id'].isin(articles_ids)]
        distances, recommended_i_ids = self.model.kneighbors(article_vectors.iloc[:, 1:])
        distances = distances.flatten()
        recommended_i_ids = recommended_i_ids.flatten()
        recommended_ids = self.embeddings.iloc[recommended_i_ids]['article_id']

        closest = [(id_, distance)
                   for (id_, distance) in list(zip(recommended_ids, distances))
                   if id_ not in articles_ids
                   ]

        # Return nb globally closest articles, excluding already read ones
        closest.sort(key=lambda tup: tup[1])
        return [item[0] for item in closest[:self.nb]]



    

