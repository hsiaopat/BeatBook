from pandas import DataFrame
from decimal import Decimal
from collections import Counter

'''
Code to implement our take on Spotify Wrapped
'''

# Get the feature values for one user and format as a list
def get_user_feature_values(mysql, username):
    cursor = mysql.connection.cursor()

    cursor.execute("select T.username, avg(popularity), avg(acousticness), \
                           avg(danceability), avg(energy), avg(instrumentalness), \
                           avg(loudness), avg(temp), avg(valence) \
                    from (select User_Tracks_All.username, popularity, acousticness, danceability, energy, instrumentalness, loudness, temp, valence from User_Tracks_All, Track_Attributes \
                    where User_Tracks_All.Track_ID = Track_Attributes.Track_ID and \
                          User_Tracks_All.username = %s and User_Tracks_All.type = 'short_term' \
                    order by User_Tracks_All.date limit 50) as T group by T.username", (username,))
    
    result = cursor.fetchone()
    cursor.close()

    if result is None:
        # Return a default value or handle the case when no data is found
        return []
    
    users = result[0]
    data = result[1:]
    data = [round(float(value), 2) if isinstance(value, Decimal) else round(float(value), 2) for value in data]

    return [users] + data


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

    print(group)
    print(user)

    diff = [round(user[i] - group[i], 2) for i in range(len(group))]

    return diff

# Find top tracks that are shared among group members
def shared_top_tracks(mysql, group_num):
    cursor = mysql.connection.cursor()

    cursor.execute("select Member_username from Group_%s", (group_num,))
    users = list(cursor.fetchall())

    # Find top short term tracks for all members of the group
    all_tracks = []
    for u in users:
        cursor.execute("select Track_name, Artist_name, Album_link \
                    from User_Tracks_All, Track_Attributes_All \
                    where User_Tracks_All.username = %s and User_Tracks_All.type = 'short_term' and User_Tracks_All.Track_ID = Track_Attributes_All.Track_ID \
                    order by User_Tracks_All.date \
                    limit 50", (u,))

        data = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
        all_tracks.append(data)
    
    # Find shared tracks
    flat_tracks = [item for sublist in all_tracks for item in sublist]
    counts = Counter(flat_tracks)
    duplicates = [item for item, count in counts.items() if count > 1]

    cursor.close()
    print(duplicates)
    return duplicates

# Find top artists that are shared among group members
def shared_top_artists(mysql, group_num):
    cursor = mysql.connection.cursor()

    cursor.execute("select Member_username from Group_%s", (group_num,))
    users = list(cursor.fetchall())

    # Find short term artists for all members of the group
    all_artists = []
    for u in users:
        cursor.execute("select Artist_name \
                        from User_Artists_All, Artist \
                        where User_Artists_All.username = %s and User_Artists_All.Artist_ID = Artist.Artist_ID and User_Artists_All.type = 'short_term' \
                        order by User_Artists_All.date \
                        limit 50", (u,))

        data = [row[0] for row in cursor.fetchall()]
        all_artists.append(data)
    
    # Find shared artists
    flat_artists = [item for sublist in all_artists for item in sublist]
    counts = Counter(flat_artists)
    duplicates = [item for item, count in counts.items() if count > 1]

    cursor.close()

    return duplicates

# Find the percentage of top songs by a single artist
def artists_pie(mysql, group_num):
    cursor = mysql.connection.cursor()

    cursor.execute("select Artist_name, count(Q.Track_ID) as count \
                    from (select Artist_name, Tracks.Track_ID as Track_ID from User_Tracks_All, Group_%s, Tracks \
                    where User_Tracks_All.username = Group_%s.Member_username and \
                          Tracks.Track_ID = User_Tracks_All.Track_ID and User_Tracks_All.type = 'short_term' order by User_Tracks_All.date limit 50) as Q \
                    group by Artist_name \
                    order by count desc", (group_num, group_num))
    
    df = DataFrame(cursor.fetchall())
    cursor.close()
    
    print(df)

    if len(df) == 0:
        return []

    df.columns = ['Artist Name', 'Num Songs']
    
    # Filters for artists with more than 2 songs in recent listening 
    df = df[df['Num Songs'] > 2]

    total_songs = df['Num Songs'].sum()
    df['Percent Top Songs'] = round((df['Num Songs'] / total_songs) * 100, 2)

    return df

