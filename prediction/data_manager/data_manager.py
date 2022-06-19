# coding=utf8
import pandas as pd


class DataManager:

    def __init__(self) -> None:
        self.data = pd.read_csv('news-portal-user-interactions-by-globocom/clicks_sample.csv')

    def get__data_for_user(self, user_id):
        """
        Return reading data for user_id.
        """
        return self.data[self.data['user_id'] == user_id]


