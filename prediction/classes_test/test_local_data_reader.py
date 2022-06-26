# coding = utf-8
import os
import sys
CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)

import pytest
from prediction.classes.local_data_reader import LocalDataReader
import pandas as pd

@pytest.fixture
def result():
    return LocalDataReader().get_data_for_user('0')    

@pytest.fixture
def most_read():
    return LocalDataReader().get_most_read_articles_ids()    

def test_user_data_loader_is_df(result):
    assert isinstance(result, pd.DataFrame)

def test_user_data_not_empty(result):
    assert not result.empty

def test_user_data_loader_has_expected_cols(result):
    assert [col in result.columns for col in 
    ['user_id', 
    'click_article_id', 
    'session_id',
    'session_start',
    'click_timestamp',
    'words_count']]

def test_most_read_return_list(most_read):
    assert isinstance(most_read, list)

def test_most_read_is_not_empty(most_read):
    assert len(most_read) > 0
