# coding=utf-8
import logging
import pandas as pd
from dask import dataframe as ddf
if __name__ == '__main__':
    import os
    import sys
    CURRENT_DIR = os.getcwd()
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    sys.path += [CURRENT_DIR, PARENT_DIR]
    from API.prediction import params
else:    
    from .. import params

root_dir = '/home/sophie/Documents/OPENCLASSROOMS/OC-IA-P9/news-portal-user-interactions-by-globocom/'


class UserDataLoader:

    def __init__(self, root_dir=root_dir) -> None:
        """Class to get readings from data."""
        self.root_dir = root_dir
        print("Loading data")
        clicks = ddf.read_csv(self.root_dir + 'clicks/*.csv').compute()
        articles_metadata = pd.read_csv(self.root_dir + 'articles_metadata.csv')
        print('Merging data')
        self.merged = clicks.merge(articles_metadata,
                                   left_on='click_article_id',
                                   right_on='article_id',)
        self.merged['user_id'] = self.merged['user_id'].astype(str)
        print('Data loaded')

    def get_data_for_user(self, user_id: str) -> pd.DataFrame:
        data = self.merged[self.merged['user_id'] == user_id]
        if data.empty:
            raise ValueError('User not found')
        else:
            return data    

    def get_most_read_articles_ids(self) -> list:
        most_read = self.merged.groupby('click_article_id').count().sort_values(ascending=False).head(params.nb)
        return most_read['user_id'].values.tolist()
        


if __name__ == '__main__':
    udm = UserDataLoader()
    # udm.get_data_for_user(0).to_csv('./user_data.csv', index=False)
    print(udm.get_most_read_articles_ids())