# encoding='utf-8'
import logging
from .classes.user_data_loader import UserDataLoader
from .classes.scorer import Scorer
from .classes.recommender import Recommender
from . import params

udm = UserDataLoader(root_dir=params.root_dir)
sc = Scorer()
rec = Recommender(root_dir=params.root_dir, nb=params.nb)


def recommend(user_id: str, only_on_liked=False):
    """
    Return array of k article_id recommended for user_id.
    """
    try:
        user_data = udm.get_data_for_user(user_id)
    except ValueError:
        logging.error('User not found')
        most_read = udm.get_most_read_articles_ids()
        logging.error(most_read)
        return most_read
    logging.warning(user_data)

    scored_articles = sc.compute_scores(user_data)
    if only_on_liked:
        scored_articles = scored_articles[scored_articles['score'] == 1]  
    articles_ids = scored_articles['click_article_id'].values
    recommendations = rec.recommend_from(articles_ids)
    return recommendations
