import requests
import pprint

# Get user profile data
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
    for item in data['items']:
        track_name = item['name']
        tracks.append(track_name)
    print(tracks)

    return tracks


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
    for item in data['items']:
        artist_name = item['name']
        artists.append(artist_name)
    print(artists)

    return artists
