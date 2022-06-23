# coding=utf-8

from sklearn.neighbors import NearestNeighbors
import pandas as pd
import pickle
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


class Recommender:

    def __init__(self, root_dir, nb=5) -> None:
        """
        Tool to recommend nb articles to a reader, based on
        previous readings.
        """
        self.nb = nb
        self.root_dir = root_dir
        with open(self.root_dir + 'articles_embeddings.pickle', 'rb') as f:
            self.embeddings = pd.DataFrame(pickle.load(f))
        self.model_pickle = self.root_dir + 'knn_pickle_file'

        if os.path.isfile(self.model_pickle):
            with open(self.model_pickle, 'rb') as f:
                self.model = pickle.load(f)
        else:
            self.model = NearestNeighbors(n_neighbors=nb + 1)  # +1 bc article itself is also returned
            self.update_model()

    def update_model(self):
        """
        Fit the model to the embeddings and save it.
        """
        self.model.fit(self.embeddings)
        with open(self.model_pickle, 'wb') as f:
            pickle.dump(self.model, f)

    def recommend_from(self, articles_ids):
        """
        Return nb articles closest (by Euclidean distance) to articles that user liked.
        """

        # For each article, find nb closest articles (by embedding vector)
        article_vectors = self.embeddings.loc[articles_ids]
        distances, recommended_i_ids = self.model.kneighbors(article_vectors)
        distances = distances.flatten()
        recommended_i_ids = recommended_i_ids.flatten()
        recommended_ids = self.embeddings.iloc[recommended_i_ids].index

        closest = [item for item in list(zip(recommended_ids, distances))
                   if item[0] not in articles_ids]

        # Return nb globally closest articles, excluding already read ones
        closest.sort(key=lambda tup: tup[1])
        return [item[0] for item in closest[:self.nb]]

