__author__ = "Justin Milanovic"
__version__ = "1.0.0"
__email__ = "justinmilanovic@gmail.com"
__status__ = "Development"


import tweepy, pickle, os
from settings import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from twitter.tweet import Tweet

class Cursor(object):
    def __init__(self, filehandle):
        self._api = self._initialize()
        self._filename = filehandle

    def _initialize(self):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.secure = True
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        return tweepy.API(auth)
        
    def page(self, query):    
        tweetCount = 0
        pageCount = 0
        try:
            for page in tweepy.Cursor(self._api.search, q=query, lang='en').pages():
                pageCount +=1
                for tweet in page:
                    tweetCount +=1

                    text = tweet.text
                    name = tweet.author.name
                    screenName = tweet.author.screen_name
                    #description is depricated in noise algorithm
                    description = tweet.user.description
                    hashtags = tweet.entities.get('hashtags')
                    location = tweet.user.location
                    tweetObject = Tweet(text=text, name=name, screenName=screenName, description=description, hashtags=hashtags, location=location)
                    print(tweetObject)
                    pickle.dump(tweetObject, self._filename)
                
                print('page: ' + str(pageCount) + '.....................')
                print('pages: ' + str(pageCount) + ' tweet count: ' + str(tweetCount) + '\n')
        except tweepy.TweepError:
            print('rate limit exceeded')
            # alternative: enter 15 minute time delay to continue instead of exiting
            os.sys.exit(0)

