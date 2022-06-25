# coding = utf-8
import os
import sys
CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)

import pytest
from prediction.classes.user_data_loader import UserDataLoader
import pandas as pd

@pytest.fixture
def result():
    return UserDataLoader().get_data_for_user('0')

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

