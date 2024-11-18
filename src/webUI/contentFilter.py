import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


class ContentFilter:

    def load_track_genres(self, dataset_name):
        base_dir = 'static'
        save_dir = os.path.join(base_dir, dataset_name)
        genre_file = os.path.join(save_dir, 'genreID.csv')
        genre_df = pd.read_csv(genre_file)
        return genre_df

    def get_genres(self):
        return self.genre_df

    def __init__(self, dataset='genre'):
        self.genre_df = self.load_track_genres(dataset)
        print('content_filter init done')

    def get_norm_genre_matrix(self):
        genre_columns = [i for i in self.genre_df.columns if i.startswith("genre")]
        genre_matrix = self.genre_df[genre_columns].to_numpy()
        g_norm = np.linalg.norm(genre_matrix, axis=1)
        g_norm_inv = np.where(g_norm != 0, 1 / g_norm, 0)
        self.norm_genre_matrix = genre_matrix * g_norm_inv[:, None]
        return self.norm_genre_matrix

    def recommend_songs(self, songIdx=1, n_recommendations=10):
        # Print particulars of the chosen song
        print(self.genre_df.iloc[songIdx])
        norm_genre_matrix = self.get_norm_genre_matrix()
        # Find dot product of the norm_genre_matrix with the norm_genre_matrix row for songIdx
        cosine_similarity = np.matmul(norm_genre_matrix, norm_genre_matrix[songIdx].T)

        # Find the indices of 10 songs that have the highest cosine similarity
        top_indices = np.argsort(cosine_similarity)[-n_recommendations - 1:-1][::-1]

        # Print artist_name and track_title for songs that are similar to songIdx

        print("Here are some recommendations:")
        print(" ")
        print(self.genre_df.iloc[top_indices][['artist_name', 'track_title']])

        return


conFilter = ContentFilter()
print(conFilter.get_norm_genre_matrix())
print(conFilter.recommend_songs(songIdx = 6, n_recommendations = 10))