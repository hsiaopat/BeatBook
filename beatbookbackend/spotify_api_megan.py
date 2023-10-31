import requests
import pprint
from collections import Counter
def get_user(mysql, headers):
    # Request user's profile from the spotify API
    r = requests.get(url='https://api.spotify.com/v1/me', headers=headers)

    # Data from the request
    username = r.json()['id']
    display_name = r.json()['display_name']

    # Select the usernames from the database
    cursor = mysql.connection.cursor()
    cursor.execute("select username from Users");
    usernames = [row[0] for row in cursor.fetchall()]

    # If the user does not already exist, add to the database
    if username not in usernames:
        cursor.execute("insert into Users (username, display_name) values (%s, %s)", 
            (username, display_name));
        cursor.connection.commit()

    cursor.close()

    return username

# Get user top tracks
def get_user_top_tracks(mysql, headers):
    url = 'https://api.spotify.com/v1/me/top/tracks'
    params = {
        'time_range': 'short_term',    # short-term: 4 weeks, medium_term: 6 months, long term: years
        'limit': 20,       # max is 50
        'offset': 0       # start from the first item
    }

    data = requests.get(url=url, params=params, headers=headers).json()

    tracks = []
    tracks_id = []
    #for each song add in its name, id, artist id, artist, album, duration and popularity (0-100)
    for item in data['items']:
        track_name = item['name']
        tracks.append(track_name)
        track_id = item['id']
        tracks_id.append(track_id)
        for art in item['artists']:
            track_art_id = art['id']
            track_art_name = art['name']
            break
        track_album_id = item['album']['id']
        track_album_name =item['album']['name']
        track_duration = item['duration_ms']
        track_popular = item['popularity']
        #Select the Track Id from the database
        cursor = mysql.connection.cursor()
        cursor.execute("select Track_ID from Tracks");
        tracks_id_current = [row[0] for row in cursor.fetchall()]

        #If the Track is not in the db, add
        if track_id not in tracks_id_current:
           cursor.execute("insert into Tracks (Track_ID, Track_name, Artist_ID, Artist_name, Album_ID, Album_name, duration, popularity) values (%s, %s, %s, %s, %s, %s, %s, %s)",
               (track_id, track_name, track_art_id, track_art_name, track_album_id, track_album_name, track_duration, track_popular));
           cursor.connection.commit()
           cursor.close() 
    

    return tracks, tracks_id


# Get user top artists data
def get_user_top_artists(mysql, headers):
    url = 'https://api.spotify.com/v1/me/top/artists'
    params = {
        'time_range': 'short_term',    # short-term: 4 weeks, medium_term: 6 months, long term: years
        'limit': 20,       # max is 50
        'offset': 0       # start from the first item
    }

    data = requests.get(url=url, params=params, headers=headers).json()
    artists = []
    artists_id = []
    for item in data['items']:
        artist_name = item['name']
        artists.append(artist_name)
        artist_id = item['id']
        artists_id.append(artist_id)
        # Select the artist id from the database
        cursor = mysql.connection.cursor()
        cursor.execute("select Artist_ID from Artist");
        artists_id = [row[0] for row in cursor.fetchall()]

        # If the artist id does not already exist, add to the database
        if artist_id not in artists_id:
            cursor.execute("insert into Artist (Artist_ID, Artist_name) values (%s, %s)", 
                (artist_id, artist_name));
            cursor.connection.commit()
            cursor.close()

    return artists, artists_id

#need to input the artist id
def get_artists_genre(mysql, headers,id):
    url = 'https://api.spotify.com/v1/artists/{0}/'.format(id)
    params = {
        
    }
    #list of artist genres
    data = requests.get(url=url, params=params, headers=headers).json()
    genre = data['genres']
    return genre

def get_user_stats(mysql, headers):
    #User_ID
    username = get_user(mysql, headers)
    
    tracks, track_ids = get_user_top_tracks(mysql,headers)
    #select the top artists from the top tracks db
    cursor = mysql.connection.cursor()
    cursor.execute("select Artist_ID from Tracks");
    artist_id = [row[0] for row in cursor.fetchall()]
    cursor.execute("select Artist_name from Tracks");
    artists = [row[0] for row in cursor.fetchall()]
    command = "select display_name from Users where username = '%s'" % username
    cursor.execute(command)
    name = str([row[0] for row in cursor.fetchall()])
    #get current top track 
    top_track = tracks[0]
    top_track_id = track_ids[0]
    genres = []
    art = []
    for x in range(len(artist_id)):
        art_id = artist_id[x]
        art_name = artists[x]
        gen = get_artists_genre(mysql,headers,art_id)
        genres.extend(gen)
        art.append(art_name)
    #Count the number of each genre and artist and take the most common
    count = Counter(genres)
    count_artist = Counter(art)
    top_artist = count_artist.most_common(1)[0][0]
    top_genre = count.most_common(1)[0][0]
    # Select the username from the database

    cursor = mysql.connection.cursor()
    cursor.execute("select username from User_Stats");
    users_id = [row[0] for row in cursor.fetchall()]

    # If the username  does not already exist, add to the database
    if username not in users_id:
        cursor.execute("insert into User_Stats (username, name, top_track_id, top_track, top_artist, top_genre) values (%s, %s, %s, %s, %s, %s)",         
            (username, name, top_track_id, top_track, top_artist, top_genre));
        cursor.connection.commit()
        cursor.close()
    #if the username does exist, update their current stats
    elif username in users_id:
        command = "update User_Stats set top_track_id = '%s', top_track = '%s', top_artist = '%s', top_genre = '%s' where username = '%s'" % (top_track_id, top_track, top_artist, top_genre, username)
        print(command)
        cursor.execute(command);
        cursor.connection.commit()
        cursor.close()

