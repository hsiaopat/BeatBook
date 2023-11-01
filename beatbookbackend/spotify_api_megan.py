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


def get_artists_genre(mysql, headers,id):
    url = 'https://api.spotify.com/v1/artists/{0}/'.format(id)
    params = {
        
    }
    
    data = requests.get(url=url, params=params, headers=headers).json()
    genre = data['genres']
    return genre

def get_user_stats(mysql, headers):
    username = get_user(mysql, headers)
    print(username)
    tracks, track_ids = get_user_top_tracks(mysql,headers)
    cursor = mysql.connection.cursor()
    cursor.execute("select Artist_ID from Tracks");
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
        print(command)
        cursor.execute(command);
        cursor.connection.commit()
        cursor.close()

#NOT IMPLEMENTED YET OR TESTED
def join_group(mysql,headers, g_id):
    cursor = mysql.connection.cursor()
    username = get_user(mysql, headers)
    command = "select display_name from Users where username = '%s'" % username
    cursor.execute(command)
    name = [row[0] for row in cursor.fetchall()]
    cursor.execute("select group_id from Clubs")
    groups_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("show tables")
    tables = [row[0] for row in cursor.fetchall()]
    group_name_id = 'Group_%s' % g_id
    if (g_id in groups_ids and group_name_id in tables):
        command = "select Member_username from %s" % group_name_id
        cursor.execute(command)
        current_members = [row[0] for row in cursor.fetchall()]
        if username not in current_members:
            cursor.execute("insert into Group_%s (Member_username, Member_name) values (%s, %s)",
                (g_id, username, name))
            cursor.execute("update Clubs set num_members = num_members+1 where group_id = '%s'" , g_id)
            cursor.connection.commit()
            cursor.close()
        else:
            print("User already in group")
    else:
        print("Group does not exist. You must first create the group")

#NOT IMPLEMENTED OR TESTED
def create_group(mysql, headers, group_name):
    username = get_user(mysql, headers)
    cursor.mysql.connection.cursor()
    command = "select display_name from Users where username = '%s'" % username
    cursor.execute(command)
    name = [row[0] for row in cursor.fetchall()]
    cursor.execute("select group_id from Clubs")
    groups_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("select group_id from Clubs order by group_id desc limit 1")
    new_id = [row[0] for row in cursor.fetchall()]+1
    while new_id in groups_ids:
        new_id = new_id+1
    if new_id not in groups_ids:
        cursor.execute("insert into Clubs (group_id, group_name, num_members) values (%s, %s, 1)",
            (new_id, group_name))
        command = "create table Group_%s(Member_username varchar(50) primary key, Member_name varchar(100)" % new_id
        cursor.execute(command)
        command = "insert into Group_%s (Member_username, Member_name) values (%s, %s)" % (username, name)
        cursor.execute(command)
        cursor.connection.commit()
        cursor.close()


#NOT IMPLEMENTED OR TESTED
def leave_group(mysql, headers, group_id):
    username = get_user(mysql, headers)
    cursor.mysql.connection.cursor()
    group_name_id = "Group_%s" % group_id
    cursor.execute("show tables")
    tables = [row[0] for row in cursor.fetchall()]
    if group_name_id in tables:
        command = "select Member_username from Group_%s" % group_id
        cursor.execute(command)
        current_members = [row[0] for row in cursor.fetchall()]
        if username in current_members:
            #USES DELETE NEED TO EVALUATE
            command = "delete from Group_%s where Member_username = '%s" % (group_id, username)
            cursor.execute(command)
            cursor.connection.commit()
            cursor.close()
#NOT IMPLEMENTED OR TESTED
#NEED TO FIGURE OUT WHO CAN DELETE GROUPS
def delete_group(mysql, headers):
    print("Help")
