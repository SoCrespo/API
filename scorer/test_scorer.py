import pytest
from scorer import Scorer
import pandas as pd
import numpy as np


@pytest.fixture
def session():
    clicks_sample = pd.read_csv('/home/sophie/Documents/OPENCLASSROOMS/OC-IA-P9/'
                                'API/scorer/clicks_sample.csv')
    return clicks_sample[clicks_sample['session_id'] == 1506826382352801]


@pytest.fixture
def sc():
    metadata = pd.read_csv('news-portal-user-interactions-by-globocom/articles_metadata.csv')
    return Scorer(metadata)


def test_score_type(sc):
    assert isinstance(sc._score([300, 1_000, 20_000]), np.ndarray)


def test_score_result(sc):
    assert np.array_equal(sc._score([300, 1_000, 20_000]), [[0], [1], [1]])


def test_score_session_is_df(sc, session):
    assert isinstance(sc._compute_scores_on_session(session), pd.DataFrame)


def test_score_session_has_expected_cols(sc, session):
    result = sc._compute_scores_on_session(session)
    assert list(result.columns) == ['user_id', 'click_article_id', 'score']

def test_score_session_return_binary_scores(sc, session):
    result = sc._compute_scores_on_session(session)
    assert all([ item in [0, 1] for item in result['score'].values])