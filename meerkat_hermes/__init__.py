"""
meerkat_hermers.py

Root Flask app for the Meerkat Hermes messaging module.
"""
from flask import Flask
from flask.json import JSONEncoder
from flask_restful import Api, reqparse
import boto3

# Create the Flask app
app = Flask(__name__)
app.config.from_object('config.Development')
app.config.from_envvar('MEERKAT_HERMES_SETTINGS')
api=Api(app)

# Import the API resources
# Import them after creating the app, because they depend upon the app.
from meerkat_hermes.resources.subscribe import Subscribe
from meerkat_hermes.resources.email import Email
from meerkat_hermes.resources.sms import Sms
from meerkat_hermes.resources.publish import Publish
from meerkat_hermes.resources.log import Log
from meerkat_hermes.resources.verify import Verify
from meerkat_hermes.authentication import require_api_key

# Add the API  resources.
api.add_resource(Subscribe, "/subscribe", "/subscribe/<string:subscriber_id>")
api.add_resource(Email, "/email")
api.add_resource(Sms, "/sms")
api.add_resource(Publish, "/publish")
api.add_resource(Log, "/log/<string:log_id>")
api.add_resource(Verify, "/verify/<string:subscriber_id>")

#display something at /
@app.route('/')
@require_api_key
def hello_world():
    #Load the database 
    db = boto3.resource('dynamodb')
    table = db.Table('hermes_subscribers')
    return table.creation_date_time.strftime('%d/%m/%Y')
