from flask import Flask, request, render_template, render_template_string
from auth import *

app = Flask(__name__)

@app.route('/')
def home():
    #return render_template('.html', var=var)
    return 'Hello World'

@app.route('/login')
def login():
    print('login')
    return request_user_authorization()
    #return 'login'

@app.route('/callback')
def idk():
    print(request.query_string)
    return 'callback'

if __name__ == '__main__':
    # run the application on port 5028 of the student machine
    app.run(host='0.0.0.0', port=5028)
