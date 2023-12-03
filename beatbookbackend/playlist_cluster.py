from sklearn.cluster import OPTICS
import numpy as np
import random
from pandas import DataFrame

def find_clusters(mysql):
    # Group number is hard coded for now
    group_num = 1;

    # Join tables to get track features from the database for users in the specified group
    cursor = mysql.connection.cursor()
    cursor.execute("select Group_%s.Member_name, Track_Attributes.track_name, Track_Attributes.track_id, \
                        Track_Attributes.popularity, Track_Attributes.acousticness, Track_Attributes.danceability, \
                        Track_Attributes.energy, Track_Attributes.instrumentalness, Track_Attributes.loudness, \
                        Track_Attributes.temp, Track_Attributes.valence \
                    from Track_Attributes, User_Tracks, Group_%s \
                    where Track_Attributes.track_id = User_Tracks.track_id and \
                          User_Tracks.username = Group_%s.Member_username", (group_num, group_num, group_num))
    #                      and Tracks.time = 'short_term'")  
    df = DataFrame(cursor.fetchall())
    cursor.close()

    # Make a data frame for the track attributes and one for the track and member names
    df.columns = ['Member', 'Track', 'Track_id', 'Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo', 'Valence']
    tracks = df[['Member', 'Track', 'Track_id']]
    attrs = df[['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo', 'Valence']]
    
    # Normalize and cluster
    normalize(attrs)
    cluster = OPTICS(min_samples=5, xi=0.03)
    cluster.fit(attrs)

    # Find the labels
    labels = cluster.labels_
    
    # Print data points for each cluster
    clusters = [attrs[labels==label].index.tolist() for label in np.unique(labels) if label != -1]
    sort_clusters = sorted(clusters, key=len, reverse=True)[:5]
    print(sort_clusters)

    cluster_tracks = []
    for c in sort_clusters:
        c = [tracks.at[ind, 'Track_id'] for ind in c]
        cluster_tracks.append(random.sample(c, k=5))
    return cluster_tracks

    '''
    unique_labels = np.unique(labels)
    for label in unique_labels:
        cluster_points = attrs[labels == label].index
        print(f"Data points in Cluster {label}:")

        # Print out each track in the cluster
        for ind in cluster_points:
            print(tracks.at[ind, 'Track'])

        print()
    '''

def normalize(df):
    # Update popularity column to be a float value and normalize between 0 and 1
    df.loc[:, 'Popularity'] = df['Popularity'].astype(float)
    df.loc[:, 'Popularity'] = df['Popularity'] / 100.0

    # Normalize loudness column
    df.loc[:, 'Loudness'] = (df['Loudness'] - df['Loudness'].min()) / (df['Loudness'].max() - df['Loudness'].min())

    # Normalize tempo column
    df.loc[:, 'Tempo'] = (df['Tempo'] - df['Tempo'].min()) / (df['Tempo'].max() - df['Tempo'].min())


if __name__ == '__main__':
    pass
    
