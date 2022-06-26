# coding=utf-8

from sklearn.neighbors import NearestNeighbors
import pandas as pd
import pickle
import os
import warnings
import logging
warnings.filterwarnings("ignore", category=UserWarning)


class Recommender:

    def __init__(self, nb=5) -> None:
        """
        Tool to recommend nb articles to a reader, based on
        previous readings.
        """
        logging.warning('Loading embeddings...')
        self.nb = nb
        self.embeddings = pd.read_csv('/home/sophie/Documents/OPENCLASSROOMS/OC-IA-P9/send_data_to_azure/cosmos/embeddings_cosmos.csv')
        self.embeddings['article_id'] = self.embeddings['article_id'].astype(str)
        logging.warning('Embeddings loaded.')
        logging.warning('Loading model...')
        self.model_pickle_file = './knn_pickle_file'
        if os.path.isfile(self.model_pickle_file):
            with open(self.model_pickle_file, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.model = NearestNeighbors(n_neighbors=nb + 1)  # +1 bc article itself is also returned
            self.update_model()
        logging.warning('Model loaded.')

    def update_model(self):
        """
        Fit the model to the embeddings and save it.
        """
        self.model.fit(self.embeddings.iloc[:, 1:])
        with open(self.model_pickle_file, 'wb') as f:
            pickle.dump(self.model, f)

    def recommend_from(self, articles_ids: list) -> list:
        """
        Return nb articles closest (by Euclidean distance) to articles that user liked.
        """
        # For each article, find nb closest articles (by embedding vector)

        article_vectors = self.embeddings[self.embeddings['article_id'].isin(articles_ids)]
        logging.warning(article_vectors.iloc[:, 1:].head())
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
