from flask_restful import Resource, reqparse    # Import our functions and Resource class from flask_restful
from app import app
from flask import redirect                       # Import our functions from Flask
from app import oauth                           # Import our oauth object from our app
import requests                                 # Import requests in order to make server sided requests


class TwitterAuthenticate(Resource):
    def get(self):
        # generating our signed OAuth Headers
        uri, headers, body = oauth.sign('https://twitter.com/oauth/request_token')
        # making a request to twitter with the OAuth parameters we just created
        res = requests.get(uri, headers=headers, data=body)
        # This returns a string with OAuth variables we need to parse
        res_split = res.text.split('&')  # Splitting between the two params sent back
        oauth_token = res_split[0].split('=')[1]  # Pulling our APPS OAuth token from the response.
        # redirecting to the login URL using our OAuth Token
        return redirect('https://api.twitter.com/oauth/authenticate?oauth_token=' + oauth_token, 302)