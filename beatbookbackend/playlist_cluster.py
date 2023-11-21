from sklearn.cluster import OPTICS
import numpy as np
from pandas import DataFrame

def find_clusters(mysql):
    # Group number is hard coded for now
    group_num = 1;

    # join the tracks, user_tracks, group_#
    #   filter for short_term tracks, only users in the group
    #   slice the data query for only the relevant columns
    #   standardize / categorize / normalize data
    #   fit the model (figure out min_samples, cluster_size, and neighbor_distance)
    #   get labels for the clusters
    #   pull 3-5 tracks from the label and call spotify recommendations endpoint

    # Join tables to get track features from the database for users in the specified group
    cursor = mysql.connection.cursor()
    cursor.execute("select Group_%s.Member_name, Tracks.track_name, Tracks.popularity \
                    from Tracks, User_Tracks, Group_%s \
                    where Tracks.track_id = User_Tracks.track_id and \
                          User_Tracks.username = Group_%s.Member_username", (group_num, group_num, group_num))
    #                      and Tracks.time = 'short_term'")  
    df = DataFrame(cursor.fetchall())
    cursor.close()
    
    print(df)
    normalize(df)
    print(df)

    #cluster = OPTICS(min_samples=20, xi=0.05, min_cluster_size=0.05)
    #cluster.fit(df)

    #labels = clustering.labels_
    #print("labels: ", labels)

def normalize(data):
    tup_pop = 2

    for row in data:
        print(row)

        # Popularity
        #tup[tup_pop] = float(tup[tup_pop]) / 100.0

        # 

if __name__ == '__main__':
    pass
