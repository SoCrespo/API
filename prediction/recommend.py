# encoding='utf-8'
import logging
from .classes.cosmos_data_reader import CosmosDataReader
from .classes.blob_manager import BlobManager
from .classes.scorer import Scorer
from .classes.recommender import Recommender

dr = CosmosDataReader()
bm = BlobManager()
sc = Scorer()
rec = Recommender()


def recommend(user_id: str, only_on_liked=False):
    """
    Return array of k article_id recommended for user_id.
    """
    logging.warning(f'Getting clicks for user {user_id}...')
    try:
        user_data = dr.get_data_for_user(user_id)
    except ValueError:
        logging.error('User not found, returning most popular articles.')
        most_read = dr.get_most_read_articles_ids()
        return most_read
    logging.warning(f'Got clicks for user {user_id}.')
    logging.warning(f'Scoring articles for user {user_id}...')
    scored_articles = sc.compute_scores(user_data)
    if only_on_liked:
        scored_articles = scored_articles[scored_articles['score'] == 1]
    logging.warning(f'Scored articles for user {user_id}.')
    logging.warning(f'Recommending articles for user {user_id}...')
    articles_ids = scored_articles['click_article_id'].astype(str).values
    recommendations = rec.recommend_from(articles_ids)
    logging.warning(f'Recommended articles for user {user_id} : {recommendations}.')
    return recommendations
