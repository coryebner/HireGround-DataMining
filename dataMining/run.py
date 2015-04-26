
#! /usr/bin/env python

__author__ = "Justin Milanovic"
__copyright__ = "Copyright 2015, HireGround"
__version__ = "1.0.0"
__email__ = "justinmilanovic@gmail.com"
__status__ = "Development"


import argparse, pickle, sys

from twitter.extraction import runner
from twitter.cursor import Cursor 
from twitter.stream import StdOutListener, Stream
from twitter.tweet import Tweet
from google.googleProcessing import googleJobs, googleSkills
from google.query import runSkills, runTitles
from google.test.googleTests import test 
from google.webScraper.fullSnippetTest import snippetTest
from mongo.Job import Job

from settings import TWITTER_CURSOR_FILE, TWITTER_STREAM_FILE, GOOGLE_TITLE_SNIPPET_FILENAME, GOOGLE_SKILL_SNIPPET_FILENAME
from settings import GOOGLE_PROCESS_TITLE, GOOGLE_JOB_TITLE, GOOGLE_SKILL_TITLE, GET_FULL_SNIPPET

def getArgs():
    parser = argparse.ArgumentParser(description='data mining app')
    parser.add_argument('-t', '--cursorclean', type=str, action="store", )    
    parser.add_argument('-tc', '--cursor', type=str, action="store", )
    parser.add_argument('-ts', '--stream', type=str, action="store", )
    return parser.parse_args()

def twitterCursor(query):
    c = Cursor(open(TWITTER_CURSOR_FILE, 'w'))
    c.page(query)
    c.close()

def twitterStream(query):
    listener = StdOutListener(open(TWITTER_STREAM_FILE, 'w'))
    Stream(listener, query)
    
def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass
    
def twitterCursorClean(test):

    with open(TWITTER_CURSOR_FILE, 'r') as f:
        for tweet in pickleLoader(f):
            print(tweet)
            cleanText = runner(tweet)
            print("ANSW: " + cleanText)
            print('-------------------')
    file.close()

def twitterStreamClean(test):

    with open(TWITTER_STREAM_FILE, 'r') as f:
        for tweet in pickleLoader(f):
            cleanText = runner(tweet)

            print(tweet)
            print(cleanText)
            print('-------------------')
    file.close()

#GOOGLE FUNCTIONS    
def googleGetJobTitles():
    googleJobs(GOOGLE_PROCESS_TITLE)
    
def googleGetSkills():
    googleSkills(GOOGLE_PROCESS_TITLE)

def googleQueryTitles(): 
    runTitles(GOOGLE_JOB_TITLE, GOOGLE_TITLE_SNIPPET_FILENAME, GET_FULL_SNIPPET)
   
def googleQuerySkills():
     runSkills(GOOGLE_JOB_TITLE, GOOGLE_SKILL_TITLE, GOOGLE_SKILL_SNIPPET_FILENAME, GET_FULL_SNIPPET)
   
   
def googleAlgorithmTest():
    test()

def fullSnippetAlgorithmTest():
    runTitles(GOOGLE_JOB_TITLE, "outputNew", False)
    snippetTest()

def dataBaseView():
    data = Job()
    data.printall()
        
    
available_actions = {"cursor": twitterCursor, "stream": twitterStream, "cursorclean": twitterCursorClean,}

if __name__=='__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "-qs":
            googleQuerySkills()
        elif sys.argv[1] == "-qt":
            googleQueryTitles()
        elif sys.argv[1] == "-gt":
            googleAlgorithmTest()
        elif sys.argv[1] == "-ps":
            googleGetSkills()
        elif sys.argv[1] == "-pt":
            googleGetJobTitles()
	elif sys.argv[1] == "-ft":
            fullSnippetAlgorithmTest()
        elif sys.argv[1] == "-printData":
            dataBaseView()
    else:
        args = vars(getArgs())
        l = [{k:v} for k, v in args.iteritems() if v is not None]
        method, methodArgs = l.pop().popitem()
        available_actions[method](methodArgs)
