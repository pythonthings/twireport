from twitter import OAuth, TwitterStream
import os
import dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)


class Twitter():
    '''
    Wrapper around TwitterStream API to authenticate, connect and get live stream data.
    Read the docs: https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/connecting
    '''

    def __init__(self, *args, **kwargs):
        '''
        Initialize the API wrapper by getting and setting all the credentials from .env file
        '''
        self.ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
        self.ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
        self.CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
        self.CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

    def authenticate(self):
        '''
        Authenticate app using OAuth
        '''
        self.oauth = OAuth(self.ACCESS_TOKEN, self.ACCESS_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET)

    def connect(self, heartbeat_timeout=60 * 5):
        '''
        Initiate the connection to Twitter Streaming API.
        Heartbeat timeout is 90 seconds by default. If no new tweet is received by the stream,
        connection shall be terminated. Increase it to 5 minutes.
        '''
        self.stream = TwitterStream(auth=self.oauth, heartbeat_timeout=heartbeat_timeout)

    def filter(self, keyword=''):
        '''
        Get tweets filtered by keyword
        '''
        iterator = self.stream.statuses.filter(track=keyword)
        return iterator
