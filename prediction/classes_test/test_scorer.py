import os
import sys
CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PARENT_DIR)


import pytest
from API.prediction.classes.scorer import Scorer
import pandas as pd
import numpy as np


@pytest.fixture
def user_data():
    return pd.read_csv('./user_data.csv')


@pytest.fixture
def session():
    user_data = pd.read_csv('./user_data.csv')
    session_id = user_data['session_id'].unique()[0]
    return user_data[user_data['session_id'] == session_id]


@pytest.fixture
def sc():
    return Scorer()


def test_score_return_ndarray(sc):
    assert isinstance(sc._score([300, 1_000, 20_000]), np.ndarray)


def test_score_result_on_sample(sc):
    assert np.array_equal(sc._score([300, 1_000, 20_000]), [[0], [1], [1]])


def test_score_session_is_df(sc, session):
    assert isinstance(sc._compute_scores_on_session(session), pd.DataFrame)


def test_score_session_has_expected_cols(sc, session):
    result = sc._compute_scores_on_session(session)
    assert list(result.columns) == ['user_id', 'click_article_id', 'score']


def test_score_session_return_binary_scores(sc, session):
    result = sc._compute_scores_on_session(session)
    assert all([item in [0, 1] for item in result['score'].values])


def test_score_session_return_binary_scores_for_user(sc, user_data):
    result = sc.compute_scores(user_data)
    assert all([item in [0, 1] for item in result['score'].values])
