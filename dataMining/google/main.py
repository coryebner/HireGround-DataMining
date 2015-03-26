'''
Created on Oct 23, 2014

@author: Cory
@author: Matt
'''

import urllib2
import urllib
import pprint
import nltk
import re
from apiclient.discovery import build
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def manualProcessing(word):
    if word.endswith("ment"):
        withoutSuffix = word[:-len('ment')]
        if withoutSuffix.endswith('e'):
            withoutSuffix = withoutSuffix[:-len('e')]
        word = withoutSuffix + 'er'
    return word

def additionalProcessing(sentanceTokens):
    
    for i in xrange(0,len(sentanceTokens)):
        for x in xrange(0,len(sentanceTokens[i])):
            #Lemmatization
            lmtzr = WordNetLemmatizer()
            sentanceTokens[i][x] = lmtzr.lemmatize(sentanceTokens[i][x])
            
            #Manual Processing
            sentanceTokens[i][x] = manualProcessing(sentanceTokens[i][x])
            
            #print sentanceTokens[i][x]
    
    return sentanceTokens
    

def preprocess(text):
    tokens = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in tokens]
    #Additional Processing
    tokens = additionalProcessing(tokens)
    tokens = [nltk.pos_tag(word) for word in tokens]
    return tokens

def processText(file, jobTitles):
    f = open(file, 'r')
    text = f.read()
    
    text = text.replace("\\n", "")
    #text = text.replace("\\xa0", "")
    #text = text.replace("\\u201c", "")
    #text = text.replace("\\u201d", "")
    #text = text.replace("u'", "")
    
    #text = re.sub("\\n$", "", text)
    #text = re.sub("\\xa0$", "", text)
    #text = re.sub("\\u201c$", "", text)
    #text = re.sub("\\u201d$", "", text)
    #text = re.sub("u'$", "", text)
    
    #print(text)
    text = "computers programmers management."
    
    tokens = preprocess(text)
    
    #print tokens
    #list: {(<NN|JJ|VB|IN|VBG>+<,>)+(<CC><NN|JJ|VB|IN|VBG>+)*}
    '''grammar = """
            comma: {<NN|JJ|VB|IN|VBG>+<,>}
            endlist: {<CC>(<NN|JJ|VB|IN|VBG>+)}
            list: {<comma>+(<endlist>)}
            
            
            
            """'''
    grammar = """
            list: {(<NN|NNS|NNP|VB|VBG|JJ|CC|PRP|IN|TO>+<,>)+}
            and: {<NN|NNS|JJ|VB|IN|VBG>*<CC><NN|NNS|JJ|VB|IN|VBG>+}
            """
            
    #grammar = "and: {(<NN|NNS|JJ|VB|IN|VBG>+<,>)+<NN|NNS|JJ|VB|IN|VBG>*<CC><NN|NNS|JJ|VB|IN|VBG>+}"
    cp = nltk.RegexpParser(grammar)
    
    stop = stopwords.words('english')
    additionalStopwords = ["list", "others", "benefits", "after", "uses", "use",
                           "jobs", "professionals", "occupations", "including",
                           "like", "such", "as", "interview"]
    
        
    for sentence in tokens: 
          
        multiName = []
        #break
        result = cp.parse(sentence)
          
        for node in result:
                      
            name = list(" ")
            counter = 0
            if type(node) is nltk.Tree:
                if node.label() == 'list':
                    #print node
                    #break
                    for element in node:
                        #print element[0]
                        if element[1] == ",":
                            counter = counter + 1
                            name.append("")
                            continue
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append("")
                            continue
                        else:
                            if element[0].strip() in stop or element[0].strip() in additionalStopwords:
                                name[counter] = ""
                            elif element[1] == "IN" or element[1] == "NNP" or element[1] == "TO":
                                name[counter] = ""
                            else:
                                #name[counter] = name[counter] + element[0] + " " + "(" + element[1] + ")" + " "
                                name[counter] = name[counter] + element[0] + " "
                  
                elif node.label() == 'and':
                    for element in node:
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append("")
                            continue
                        else:
                            if element[0].strip() in stop or element[0].strip() in additionalStopwords:
                                name[counter] = ""
                            elif element[1] == "IN" or element[1] == "NNP" or element[1] == "TO":
                                name[counter] = ""
                            else:
                                #name[counter] = name[counter] + element[0] + " " + "(" + element[1] + ")" + " "
                                name[counter] = name[counter] + element[0] + " "
 
                     
                                 
            if len(name) == 1:
                if name[0] == " " or name[0] == "":
                    continue
            if len(name) == 2:
                if name[0] == "" and name[1] == "":
                    continue
             
            if "/" in name:
                multiName = name.split("/")
                print "found a multi name"
                 
            if len(multiName) > 0:
                for additionalName in multiName:
                    print additionalName
            else:
                for singleName in name:
                    if singleName != "" and singleName != " ":
                        if not singleName.strip() in jobTitles:
                            jobTitles.append(singleName.strip())
                    
                #print name
                
            
''' END OF processText() FUNCTION '''

#nltk.download('all')


query = " "

jobTitles = ["software engineer"]

processText("output/outputNew.txt", jobTitles)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(jobTitles)
#print jobTitles
print len(jobTitles)

#print(jobs)



        
        





