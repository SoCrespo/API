from scorer import Scorer
import pandas as pd
import numpy as np

metadata = pd.read_csv('news-portal-user-interactions-by-globocom/articles_metadata.csv')
scorer = Scorer(metadata)

def test_score_type():
    assert isinstance(scorer.score([300,1_000, 20_000]), np.ndarray)

def test_score_result():
    assert np.array_equal(scorer.score([300,1_000, 20_000]),[[0],[1],[1]])

