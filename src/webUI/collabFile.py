import pandas as pd
import numpy as np
import warnings
import os

warnings.filterwarnings('ignore')


class CollabFilter:

    def load_tracks(self, dataset_name):
        base_dir = 'static'
        save_dir = os.path.join(base_dir, dataset_name)
        track_file = os.path.join(save_dir, 'IndianMusicTracks.csv')
        track_df = pd.read_csv(track_file, index_col=0)
        return track_df

    def load_users(self, dataset_name):
        base_dir = 'static'
        save_dir = os.path.join(base_dir, dataset_name)
        user_file = os.path.join(save_dir, 'UserList.csv')
        user_df = pd.read_csv(user_file, index_col=0)
        return user_df

    def load_user_item_interactions(self, dataset_name):
        base_dir = 'static'
        save_dir = os.path.join(base_dir, dataset_name)
        uii_file = os.path.join(save_dir, 'user_item_interactions.csv')
        user_item_df = pd.read_csv(uii_file, index_col=0)
        return user_item_df

    def __init__(self, dataset='collab'):
        self.track_df = self.load_tracks(dataset)
        self.user_df = self.load_users(dataset)
        self.user_item_df = self.load_user_item_interactions(dataset)
        print('collab_filter init done')

    def get_tracks(self):
        return self.track_df

    def get_users(self):
        return self.user_df

    def get_user_item(self):
        return self.user_item_df

    def cosine_similarity(self, song_index, rank=12, n_recommendations=3):
        user_item_matrix = self.user_item_df.to_numpy()
        P, S, Qh = np.linalg.svd(user_item_matrix)
        q = Qh[:rank, song_index]
        q_norm = np.linalg.norm(q)
        q = q / q_norm

        Q_temp = Qh[:rank, :].T
        Q_temp_norm = np.linalg.norm(Q_temp, axis=1)
        # Normalize every row of Qh
        Q_temp = Q_temp / Q_temp_norm[:, None]

        cs_vector = np.dot(Q_temp, q)
        print(cs_vector)
        # sort cs_vector in ascending order and return the indices
        top_indices = np.argsort(cs_vector)[-1:0:-1][0:n_recommendations]
        top_values = cs_vector[top_indices]
        return (top_indices, top_values)

colabF = CollabFilter()
song_index = 8
rank = 4

print(type(colabF.track_df.iloc[song_index]))
print(colabF.track_df.iloc[song_index])
print(type(colabF.track_df.iloc[colabF.cosine_similarity(song_index, rank)[0]]))
print(colabF.track_df.iloc[colabF.cosine_similarity(song_index, rank)[0]])