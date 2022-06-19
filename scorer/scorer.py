

import pandas as pd
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer


disc = KBinsDiscretizer(n_bins=2, encode='ordinal')


class Scorer:

    def __init__(self, articles_metadata: pd.DataFrame):
        self.articles_metadata = articles_metadata

    @staticmethod
    def _score(durations_per_words):
        """
        Return array of binary scores corresponding to durations_per_word list.
        E.g. :
        durations_per_word = [300,1_000, 20_000]
        scores =  [[0],
                [1],
                [1]]
        """
        durations_array = np.array(durations_per_words).reshape(-1, 1)
        result = disc.fit_transform(durations_array).astype(int)
        return result

    def _compute_scores_on_session(self, session_df):
        """
        Input : a dataframe of a user session
        Output : a dataframe with input columns user_id and click_article_id,
        plus reading score for each article; computed from timestamps and word count.
        """
        session = session_df.copy()
        session['session_start'] = pd.to_datetime(session['session_start'])
        session['click_timestamp'] = pd.to_datetime(session['click_timestamp'])

        # Compute durations
        indices = session.index
        session.loc[indices[0], 'duration'] = ((session.loc[indices[0], 'click_timestamp']
                                               - session.loc[indices[0], 'session_start'])
                                               .total_seconds() * 1000)
        for i in indices[1:]:
            session.loc[i, 'duration'] = ((session.loc[i, 'click_timestamp']
                                          - session.loc[i - 1, 'click_timestamp'])
                                          .total_seconds() * 1000)

        # Add number of words
        session = session.merge(self.articles_metadata, left_on='click_article_id',
                                right_index=True)

        # Drop irrelevant values
        session = session[session['duration'] != 30000]
        session = session[session['words_count'] > 0]

        # Compute duration per word
        session['duration_per_word'] = (session['duration'] // (session['words_count']))

        # Compute binary scores
        session['score'] = self._score(session['duration_per_word'].values)

        # Drop unused columns
        session = session[['user_id', 'click_article_id', 'score']]

        return session

    def compute_scores(self, user_df):
        """
        Return dataframe with columns user_id, article_id, scores,
        computed for all sessions for user_df.
        """
        scores = pd.DataFrame(columns=['user_id', 'click_article_id', 'score'])
        for session_id in user_df['session_id'].unique():
            session = user_df[user_df['session_id'] == session_id]
            session_scores = self._compute_scores_on_session(session)
            scores = pd.concat((scores, session_scores))
        scores = scores.reset_index(drop=True)
        return scores


if __name__ == '__main__':
    sc = Scorer(pd.read_csv('news-portal-user-interactions-by-globocom/articles_metadata.csv'))
    clicks_sample = pd.read_csv('/home/sophie/Documents/OPENCLASSROOMS/OC-IA-P9/'
                                'API/scorer/clicks_sample.csv')
    session = clicks_sample[clicks_sample['session_id'] == 1506826382352801]
    print(sc._compute_scores_on_session(session).columns)