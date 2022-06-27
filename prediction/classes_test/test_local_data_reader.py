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
def user_data():
    return LocalDataReader().get_data_for_user('0')    

@pytest.fixture
def most_read():
    return LocalDataReader().get_most_read_articles_ids() 

@pytest.fixture
def embeddings():
    return LocalDataReader().get_embeddings()

def test_user_data_loader_is_df(user_data):
    assert isinstance(user_data, pd.DataFrame)

def test_user_data_not_empty(user_data):
    assert not user_data.empty

def test_user_data_loader_has_expected_cols(user_data):
    assert [col in user_data.columns for col in 
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

def test_get_embeddings(embeddings):
    assert embeddings.shape[1] ==  251
