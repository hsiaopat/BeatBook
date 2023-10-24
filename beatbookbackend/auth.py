import requests
import base64
from cred import *

# Request Access Token
#   An access token provides the credentials and permissions that will be needed to access Spotify's API
#   These access tokens are valid for one hour
def request_client_credentials_access_token():
    url = 'https://accounts.spotify.com/api/token'
    data = { 
        'grant_type'    : 'client_credentials',
        'client_id'     : client_ID,
        'client_secret' : client_SECRET 
    }

    r = requests.post(url, data=data)

    # returns header for future API requests
    return {'Authorization' : 'Bearer ' + r.json()['access_token']}

# Request Authorization Code Access Token
#   Step 2 of being able to access user specific data
#   The auth_code will come from the redirect_uri url
def request_authcode_access_token(auth_code):
    url = 'https://accounts.spotify.com/api/token'
    redirect_uri = 'http://localhost:3000/callback'
    cred = f'{client_ID}:{client_SECRET}'
    cred = base64.b64encode(cred.encode('ascii')).decode('ascii')

    data = {
        'grant_type' : 'authorization_code',
        'code' : auth_code,
        'redirect_uri' : redirect_uri
    }
    headers = {
        'content-type' : 'application/x-www-form-urlencoded',
        'Authorization' : f"Basic {cred}"
    }
    r = requests.post(url, headers=headers, data=data)

    # currently using this for debugging, once it works we will want to return
    print(r.text)
    #return {'Authorization' : 'Bearer ' + r.json()['access_token']}


# Request User Authorization
#   Step 1 of being able to access user specific data
#   The GET request will provide a code which will be used to request a token
def request_user_authorization():
    url = 'https://accounts.spotify.com/authorize'
    redirect_uri = 'http://localhost:3000/callback'

    # The scope parameter will determine the user data that they are consenting access to
    # Different API endpoints will require different scopes which will be specified on the API website
    params = {
        'response_type' : 'code',
        'client_id' : client_ID,
        'scope' : 'user-read-private user-read-email',
        'redirect_uri' : redirect_uri 
    }

    r = requests.get(url, params=params) 


# This is an arbitrary function to scrape the Morgan Wallen I am currently listening to
#   Proves that the client credentials access token works
def get_album(headers):
    album_id = '6i7mF7whyRJuLJ4ogbH2wh'
    r = requests.get(url=f'https://api.spotify.com/v1/albums/{album_id}', headers=headers)
    print(r.json()['name'])


if __name__ == '__main__':
    # Get the access token and use the API to get data on an album
    #headers = request_client_credentials_access_token()
    request_authcode_access_token('0')
    #get_album(headers)
