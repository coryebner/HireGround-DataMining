import tweepy, pickle, os
from dataMining.settings import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_CURSOR_FILE
from dataMining.twitter.tweet import Tweet




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
                    description = tweet.user.description
                    hashtags = tweet.entities.get('hashtags')
                    location = tweet.user.location
                    tweetObject = Tweet(text, name, screenName, description, hashtags, location)
                    print(tweetObject)
                    pickle.dump(tweetObject, self._filename)
                
                print('page: ' + str(pageCount) + '.....................')
                print('pages: ' + str(pageCount) + ' tweet count: ' + str(tweetCount) + '\n')
        except tweepy.TweepError:
            print('rate limit exceeded')
            os.sys.exit(0)
            
if __name__ == "__main__":
    
    c = Cursor(open(TWITTER_CURSOR_FILE, 'w'))
    c.page('#jobs information technology')
    
