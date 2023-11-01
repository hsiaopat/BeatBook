from flask import Flask, request, render_template, render_template_string
from flask import redirect, session
from flask_mysqldb import MySQL
from auth import *
from spotify_api import *

# Create a new flask instance
app = Flask(__name__)

# Global headers variable
headers = {}

app.secret_key='mschmi26'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mschmi26'
app.config['MYSQL_PASSWORD'] = 'goirish'
app.config['MYSQL_DB'] = 'chackl'

mysql = MySQL(app)

@app.route('/')
def home():
    global headers
    
    if 'Authorization' in headers:
        # Get the username from get_user spotify API call
        username = get_user(mysql, headers)
        tracks, tracks_id = get_user_top_tracks(mysql, headers)
        artists,artists_id = get_user_top_artists(mysql,headers)
        #get_user_stats(mysql,headers)
        top_tracks = display_top_tracks(mysql, headers)
        top_artists = display_top_artists(mysql,headers)
        groups = display_groups(mysql, headers)
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
    return redirect('/')
@app.route('/join-group')
def j_group():
    join_group(mysql, headers, 1)
    return redirect('http://localhost:3000/home')

@app.route('/create-group')
def c_group():
    create_group(mysql, headers, 'hi')
    return redirect('http://localhost:3000/home')

@app.route('/leave-group')
def l_group():
    leave_group(mysql, headers, 1)
    return redirect('http://localhost:3000/home')

if __name__ == '__main__':
    # make changes in real time
    app.debug = True

    # run the application on port 5028 of the student machine
    app.run(host='0.0.0.0', port=5028)
