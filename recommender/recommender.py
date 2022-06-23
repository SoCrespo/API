# coding=utf-8

from sklearn.neighbors import NearestNeighbors
import pickle


class Recommender:

    def __init__(self, nb=5) -> None:
        """
        Tool to recommend nb articles to a reader, based on
        previous readings.
        """

        with open('news-portal-user-interactions-by-globocom/articles_embeddings.pickle') as f:
            self.embeddings = pickle.load(f)

        try:
            with open('knn_pickle_file', 'rb') as f:
                self.knn = pickle.load(f)
        except FileNotFoundError:
            self.knn = NearestNeighbors(n_neighbors=nb + 1)  # +1 bc article itself is also returned
            self.update_model()

    def update_model(self):
        """
        Fit the model to the embeddings and save it.
        """
        self.knn.fit(self.embeddings)
        with open('knn_pickle_file', 'wb') as f:
            pickle.dump(self.knn, f)

    def recommend_from(self, articles_ids):
        """
        Return nb articles closest (by Euclidean distance) to articles that user liked.
        """

        # For each article, find nb closest articles (by embedding vector)
        article_vectors = self.embeddings.loc[articles_ids]
        distances, recommended_i_ids = self.knn.kneighbors(article_vectors)
        distances = distances.flatten()
        recommended_i_ids = recommended_i_ids.flatten()
        recommended_ids = self.embeddings.iloc[recommended_i_ids].index

        closest = [item for item in list(zip(recommended_ids, distances))
                   if item[0] not in articles_ids]

        # Return nb globally closest articles, excluding already read ones
        closest.sort(key=lambda tup: tup[1])
        return [item[0] for item in closest[:self.nb]]
