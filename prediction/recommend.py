#encoding='utf-8'

def recommend(user_id: str):
    """
    Predict 5 articles for user_id. Return array of 5 article_id.
    """
    return [f'{(user_id)}-{item}' for item in [10,20,30,40,50]]