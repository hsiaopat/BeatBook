from flask import Flask, request, render_template, render_template_string
from flask import redirect, session
from flask_mysqldb import MySQL
from auth import *
from spotify_api import *
from flask import jsonify  
from flask_cors import CORS
import logging
from groups import *
from playlist_cluster import *

# Create a new flask instance
app = Flask(__name__)
logging.getLogger('flask_cors').level = logging.DEBUG
CORS(app, resources={r"/toptracks": {"origins": "*"},
                     r"/topartists": {"origins": "*"},
                     r"/joingroup": {"origins": "*"},
                     r"/creategroup": {"origins": "*"},
                     r"/leavegroup": {"origins": "*"},
                     r"/displaygroups": {"origin": "*"}})

# Global headers variable
headers = {}

app.secret_key='mschmi26'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mschmi26'
app.config['MYSQL_PASSWORD'] = 'goirish'
app.config['MYSQL_DB'] = 'chackl'

mysql = MySQL(app)

# Temporary endpoint to test clustering algorithm
@app.route('/test')
def test():
    tracks = find_clusters(mysql)
    tracks = get_recommendations(headers, tracks)
    create_rec_playlist(mysql, headers, tracks)
    return 'works'

@app.route('/')
def home():
    global headers
    
    if 'Authorization' in headers:
        # Get the username from get_user spotify API call
        username = get_user(mysql, headers)
        tracks, tracks_id = get_user_top_tracks(mysql, headers)
        artists,artists_id = get_all_user_top_artists(mysql,headers)
        #get_user_stats(mysql,headers)
        # Select from the database to get the user display_name
        cursor = mysql.connection.cursor()
        cursor.execute("select display_name from Users where username = %s", (username,));
        display_name = cursor.fetchall()[0][0]
        cursor.close()

        return (f'Hello {display_name}')
    return 'Hello World'


@app.route('/login')
def login():
    # login function redirects to callback screen after Spotify user authorization
    return redirect(request_user_authorization())


@app.route('/callback')
def callback():
    # use the user authorization to get an access code to get their personal data
    #   from the Spotify API
    global headers
    headers = request_authcode_access_token(request.args.get('code'))
    return redirect('http://129.74.153.235:5029/')

@app.route('/toptracks')
def top_tracks():
    global headers

    if 'Authorization' in headers:
        # Get the username from the get_user Spotify API call
        username = get_user(mysql, headers)

        # Get the user's top tracks
        tracks, tracks_id = get_user_top_tracks(mysql, headers)
        print(tracks)
        # Render a template or return the data in JSON format
        return jsonify({'tracks': tracks, 'tracks_id': tracks_id})

    return 'Hello World'

@app.route('/topartists')
def top_artists():
    global headers

    if 'Authorization' in headers:
        # Get the username from the get_user Spotify API call
        username = get_user(mysql, headers)

        # Get the user's top tracks
        artists, artists_id = get_all_user_top_artists(mysql, headers)
        print(artists)
        # Render a template or return the data in JSON format
        return jsonify({'artists': artists, 'artists_id': artists_id})

    return 'Hello World'

@app.route('/joingroup', methods=['POST'])
def join_group_route():
    global headers
    print(request.json)
    if 'Authorization' not in headers:
        return jsonify({"error": "Unauthorized"}), 401

    g_id = request.json.get('group_identifier')  # Assuming the group_id is passed in the request JSON
    if not g_id:
        return jsonify({"error": "Group ID not provided"}), 400

    # Call your join_group function here
    result, message = join_group(mysql, headers, g_id)

    if result:
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "error": message})
    

@app.route('/creategroup', methods=['POST'])
def create_group_route():
    global headers

    if 'Authorization' not in headers:
        return jsonify({"error": "Unauthorized"}), 401

    group_name = request.json.get('group_name')  # Assuming the group_name is passed in the request JSON
    if not group_name:
        return jsonify({"error": "Group name not provided"}), 400

    # Call your create_group function here
    result, message = create_group(mysql, headers, group_name)

    if result:
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "error": message})
    

@app.route('/leavegroup', methods=['POST'])
def leave_group_route():
    global headers

    if 'Authorization' not in headers:
        return jsonify({"error": "Unauthorized"}), 401

    group_identifier = request.json.get('group_identifier')  # Assuming the group_id is passed in the request JSON
    if not group_identifier:
        return jsonify({"error": "Group ID not provided"}), 400

    # Call your leave_group function here
    result, message = leave_group(mysql, headers, group_identifier)

    if result:
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "error": message})
    
@app.route('/displaygroups')
def display_groups_route():
    global headers

    if 'Authorization' not in headers:
        return jsonify({"error": "Unauthorized"}), 401

    # Call your display_groups function here
    groups = display_groups(mysql, headers)
    print(groups)

    # Render a template or return the data in JSON format
    return jsonify({'groups': groups})


if __name__ == '__main__':
    # make changes in real time
    app.debug = True

    # run the application on port 5028 of the student machine
    app.run(host='0.0.0.0', port=5028)
