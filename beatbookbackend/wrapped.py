from pandas import DataFrame
from decimal import Decimal

'''
Code to implement our take on Spotify Wrapped
'''

# Get the feature values for one user and format as a list
def get_user_feature_values(mysql, username):
    cursor = mysql.connection.cursor()

    cursor.execute("select User_Tracks.username, avg(popularity), avg(acousticness), \
                           avg(danceability), avg(energy), avg(instrumentalness), \
                           avg(loudness), avg(temp), avg(valence) \
                    from User_Tracks, Track_Attributes \
                    where User_Tracks.Track_ID = Track_Attributes.Track_ID and \
                          User_Tracks.username = %s \
                    group by User_Tracks.username", (username,))
    result = list(cursor.fetchone())
    result = [float(value) if isinstance(value, Decimal) else value for value in result]

    cursor.close()

    return result

# Add the track features for all users in a group into a dataframe and return the average for each column
def get_group_feature_values(mysql, group_num):
    cursor = mysql.connection.cursor()

    cursor.execute("select Member_username \
                    from Group_%s", (group_num,))
    result = list(cursor.fetchall())
    users = [value[0] for value in result]

    cursor.close()

    # Dataframe to hold feature values for each user in the group
    columns = ['username', 'avg_popularity', 'avg_acousticness', 'avg_danceability', 'avg_energy', 'avg_instrumentalness', 'avg_loudness', 'avg_temp', 'avg_valence']
    feature_columns = ['avg_popularity', 'avg_acousticness', 'avg_danceability', 'avg_energy', 'avg_instrumentalness', 'avg_loudness', 'avg_temp', 'avg_valence']
    df = DataFrame(columns=columns)

    for user in users:
        df = df.append(dict(zip(columns, get_user_feature_values(mysql, user))), ignore_index=True)

    avg_features = list(df[feature_columns].mean())
    return avg_features

# Find the difference between the user track values and the group average
def get_user_feature_diff(mysql, group_num, username):
    group = get_group_feature_values(mysql, group_num)
    user = get_user_feature_values(mysql, username)[1:]

    diff = [user[i] - group[i] for i in range(len(group))]

    return diff

# Find top tracks that are shared among group members
def shared_top_tracks(mysql, group_num):
    cursor = mysql.connection.cursor()

    cursor.execute("select Track_name, Artist_name, Album_name \
                    from (select Track_ID, count(Track_ID) as count \
                          from User_Tracks, Group_%s \
                          where User_Tracks.username = Group_%s.Member_username \
                          group by Track_ID \
                          order by count desc) as T, Tracks \
                    where T.count > 1 and Tracks.Track_ID = T.Track_ID", (group_num, group_num))

    df = DataFrame(cursor.fetchall())
    df.columns = ['Track Name', 'Artist Name', 'Album Name']

    cursor.close()

    return df

# Find top artists that are shared among group members
def shared_top_artists(mysql, group_num):
    cursor = mysql.connection.cursor()

    cursor.execute("select Artist_name \
                    from (select Artist_ID, count(Artist_ID) as count \
                          from User_Artist, Group_%s \
                          where User_Artist.username = Group_%s.Member_username \
                          group by Artist_ID \
                          order by count desc) as T, Artist \
                    where T.count > 1 and Artist.Artist_ID = T.Artist_ID", (group_num, group_num))

    df = DataFrame(cursor.fetchall())
    df.columns = ['Artist Name']
    
    cursor.close()

    return df

# Find the percentage of top songs by a single artist
def artists_pie(mysql, group_num):
    cursor = mysql.connection.cursor()

    cursor.execute("select Artist_name, count(Tracks.Track_ID) as count \
                    from User_Tracks, Group_%s, Tracks \
                    where User_Tracks.username = Group_%s.Member_username and \
                          Tracks.Track_ID = User_Tracks.Track_ID \
                    group by Artist_name \
                    order by count desc", (group_num, group_num))
    
    df = DataFrame(cursor.fetchall())
    df.columns = ['Artist Name', 'Num Songs']
    
    # Filters for artists with more than 2 songs in recent listening 
    df = df[df['Num Songs'] > 2]

    cursor.close()

    total_songs = df['Num Songs'].sum()
    df['Percent Top Songs'] = (df['Num Songs'] / total_songs) * 100

    return df

# Find the number of tracks listened to by a single group member
def unique_tracks(mysql, group_num, username):
    cursor = mysql.connection.cursor()

    
    cursor.execute("select Track_name, Artist_name, Album_name \
                    from (select Track_ID, count(Track_ID) as count \
                          from User_Tracks, Group_%s \
                          where User_Tracks.username = Group_%s.Member_username \
                                and User_Tracks.username = %s \
                          group by Track_ID \
                          order by count desc) as T, Tracks \
                    where T.count = 1 and Tracks.Track_ID = T.Track_ID", (group_num, group_num, username))

    df = DataFrame(cursor.fetchall())
    df.columns = ['Track Name', 'Artist Name', 'Album Name']

    cursor.close()

    print(df)

    return df




    
