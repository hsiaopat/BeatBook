from sklearn.cluster import OPTICS
import numpy as np
from pandas import DataFrame

def find_clusters(mysql):
    # Group number is hard coded for now
    group_num = 1;

    # Join tables to get track features from the database for users in the specified group
    cursor = mysql.connection.cursor()
    cursor.execute("select Group_%s.Member_name, Track_Attributes.track_name, \
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
    df.columns = ['Member', 'Track', 'Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo', 'Valence']
    tracks = df[['Member', 'Track']]
    attrs = df[['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Loudness', 'Tempo', 'Valence']]
    
    # Normalize and cluster
    normalize(attrs)
    cluster = OPTICS(min_samples=3, xi=0.03)
    cluster.fit(attrs)

    # Find the labels
    labels = cluster.labels_
    print("labels: ", labels, "len: ", len(labels))
    
    # Print data points for each cluster
    unique_labels = np.unique(labels)
    for label in unique_labels:
        cluster_points = attrs[labels == label].index
        print(f"Data points in Cluster {label}:")

        # Print out each track in the cluster
        for ind in cluster_points:
            print(tracks.at[ind, 'Track'])

        print()

def normalize(df):
    # Update popularity column to be a float value and normalize between 0 and 1
    df['Popularity'] = df['Popularity'].astype(float)
    df['Popularity'] = df['Popularity'] / 100.0

    # Normalize loudness column
    df['Loudness'] = (df['Loudness'] - df['Loudness'].min()) / (df['Loudness'].max() - df['Loudness'].min())

    # Normalize tempo column
    df['Tempo'] = (df['Tempo'] - df['Tempo'].min()) / (df['Tempo'].max() - df['Tempo'].min())


if __name__ == '__main__':
    pass
    
