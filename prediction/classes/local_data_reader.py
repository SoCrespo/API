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
    from prediction import params
else:    
    from .. import params

root_dir = '/home/sophie/Documents/OPENCLASSROOMS/OC-IA-P9/news-portal-user-interactions-by-globocom/'


class LocalDataReader:

    def __init__(self, root_dir=root_dir) -> None:
        """Class to get readings from data."""
        self.root_dir = root_dir
        self.clicks = self._get_clicks()
        self.articles_metadata = self._get_articles_metadata()

    def _get_clicks(self) -> pd.DataFrame:
        return ddf.read_csv(self.root_dir + 'clicks/*.csv',
        dtype={'user_id': str, 'click_article_id': str}).compute()   

    def _get_articles_metadata(self) -> pd.DataFrame:
        return pd.read_csv(self.root_dir + 'articles_metadata.csv',
                           dtype={'article_id': str})

    def get_data_for_user(self, user_id: int) -> pd.DataFrame:
        data = self.clicks[self.clicks['user_id'] == str(user_id)]
        if data.empty:
            raise ValueError('User not found')
        data = data.merge(self.articles_metadata, 
                          left_on='click_article_id',
                          right_on='article_id')
        return data    

    def get_most_read_articles_ids(self) -> list:
        most_read = self.clicks.groupby('click_article_id').count().sort_values(by='user_id', ascending=False).head(params.nb)
        return most_read['user_id'].values.tolist()

if __name__=='__main__':
    print(LocalDataReader().get_most_read_articles_ids())