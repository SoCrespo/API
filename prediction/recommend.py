# encoding='utf-8'
import logging
from .classes.cosmos_data_reader import CosmosDataReader
from .classes.scorer import Scorer
from .classes.recommender import Recommender
from . import params

dr = CosmosDataReader(
    params.endpoint, 
    params.read_key, 
    params.database_name, 
    params.clicks_container_name, 
    params.metadata_container_name)
sc = Scorer()
rec = Recommender(root_dir=params.root_dir, nb=params.nb)


def recommend(user_id: str, only_on_liked=False):
    """
    Return array of k article_id recommended for user_id.
    """
    try:
        user_data = dr.get_data_for_user(user_id)
    except ValueError:
        logging.error('User not found')
        most_read = dr.get_most_read_articles_ids()
        logging.error(most_read)
        return most_read
    logging.warning(user_data)

    scored_articles = sc.compute_scores(user_data)
    if only_on_liked:
        scored_articles = scored_articles[scored_articles['score'] == 1]  
    articles_ids = scored_articles['click_article_id'].astype(str).values
    recommendations = rec.recommend_from(articles_ids)
    return recommendations
