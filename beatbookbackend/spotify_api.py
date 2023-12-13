import requests
import pprint
from collections import Counter
from pandas import DataFrame
from datetime import date

def get_user(mysql, headers, cursor=None):
    passed_cur = False
    if cursor:
        passed_cur = True

    # Request user's profile from the spotify API
    r = requests.get(url='https://api.spotify.com/v1/me', headers=headers)

    # Data from the request
    username = r.json()['id']
    display_name = r.json()['display_name']

    # Select the usernames from the database
    if not passed_cur:
        cursor = mysql.connection.cursor()
    cursor.execute("select username from Users");
    usernames = [row[0] for row in cursor.fetchall()]

    # If the user does not already exist, add to the database
    if username not in usernames:
        cursor.execute("insert into Users (username, display_name) values (%s, %s)", 
            (username, display_name));
        cursor.connection.commit()

    if not passed_cur:
        cursor.close()

    return username

def add_links(mysql, headers):
    cursor = mysql.connection.cursor()
    cursor.execute("select Track_ID, Track_name, Artist_ID, Artist_name, Album_ID, Album_name, duration, popularity, acousticness, danceability, energy, instrumentalness, loudness, temp, valence from Track_Attributes")
    df = DataFrame(cursor.fetchall(), columns = ['Track_ID', 'Track_name', 'Artist_ID', 'Artist_name', 'Album_ID', 'Album_name', 'duration', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'temp','valence'])
    for index, item in df.iterrows():
        url = 'https://api.spotify.com/v1/tracks/%s' % item['Track_ID']
        params = {
            
        }
        data = requests.get(url=url, params = params, headers=headers).json()
        artist_link = ""
        album_link = ""
        try:
            data['album']['images']
            album_link = (data['album']['images'][0]['url'])
        except:
            album_link = ""
        try:
            data['artists']['images']
            artist_link = (data['artists']['images'][0]['url'])
        except:
             artist_link = ""
        print(item['Album_name'])
        cursor.execute('select Track_ID from Track_Attributes_All')
        Track_Attributes_All = [row[0] for row in cursor.fetchall()]
        if item["Track_ID"] not in Track_Attributes_All:
             cursor.execute("insert into Track_Attributes_All (Track_ID, Track_name, Artist_ID, Artist_name, Album_ID, Album_name, duration, popularity, acousticness, danceability, energy, instrumentalness, loudness, temp, valence, Artist_link, Album_link) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (item['Track_ID'], item['Track_name'], item['Artist_ID'], item['Artist_name'], item['Album_ID'], 
                    item['Album_name'], item['duration'], item['popularity'], item['acousticness'], item['danceability'], item['energy'], 
                    item['instrumentalness'], item['loudness'], item['temp'], item['valence'], artist_link, album_link))
             cursor.connection.commit()

    cursor.close()
    print('Done')

def get_user_short_term_top_tracks(mysql, headers, username=None):
    if username is None:
        username = get_user(mysql, headers)
    cursor = mysql.connection.cursor()
    cursor.execute("select T.Track_name, T.Track_ID, T.Album_link \
                    from (select Tracks.Track_name, Tracks.Track_ID, Album_link, input_order \
                          from User_Tracks_All, Tracks, Track_Attributes \
                          where Track_Attributes.Track_ID = Tracks.Track_ID and username = %s and type ='short_term' and User_Tracks_All.Track_ID = Tracks.Track_ID and date = %s \
                          order by date desc \
                          limit 50) as T \
                    order by input_order", (username, date.today()))
    
    data = cursor.fetchall()
    tracks = [row[0] for row in data]
    track_ids = [row[1] for row in data]
    album_url = [row[2] for row in data]

    cursor.connection.commit()
    cursor.close
    return tracks, track_ids, album_url

def get_user_short_term_top_artists(mysql, headers, username=None):
    if username is None:
        username = get_user(mysql, headers)
    cursor = mysql.connection.cursor()
    
    cursor.execute("select T.Artist_name \
                    from (select Artist_name, input_order \
                            from User_Artists_All, Artist \
                            where username = %s and type ='short_term' and User_Artists_All.Artist_ID = Artist.Artist_ID and date = %s \
                            order by date desc \
                            limit 50) as T \
                    order by input_order",  (username, date.today()))
    

    artists = [row[0] for row in cursor.fetchall()]
    print(artists)
    

    cursor.execute("select T.Artist_ID from (select Artist.Artist_ID,input_order from User_Artists_All, Artist where username = %s and type ='short_term' and User_Artists_All.Artist_ID = Artist.Artist_ID and date = %s order by date desc limit 50) as T order by input_order", (username, date.today()))


    artist_ids = [row[0] for row in cursor.fetchall()]
    cursor.connection.commit()
    cursor.close
    return artists, artist_ids



# Get user top tracks for short, medium and long term
def get_user_top_tracks(mysql, headers, cursor=None):
    passed_cur = False
    if cursor:
        passed_cur = True

    times = ['short_term', 'medium_term', 'long_term']
    for time in times:

        url = 'https://api.spotify.com/v1/me/top/tracks'
        params = {
            'time_range': time,    # short-term: 4 weeks, medium_term: 6 months, long term: years
            'limit': 50,       # max is 50
            'offset': 0       # start from the first item
        }

        data = requests.get(url=url, params=params, headers=headers).json()
        username = get_user(mysql, headers, cursor)
        tracks = []
        tracks_id = []
        count = 1
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
            try:
                item['album']['images']
                album_link = (item['album']['images'][0]['url'])
            except:
                album_link = ""
            try:
                item['artists']['images']
                artist_link = (item['artists']['images'][0]['url'])
            except:
                artist_link = ""
            track_duration = item['duration_ms']
            track_popular = item['popularity']

            #Select the Track Id from the database
            if not passed_cur:
                cursor = mysql.connection.cursor()
            cursor.execute("select Track_ID from Tracks");
            tracks_id_current = [row[0] for row in cursor.fetchall()]
            cursor.execute("select Track_ID, username from User_Tracks_All")
            User_Tracks = cursor.fetchall()
            cursor.execute("select date from User_Tracks_All")
            User_Tracks_Date = [row[0] for row in cursor.fetchall()]
            cursor.execute("select Track_ID from Track_Attributes")
            tracks_id_attr_current = [row[0] for row in cursor.fetchall()]
            Track_User = '_'.join([track_id , username, str(date.today())])

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
                 T = '_'.join([('_'.join(User_Tracks[x])), str(User_Tracks_Date[x])])
                 User_Track.append(T)
            if Track_User not in User_Track:
                cursor.execute("insert into User_Tracks_All (Track_ID, username, type, date, input_order) values (%s, %s, %s, %s, %s)" ,        
                    (track_id, username, time, date.today(), count))

                cursor.connection.commit()
            if track_id not in tracks_id_current:
                cursor.execute("insert into Tracks (Track_ID, Track_name, Artist_ID, Artist_name, Album_ID, Album_name, duration, popularity) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (track_id, track_name, track_art_id, track_art_name, track_album_id, track_album_name, track_duration, track_popular))
                cursor.connection.commit()
            #If the Track is not in the db, add
            if track_id not in tracks_id_attr_current:
                cursor.execute("insert into Track_Attributes (Track_ID, Track_name, Artist_ID, Artist_name, Album_ID, Album_name, duration, popularity, acousticness, danceability, energy, instrumentalness, loudness, temp, valence, Artist_link, Album_link) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (track_id, track_name, track_art_id, track_art_name, track_album_id, track_album_name, track_duration, track_popular, acoust, dance, energy, instru, loud, tempo, valence, artist_link, album_link))
                #cursor.execute("insert into User_Tracks (Track_ID, username) values (%s, %s)" , 
                #    (track_id, username))
                cursor.connection.commit()
            
            count=count+1
            if not passed_cur:
                cursor.close() 

            #count=count+1
            #cursor.close() 

    

    return tracks, tracks_id


# Get user top artists data for short, medium and long term
def get_all_user_top_artists(mysql, headers, cursor=None):
    passed_cur = False
    if cursor:
        passed_cur = True

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
        username = get_user(mysql, headers, cursor)
        #username = get_user(mysql, headers)

        count = 1
        for item in data['items']:
            artist_name = item['name']
            artists.append(artist_name)
            artist_id = item['id']
            artists_id.append(artist_id)
            
            # Select the artist id from the database
            if not passed_cur:
                cursor = mysql.connection.cursor()
            cursor.execute("select Artist_ID from Artist");
            artists_id_db = [row[0] for row in cursor.fetchall()]
            cursor.execute("select Artist_ID, username from User_Artists_All")
            User_Artists = cursor.fetchall()
            cursor.execute("select date from User_Artists_All")
            User_Artists_Date = [row[0] for row in cursor.fetchall()]
            Art_User = '_'.join([artist_id , username,str(date.today())])
            User_Artist = []
            for x in range(len(User_Artists)):
                 T = '_'.join([('_'.join(User_Artists[x])), str(User_Artists_Date[x])])
                 User_Artist.append(T)
            if Art_User not in User_Artist:
                cursor.execute("insert into User_Artists_All (Artist_ID, username, type, date, input_order) values (%s, %s, %s, %s, %s)" ,        
                    (artist_id, username, time, date.today(), count))

            # If the artist id does not already exist, add to the database
            if artist_id not in artists_id_db:
                cursor.execute("insert into Artist (Artist_ID, Artist_name) values (%s, %s)", 
                    (artist_id, artist_name));
            count=count+1
            cursor.connection.commit()
            if not passed_cur:
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
    t_id = []
    t_name = []
    for group in tracks:
        params = {
            'seed_tracks': ','.join(group),
            'limit': 2  
        }

        response = requests.get(url=url, params=params, headers=headers)
        data = response.json()

        for item in data['tracks']:
            playlist.append(item['uri'])
            t_id.append(item['id'])
            t_name.append(item['name'])

    # Return list of track uris to be in the playlist
    return playlist, t_id, t_name

# Create recommendation playlist
def create_rec_playlist(mysql, headers, playlist, track_ids, track_names, group_id):
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
    print(data)

    cursor = mysql.connection.cursor()
    cursor.execute("select group_name from Clubs where group_id = %s", (group_id,))
    group_name = cursor.fetchall()
    for i in range(len(track_ids)):
        cursor.execute("select Playlist_ID from Playlists")
        playlist_ids = [row[0] for row in cursor.fetchall()]

        if playlist_id not in playlist_ids:
            cursor.execute("insert into Playlists (Group_ID, Group_name, Playlist_ID, User_ID, Track_ID, Track_name) values (%s, %s, %s, %s, %s, %s)", 
                (int(group_id), group_name, playlist_id, user_id, track_ids[i], track_names[i]))
            cursor.connection.commit()
    cursor.close()

