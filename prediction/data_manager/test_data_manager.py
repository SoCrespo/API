#coding=utf8
import pandas as pd
from data_manager import DataManager
dm = DataManager()


def test_data_manager_return_df():
    assert isinstance(dm.get__data_for_user(0), pd.DataFrame)


def test_data_manager_return_not_empty_df_for_existing_user():
    assert not dm.get__data_for_user(0).empty


def test_data_manager_has_necessary_columns():
    necessary_columns = [
        'user_id',
        'session_id',
        'click_article_id',
        'session_start',
        'click_timestamp', ]
    assert all([item in dm.get__data_for_user(0).columns
                for item in necessary_columns])
