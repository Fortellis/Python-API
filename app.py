from asyncio.windows_events import NULL
from flask import Flask, request
from flask_restful import Resource, Api
import logging

import jwt

from jwt import PyJWKClient

import json


app = Flask(__name__)
api = Api(app)

logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger

PREFIX = 'Bearer '

with open('inventory.json') as f:
  inventory = json.load(f)

class HelloWorld(Resource):
    def get(self):
        logger.info('Here\'s some logged info.')
        logger.info(request.headers['Authorization'].startswith(PREFIX))

        if not request.headers['Authorization'].startswith(PREFIX):
            return 'Not a Bearer token'

        if not 'Subscription-Id' in request.headers:
            return 'You must have a Subscription-Id.'      

        if not request.headers['Subscription-Id']=="7e465be1-4fef-4840-8b84-a95ab4c74f0c":
            return 'Not subscribed'
        
        logger.info(request.headers['Authorization'][len(PREFIX):])

        token = request.headers['Authorization'][len(PREFIX):]

        url = "https://identity.fortellis.io/oauth2/aus1p1ixy7YL8cMq02p7/v1/keys"

        jwks_client = PyJWKClient(url)
        
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="api_providers",
            options={"verify_exp": True},
        )
        
        print(data)
        
        logger.info(data)

       

        logger.info(inventory)

        ## logger.info(/inventory.json)

        return inventory
        
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)

