__author__ = "Justin Milanovic"
__version__ = "1.0.0"
__email__ = "justinmilanovic@gmail.com"
__status__ = "Development"


import tweepy, json, pickle
from settings import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from twitter.tweet import Tweet


class StdOutListener(tweepy.StreamListener):
    
    def __init__(self, filehandle):
        self._filehandle = filehandle    
    
    def on_data(self, data):
        decoded = json.loads(data)
             
        text = decoded['text']
        name = decoded['user']['name']
        screenName = decoded['user']['screen_name']
        # description is depricated in noise algorithm
        description = decoded['user']['description']
        hashtags = decoded['entities']['hashtags']
        location = decoded['user']['location']
        tweet = Tweet(text=text, name=name, screenName=screenName, description=description, hashtags=hashtags, location=location)
        
        print(tweet)
        return True
          
    def pickleTweet(self, data):
        pickle.dump(data, self._filehandle)

    def on_error(self, status):
        print status
        
class Stream(object):
    
    def __init__(self, listener, query):
        self._auth = self._getToken() 
        self._listener = listener
        self._query = query
        self._stream = self._initialize()   

    def _getToken(self):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)       
        return auth
    
    def _initialize(self):
        stream = tweepy.Stream(self._auth, self._listener)
        stream = stream.filter(track=[self._query]) 
        return stream   

    
    