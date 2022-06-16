# coding=utf8

import pandas as pd
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer


disc = KBinsDiscretizer(n_bins=2, encode='ordinal')

class Scorer:

    def __init__(self, articles_metadata):
        self.articles_metadata = articles_metadata

    @staticmethod
    def score(durations_per_words):
        """
        Return array of binary scores corresponding to durations_per_word list. 
        E.g. : 
        durations_per_word = [300,1_000, 20_000]
        scores =  [[0],
                [1],
                [1]]
        """
        durations_array = np.array(durations_per_words).reshape(-1,1)
        result = disc.fit_transform(durations_array).astype(int)
        return result



    def compute_scores_on_session(self, session_df):
        """
        Input : a dataframe of a user session 
        Output : a dataframe with input columns user_id and click_article_id, 
        plus reading score for each article; computed from timestamps and word count.
        """
        session = session_df.copy()

        # Compute durations
        indices = session.index
        session.loc[indices[0], 'duration'] = (session.loc[indices[0], 'click_timestamp'] 
                                            - session.loc[indices[0], 'session_start']).total_seconds()*1000
        for i in indices[1:]:
            session.loc[i, 'duration'] = (session.loc[i, 'click_timestamp']
                                        - session.loc[i-1, 'click_timestamp']).total_seconds()*1000

        # Add number of words
        session = session.merge(self.articles_metadata, left_on='click_article_id', right_index=True)
        
        # Drop irrelevant values        
        session = session[session['duration'] != 30000]
        session = session[session['words_count'] > 0]
        
        # Compute duration per word
        session['duration_per_word'] = (session['duration'] // (session['words_count']))

        # Compute binary scores
        session['score'] = self.score(session['duration_per_word'].values)

        # Drop unused columns
        session = session[['user_id','click_article_id', 'score']]
        
        return session

if __name__ == '__main__':
    metadata = pd.read_csv('news-portal-user-interactions-by-globocom/articles_metadata.csv')
    scorer = Scorer(metadata)
    result = scorer.score([300,1_000, 20_000])
    print(result)
    print(type(result))