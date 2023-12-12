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




# Get user top tracks for short, medium and long term
def get_user_top_tracks(mysql, headers):
    times = ['short_term', 'medium_term', 'long_term']
    for time in times:

        url = 'https://api.spotify.com/v1/me/top/tracks'
        params = {
            'time_range': time,    # short-term: 4 weeks, medium_term: 6 months, long term: years
            'limit': 50,       # max is 50
            'offset': 0       # start from the first item
        }

        data = requests.get(url=url, params=params, headers=headers).json()
        username = get_user(mysql, headers)
        tracks = []
        tracks_id = []
        print("Check 1")
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
            cursor.execute("select Track_ID, username from User_Tracks")
            User_Tracks = cursor.fetchall()
            cursor.execute("select Track_ID from Track_Attributes")
            tracks_id_attr_current = [row[0] for row in cursor.fetchall()]
            Track_User = '_'.join([track_id , username])

            url_attributes = 'https://api.spotify.com/v1/audio-features'
            params_attributes = {
                'ids' : track_id
            }
            data_attributes = requests.get(url=url_attributes, params=params_attributes, headers=headers).json()
            if 'audio_features' in data_attributes:
                for i in data_attributes['audio_features']:
                    acoust = i['acousticness']
                    dance = i['danceability']
                    energy = i['energy']
                    instru = i['instrumentalness']
                    loud = i['loudness']
                    tempo = i['tempo']
                    valence = i['valence']
            User_Track = []
            for x in range(len(User_Tracks)):
                 User_Track.append('_'.join(User_Tracks[x]))
            if Track_User not in User_Track:
                cursor.execute("insert into User_Tracks (Track_ID, username) values (%s, %s)" ,        
                    (track_id, username))
            if track_id not in tracks_id_current:
                cursor.execute("insert into Tracks (Track_ID, Track_name, Artist_ID, Artist_name, Album_ID, Album_name, duration, popularity) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (track_id, track_name, track_art_id, track_art_name, track_album_id, track_album_name, track_duration, track_popular));
            #If the Track is not in the db, add
            if track_id not in tracks_id_attr_current:
                cursor.execute("insert into Track_Attributes (Track_ID, Track_name, Artist_ID, Artist_name, Album_ID, Album_name, duration, popularity, acousticness, danceability, energy, instrumentalness, loudness, temp, valence) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (track_id, track_name, track_art_id, track_art_name, track_album_id, track_album_name, track_duration, track_popular, acoust, dance, energy, instru, loud, tempo, valence));
                #cursor.execute("insert into User_Tracks (Track_ID, username) values (%s, %s)" , 
                #    (track_id, username))
                print("hi")
                cursor.connection.commit()
                cursor.close() 
    

    return tracks, tracks_id


# Get user top artists data for short, medium and long term
def get_all_user_top_artists(mysql, headers):
    times = ['short_term', 'medium_term', 'long_term']
    for time in times:

        url = 'https://api.spotify.com/v1/me/top/artists'
        params = {
            'time_range': time,    # short-term: 4 weeks, medium_term: 6 months, long term: years
            'limit': 50,       # max is 50
            'offset': 0       # start from the first item
        }

        data = requests.get(url=url, params=params, headers=headers).json()
        artists = []
        artists_id_db = []
        artists_id = []
        username = get_user(mysql, headers)
        for item in data['items']:
            artist_name = item['name']
            artists.append(artist_name)
            artist_id = item['id']
            artists_id.append(artist_id)
            # Select the artist id from the database
            cursor = mysql.connection.cursor()
            cursor.execute("select Artist_ID from Artist");
            artists_id_db = [row[0] for row in cursor.fetchall()]
            cursor.execute("select Artist_ID, username from User_Artist")
            User_Artists = cursor.fetchall()
            Art_User = '_'.join([artist_id , username])
            User_Artist = []
            for x in range(len(User_Artists)):
                 User_Artist.append('_'.join(User_Artists[x]))
            print(Art_User)
            if Art_User not in User_Artist:
                cursor.execute("insert into User_Artist (Artist_ID, username) values (%s, %s)" ,
                     (artist_id, username))
            # If the artist id does not already exist, add to the database
            if artist_id not in artists_id_db:
                cursor.execute("insert into Artist (Artist_ID, Artist_name) values (%s, %s)", 
                    (artist_id, artist_name));
            cursor.connection.commit()
            cursor.close()

    return artists, artists_id


def get_artists_genre(mysql, headers,id):
    url = 'https://api.spotify.com/v1/artists/{0}/'.format(id)
    params = {
        
    }
    
    data = requests.get(url=url, params=params, headers=headers).json()
    genre = data['genres']
    return genre

def get_user_stats(mysql, headers):
    username = get_user(mysql, headers)
    tracks, track_ids = get_user_top_tracks(mysql,headers)
    cursor = mysql.connection.cursor()
    cursor.execute("select Artist_ID from User_Tracks where username = '%s'" % username);
    artist_id = [row[0] for row in cursor.fetchall()]
    cursor.execute("select Artist_name from Tracks");
    artists = [row[0] for row in cursor.fetchall()]
    command = "select display_name from Users where username = '%s'" % username
    cursor.execute(command)
    name = str([row[0] for row in cursor.fetchall()])
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
    count = Counter(genres)
    count_artist = Counter(art)
    top_artist = count_artist.most_common(1)[0][0]
    top_genre = count.most_common(1)[0][0]
    # Select the artist id from the database
    
    cursor = mysql.connection.cursor()
    cursor.execute("select username from User_Stats");
    users_id = [row[0] for row in cursor.fetchall()]

    # If the artist id does not already exist, add to the database
    if username not in users_id:
        cursor.execute("insert into User_Stats (username, name, top_track_id, top_track, top_artist, top_genre) values (%s, %s, %s, %s, %s, %s)",         
            (username, name, top_track_id, top_track, top_artist, top_genre));
        cursor.connection.commit()
        cursor.close()

    elif username in users_id:
        command = "update User_Stats set top_track_id = '%s', top_track = '%s', top_artist = '%s', top_genre = '%s' where username = '%s'" % (top_track_id, top_track, top_artist, top_genre, username)
        cursor.execute(command);
        cursor.connection.commit()
        cursor.close()

# Get recommendations based on a list of lists of tracks within clusters
def get_recommendations(headers, tracks):
    # Spotify API endpoint
    url = 'https://api.spotify.com/v1/recommendations'

    # Request data from Spotify endpoint
    playlist = []
    for group in tracks:
        params = {
            'seed_tracks': ','.join(group),
            'limit': 2  
        }

        data = requests.get(url=url, params=params, headers=headers).json()
        for item in data['tracks']:
            playlist.append(item['uri'])
    
    # Return list of track uris to be in the playlist
    return playlist

# Create recommendation playlist
def create_rec_playlist(mysql, headers, playlist):
    # Create a new playlist
    user_id = get_user(mysql, headers)
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    params = {
        'name': 'BeatBook Recommendations'
    }
    headers['content-type'] = 'application/json'
    data = requests.post(url=url, json=params, headers=headers).json()
    
    # Add the recommended tracks to the playlist
    playlist_id = data['id']
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    params = {
        'uris': playlist
    }
    data = requests.post(url=url, json=params, headers=headers).json()


