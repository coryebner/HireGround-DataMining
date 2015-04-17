__author__ = "Justin Milanovic"
__version__ = "1.0.0"
__email__ = "justinmilanovic@gmail.com"
__status__ = "Development"


#------------------------------------------------------------------------------

from settings import STANFORD_NER, STANFORD_NER_JAR, TWITTER_REGEX, TWITTER_CUSTOM_STOPWORDS, TWITTER_CUSTOM_PHRASES_LEFT, TWITTER_CUSTOM_PHRASES_RIGHT,\
    TWITTER_US_STATES_2_WORD
from twitter.tweet import Tweet

import re

from textblob import TextBlob, Word
from textblob.wordnet import Synset

import nltk
from nltk.corpus import stopwords
from nltk.tag.stanford import NERTagger
from nltk.corpus.reader import TaggedCorpusReader

#------------------------------------------------------------------------------
# NER    
    
def stanford(tweet):
    st = NERTagger(STANFORD_NER, STANFORD_NER_JAR) 
    return st.tag(tweet.split())

def stanfordContext(tweet):
    t = stanford(tweet)

    nerList = []
    for x in t:
        x = t.pop()
        j = x[0].encode('ascii', 'replace')
        k = x[1].encode('ascii', 'replace')
        if k != 'O':
            nerList.append(j)
    return set(nerList)
       
def stopWords(tweet):
    #NLTK stop words - decommissioned
    #englishStops = stopwords.words('english')

    customStops = stopwords.words(TWITTER_CUSTOM_STOPWORDS)
    capitaldStops = [word.title() for word in customStops]
    combinedStops = set(capitaldStops).union(set(customStops))
    return combinedStops

def cityStateExtraction(tweet):
    regularExpression = re.compile(TWITTER_US_STATES_2_WORD)
    cityStateTuple = regularExpression.search(tweet.text)
    nerList = []
    if cityStateTuple is not None:
        cityStateTuple = cityStateTuple.groups()
        nerList = (stanfordContext("It's a nice day in " + cityStateTuple[0]))
    return nerList

def cleaner(tweet, stopWords):
    words = tweet.split()
    cleanedData = [word for word in words if word not in stopWords]
    cleanedData = " ".join(cleanedData)
    return cleanedData

#------------------------------------------------------------------------------

def regexEncoding(tweet):
    return re.sub(r'&amp', "&", tweet).strip()

def regexRemoval(tweet, regexList):
    text = tweet.text
    for expression in regexList:
        text = re.sub(expression, "", text).strip()   
    return text
 
def phraseLeft(tweet):
    text = tweet.text
    for phrase in TWITTER_CUSTOM_PHRASES_LEFT:
        index = text.find(phrase)
        if index != -1:
            index = index + len(phrase)
            text = (text[index:])
    return text

def phraseRight(tweet):
    text = tweet.text
    for phrase in TWITTER_CUSTOM_PHRASES_RIGHT:
        index = text.find(phrase)
        if index != -1:
            text = (text[:index])
    return text

# decommissioned    
def tags(tweet): 
    tweetTags = TextBlob(tweet).tags
    nounList = [pos[0] for pos in tweetTags if pos[1][0] == 'N']
    return ' '.join(nounList) 

# decommissioned
def nltkTags(tweet):
    text = nltk.word_tokenize(tweet)
    tags = nltk.pos_tag(text)
    return [pos[1] for pos in tags]

# decommissioned - causes changes to correctly spelled words    
def spellcheck(tweet):
    return TextBlob(tweet).correct()


#------------------------------------------------------------------------------
# runner

def runner(tweet):   
    if type(tweet) != Tweet:
        pass
    else: 
        cleanTweet = tweet
        locationList = cityStateExtraction(cleanTweet)
        nerList = stanfordContext(cleanTweet.text) 
        cleanTweet.text = regexRemoval(cleanTweet, TWITTER_REGEX)
        cleanTweet.text = phraseLeft(cleanTweet)
        cleanTweet.text = phraseRight(cleanTweet)        
        text = cleaner(cleanTweet.text, locationList)
        
        # ner - organization, location, person      
        text = cleaner(text, nerList)
        # stopwords
        text = cleaner(text, stopWords(text))
        # metadata
        text = cleaner(text, tweet.metaData())
        text = regexEncoding(text)
        return text.strip()
