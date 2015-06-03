"""
#!/usr/bin/env python
"""
from datetime import datetime, timedelta
import os
import jwt
import json
import requests
from functools import wraps
from urlparse import parse_qs, parse_qsl
from urllib import urlencode
from flask import  g, request, redirect, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from requests_oauthlib import OAuth1
from jwt import DecodeError, ExpiredSignature
import urllib2
import math

from db import session
import classes as cls

from flask import Flask
from flask.ext.restful import Api
from flask.ext.cors import CORS
from flask import send_file
import os

# Configuration
current_path = os.path.dirname(__file__)
client_path = os.path.abspath(os.path.join(current_path, 'static'))

application = Flask(__name__, static_url_path='', static_folder=client_path)

# Set application.debug=true to enable tracebacks on Beanstalk log output. 
# TBD: Make sure to remove this line before deploying to production.
application.debug=True

""" 
@application.route('/')
def sanity():
    return "BF Backend is up and running."
"""

# Set CORS options on app configuration

application.config['CORS_HEADERS'] = "Content-Type"
application.config['CORS_RESOURCES'] = {r"*": {"origins": "*"}}
cors = CORS(application)

api = Api(application)

from resources import UserResource
from resources import BidResource
from resources import ContributionResource
from resources import CloseContributionResource


# API:
api.add_resource(UserResource, '/users/<string:id>', endpoint='users')
api.add_resource(UserResource, '/users', endpoint='user')

api.add_resource(BidResource, '/bids/<string:id>', endpoint='bids')
api.add_resource(BidResource, '/bids', endpoint='bid')

api.add_resource(ContributionResource, '/contribution', endpoint='contribution')
api.add_resource(ContributionResource, '/contribution/<string:id>', endpoint='contributions')

api.add_resource(CloseContributionResource, '/contribution/close/<string:id>', endpoint='closeContribution')




# Navigation:
@application.route('/')
def index():
    return send_file('static/index.html')
  
# Auth:


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authHeader = request.headers.get('x-access-token')
        if not authHeader:
            response = jsonify(message='Missing authorization header:'+str(authHeader))
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function



# API - ME :
@application.route('/api/me',methods=['GET'])
@login_required
def me():
    if(not g.user_id):
        print 'User Not Logged In.',404
        return 'User Not Logged In.',404
	
    #user = User.query.filter_by(id=g.user_id).first()
    user = session.query(cls.User).filter(cls.User.id == g.user_id).first()
    
    if(not user):
        print 'User Not Logged In.',404
        return 'User Not Logged In.',404	
    
    return jsonify(	dict(id=user.slack_id,displayName=user.name))

SLACK_SECRET = os.environ.get('SLACK_SECRET') or 'e7efc9a81d4043defb7b7e27816ae27e'
TOKEN_SECRET = os.environ.get('SECRET_KEY') or 'JWT Token Secret String'
def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.now(),
        'exp': datetime.now() + timedelta(days=14)
    }
    token = jwt.encode(payload, TOKEN_SECRET)
    return token.decode('unicode_escape')


def parse_token(req):
    authHeader = req.headers.get('x-access-token')
    print 'parse_token: authHeader:'+str(authHeader)
    token = authHeader.split()[1]
    return jwt.decode(token, TOKEN_SECRET)

@application.route('/auth/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.json['email']).first()
    if not user or not user.check_password(request.json['password']):
        response = jsonify(message='Wrong Email or Password')
        response.status_code = 401
        return response
    token = create_token(user)
    return jsonify(token=token)


@application.route('/auth/signup', methods=['POST'])
def signup():
    user = User(email=request.json['email'], password=request.json['password'])
    db.session.add(user)
    db.session.commit()
    token = create_token(user)
    return jsonify(token=token)


# Services Auth Routes:
@application.route('/auth/slack', methods=['POST'])
def slack():
    access_token_url = 'https://slack.com/api/oauth.access'
    users_api_url = 'https://slack.com/api/auth.test'

    params = {
        'client_id': request.json['clientId'],
        'redirect_uri': request.json['redirectUri'],
        'client_secret': SLACK_SECRET,
        'code': request.json['code']
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.get(access_token_url, params=params)
    print 'r.text:'+str(r.text)

    response = json.loads(r.text)
    print str(response)
    access_token = response["access_token"]
    
    headers = {'User-Agent': 'DEAP'}
    print 'access_token:'+str(access_token)

    # Step 2. Retrieve information about the current user.
    r = requests.get(users_api_url, params={'token':access_token}, headers=headers)
    profile = json.loads(r.text)
    print 'slack profile:'+str(profile)
    	   
    # Step 3. (optional) Link accounts.
    if request.headers.get('x-access-token'):
        #user = User.query.filter_by(slack=profile['user_id']).first()
        user = session.query(cls.User).filter(slc.User.slack_id == profile['user_id']).first()

        if user:
            response = jsonify(message='There is already a Slack account that belongs to you')
            response.status_code = 409
            return response

        payload = parse_token(request)

        #user = User.query.filter_by(id=payload['sub']).first()
        user = session.query(cls.User).filter(slc.User.id == payload['sub']).first()

        if not user:
            response = jsonify(message='User not found')
            response.status_code = 400
            return response

        u = User(slack_id=profile['user_id'], name=profile['user'])
        session.add(u)
        session.commit()
        token = create_token(u)
        return jsonify(token=token)

    # Step 4. Create a new account or return an existing one.
    #user = User.query.filter_by(slack=profile['user_id']).first()
    user = session.query(cls.User).filter(cls.User.slack_id == profile['user_id']).first()

    if user:
        token = create_token(user)
        return jsonify(token=token)

    print 'slack profile:'+str(profile)
    #u = cls.User(slack_id=profile['user_id'], name=profile['user'])
    jsonStr = {"slack_id":profile['user_id'],"name":profile['user']}
    u = cls.User(jsonStr,session)
    session.add(u)
    session.commit()
    token = create_token(u)
    return jsonify(token=token)

  
if __name__ == '__main__':
    #application.run(host='0.0.0.0',debug=True)
    application.run(debug=True)


# BUG: app loads from one session , world eng writes logs on another, app server needs to be restarted for changes from eng to take effect
# TBD: read ENV variable (when in DEV) to aestablish DB engine connect string (DEV/PROD)
# TBD: CORS needed?
# TBD: set up  engine as AWS worker tier