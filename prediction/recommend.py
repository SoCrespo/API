# encoding='utf-8'
from user_data_loader.user_data_loader import UserDataLoader
from scorer.scorer import Scorer
from recommender.recommender import Recommender


udm = UserDataLoader()
sc = Scorer()
rec = Recommender()


def main(user_id: str, only_on_liked=False):
    """
    Return array of k article_id recommended for user_id.
    """
    user_data = udm.get_data_for_user(user_id)
    articles = sc.compute_scores(user_data)
    if only_on_liked:
        articles = user_data[user_data['score'] == 1]
    recommendations = rec.recommend_from(articles)
    return recommendations


if __name__ == '__main__':
    print(main(0))
