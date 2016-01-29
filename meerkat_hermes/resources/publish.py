"""
This resource provides a simple means of sending a given e-mail message to given e-mail addresses.
"""

import uuid, boto3, json, uuid
import meerkat_hermes.util as util
from flask_restful import Resource, reqparse
from flask import jsonify, current_app
from boto3.dynamodb.conditions import Key, Attr


#This simple Emailer resource has just one method, which sends a given email message.
class Publish(Resource):

    def __init__(self):
        #Load the database 
        db = boto3.resource('dynamodb')
        self.subscribers = db.Table(current_app.config['SUBSCRIBERS'])
        self.subscriptions = db.Table(current_app.config['SUBSCRIPTIONS'])

    def put(self):
        """
        Publish a method to a given topic set. 
        First parse the given arguments to check it is a valid email.
        !!!Remember that whilst still in AWS "Sandbox" we can only send to verified emails.

        PUT args:

            'id'*         - If another message with the same ID has been logged, this one won't send.
            'message'*    - The message.
            'topics'*     - The topics the message fits into (determines destination address/es).
                            Accepts array of multiple topics.
            'medium'      - The medium by which to publish the message (email, sms, etc...)
                            Defaults to email. Accepts array of multiple mediums.
            'sms-message' - The sms version of the message. Defaults to the same as 'message'
            'html-message'- The html version of the message. Defaults to the same as 'message'
            'subject'     - The e-mail subject. Defaults to "".
 
        Returns:
            The amazon SES response.
        """

        #Define an argument parser for creating a valid email message.
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, type=str, help='The message Id - must be unique.')
        parser.add_argument('message', required=True, type=str, help='The message to be sent')
        parser.add_argument('topics', required=True, action='append', type=str, 
                            help='The destination address')
        parser.add_argument('medium', required=False, action='append', type=str, 
                            help='The destination address')
        parser.add_argument('html', required=False, type=str, 
                            help='If applicable, the message in html')
        parser.add_argument('subject', required=False, type=str, help='The email subject')
        args = parser.parse_args()

        #Check that the message hasn't already been sent.
        if util.id_valid(args['id']):

            #Set the default values for the non-required fields.
            if 'medium' not in args: args['medium'] = ['email']
            if 'html-message' not in args: args['html-message'] = args['message']
            if 'sms-message' not in args: args['sms-message'] = args['message']
            if 'subject' not in args: args['subject'] = ''
    
            #Collect the subscriber IDs for all subscriptions to the given topics.
            subscribers = []
    
            for topic in args['topics']:
                query_response = self.subscriptions.query(
                    IndexName='topicID-index',
                    KeyConditionExpression=Key('topicID').eq(topic)
                )
                for item in query_response['Items']:
                    subscribers.append( item['subscriberID'] )
            
            #Record details about the sent messages.
            responses = []
            destinations = []

            #Send the messages to each subscriber.     
            for subscriber_id in subscribers:    
                #Get subscriber's details.        
                subscriber = self.subscribers.get_item(
                    Key={ 'id':subscriber_id }
                )['Item']
    
                #TODO: Keywords management here.

                #Assemble and send the messages for each medium.
                for medium in args['medium']: 
                    

                    if medium == 'email':
                        temp = util.send_email(
                            subscriber['email'],
                            args['subject'],
                            args['message'],
                            args['html-message']
                        )
                        temp['type'] = 'email'
                        responses.append(temp)
                        destinations.append( subscriber['email'] )  

                    elif medium == 'sms' and 'sms' in subscriber:
                        temp = util.send_sms(
                            subscriber['sms'],
                            args['sms-message']
                        )
                        temp['type'] = 'sms'
                        responses.append( temp )  
                        destinations.append( subscriber['sms'] )
                             

            util.log_message( args['id'], {
                'destination': destinations, 
                'medium': args['medium'], 
                'time': util.get_date(),
                'message': args['message']
            })
            
            return responses, 200

        else:
            #If the message Id already exists, return with a 400 bad request response.
            return "400 Bad Request: id already exists", 400
