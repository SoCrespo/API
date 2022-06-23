# coding=utf-8
import pandas as pd
from dask import dataframe as ddf


class UserDataLoader:
    def __init__(self) -> None:
        print("Loading data")
        clicks = ddf.read_csv('news-portal-user-interactions-by-globocom/clicks/*.csv').compute()
        articles_metadata = pd.read_csv('news-portal-user-interactions-by-globocom/articles_metadata.csv')
        print('Merging data')
        self.merged = clicks.merge(articles_metadata,
                                   left_on='click_article_id',
                                   right_on='article_id',)
        print('Data loaded')

    def get_data_for_user(self, user_id):
        return self.merged[self.merged['user_id'] == user_id]


if __name__ == '__main__':
    udm = UserDataLoader()
    udm.get_data_for_user(0).to_csv('./user_data.csv', index=False)
