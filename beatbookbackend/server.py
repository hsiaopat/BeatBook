from flask import Flask, request, render_template, render_template_string, redirect
from auth import *

app = Flask(__name__)

headers = {}

@app.route('/')
def home():
    global headers
    
    if 'Authorization' in headers:
        return ('Hello ' + get_user(headers))
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

if __name__ == '__main__':
    # run the application on port 5028 of the student machine
    app.run(host='0.0.0.0', port=5028)
