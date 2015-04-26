'''
Created on Jan 20, 2015

@author: Matt Bahler, Cory Ebner
@Description: This module uses processes the snippets and extracts the relevant information
@output: It stores the information onto the Mongo Database and displays the results on the command line
@Date: Last Revised Apr. 12 2015
'''

import pprint
import nltk
from mongo.Job import Job
from nltk.corpus import stopwords
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from settings import GOOGLE_ADDITIONAL_PROCESSING, GOOGLE_MANUAL_PROCESSING, GRAMMAR, ADDITIONAL_STOP_WORDS_SKILLS, ADDITIONAL_STOP_WORDS_TITLES
from settings import GOOGLE_TITLE_SNIPPET_FILENAME, GOOGLE_SKILL_SNIPPET_FILENAME, GET_FULL_SNIPPET

'''
Performs manual text processing on the given word
word - the word to perform the manual testing on
'''
def manualProcessing(word):
    if(GOOGLE_MANUAL_PROCESSING == 1):
        if word.endswith("ment"):
            withoutSuffix = word[:-len('ment')]
            if withoutSuffix.endswith('e'):
                withoutSuffix = withoutSuffix[:-len('e')]
                word = withoutSuffix + 'er'
    return word

'''
Performs additional processing on a given sentence token
sentenceToken - a sentence created by nltk.sent_tokenize()
'''
def additionalProcessing(sentenceTokens):
    if(GOOGLE_ADDITIONAL_PROCESSING == 1):
        for i in xrange(0,len(sentenceTokens)):
            for x in xrange(0,len(sentenceTokens[i])):
                #Lemmatization
                lmtzr = WordNetLemmatizer()
                sentenceTokens[i][x] = lmtzr.lemmatize(sentenceTokens[i][x])
            
                #Manual Processing
                sentenceTokens[i][x] = manualProcessing(sentenceTokens[i][x])
            
                #print sentenceTokens[i][x]
    return sentenceTokens
    
'''
Performs text preprocessing so it can be worked with
text - the text to be processed
'''
def preprocess(text):
    tokens = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in tokens]
    #Additional Processing
    tokens = additionalProcessing(tokens)
    tokens = [nltk.pos_tag(word) for word in tokens]
    return tokens

'''
file - file that includes the snippets
domain - domain to find job titles for
jobTitles - list to populate job titles with
'''
def processTitles(file, domain, jobTitles):
    f = open(file, 'r')
    text = f.read()
    text = text.replace(("\\n"), "")
    
    tokens = preprocess(text)

    #grammar = """
    #        list: {(<NN|NNS|NNP|VB|VBG|JJ|CC|PRP|IN|TO>+<,>)+}
    #        and: {<NN|NNS|JJ|VB|IN|VBG>*<CC><NN|NNS|JJ|VB|IN|VBG>+}
    #        """
    cp = nltk.RegexpParser(GRAMMAR)
    
    stop = stopwords.words('english')
    additionalStopwords = ADDITIONAL_STOP_WORDS_TITLES
    
    domain = domain.split(" ")
    for word in domain:
        additionalStopwords.append(word)
    
    #Using the grammar we find lists and find potential titles from them
    for sentence in tokens:
        #for text that has a "/" in it. Splits the word into two titles/skills
        multiName = []
        result = cp.parse(sentence)
        
        for node in result:
            #creates a 3 dimensional array. 1st Dimension is the found list forms
            #2nd is individual titles within those lists, and the 3rd is the Part of Speech Tag
            name = []
            name.append([])
            name[0].append([])
            counter = 0
            wordCounter = 0;
            if type(node) is nltk.Tree:
                #results from the list grammar
                if node.label() == 'list':
                    for element in node:
                        if element[1] == ",":
                            counter = counter + 1
                            name.append([])
                            name[counter].append([])
                            wordCounter = 0
                            continue
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append([])
                            name[counter].append([])
                            wordCounter = 0
                            continue
                        else:
                            if element[0].strip() in stop or element[0].strip() in additionalStopwords:
                                name[counter] = []
                                name.append([])
                                name[counter].append([])
                                wordCounter = 0
                                continue
                                
                            elif element[1] == "IN" or element[1] == "NNP" or element[1] == "TO":
                                name[counter][wordCounter] = ["", ""]
                            else:
                                name[counter][wordCounter] = [element[0], element[1]]
                                name[counter].append([])
                                wordCounter += 1
                
                #results from the and grammar
                elif node.label() == 'and':
                    for element in node:
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append([])
                            name[counter].append([])
                            wordCounter = 0
                            continue
                        else:
                            if element[0].strip() in stop or element[0].strip() in additionalStopwords:
                                name[counter] = []
                                name.append([])
                                name[counter].append([])
                                wordCounter = 0
                                continue
                            elif element[1] == "IN" or element[1] == "NNP" or element[1] == "TO":
                                name[counter][wordCounter] = ["", ""]
                            else:
                                name[counter][wordCounter] = [element[0], element[1]]
                                name[counter].append([])
                                wordCounter += 1
            
            #After finding potential job titles we do additional processing
            #and add them to the return list                    
            for n in name:
                jt = ""
                form = [" "]
                for w in n:
                    if  w:
                        if (len(n) == 1 or len(n) == 2) and (w[1] == "JJ" or w[1] or "VB" or w[1] == "NNS"):
                            continue
                        if "/" in w[0]:
                            multiName = w[0].split("/")
                            jt += multiName[0] + " "
                            if not jt.strip() in jobTitles:
                                if w[1] == "VBG" or w[1] == "JJ":
                                    form = [" "]
                                else:
                                    jobTitles.append(jt.strip())
                                    form = [" "]
                                    
                            jt = multiName[1] + " "
                            form.append(w[1])
                        else:
                            jt += w[0] + " "
                            form.append(w[1])
            
                if jt != "" and jt != " ": 
                    if not jt.strip() in jobTitles:
                        if form[len(form)-1] == "NNS" or form[len(form)-1] == "VBG" or form[len(form)-1] == "JJ": 
                            pass
                        else:     
                            jobTitles.append(jt.strip())         
''' END OF processTitles() FUNCTION '''

'''
file - file to get information from
domain - the domain the job title is in
jobSkills - the list to populate job skills with
querys - list of the queries used in finding the snippets
'''
def processSkills(file, domain, jobSkills, querys):
    f = open(file, 'r')
    text = f.read()
    text = text.replace(("\\n"), "")
    
    tokens = nltk.sent_tokenize(text)
    tokens = [nltk.word_tokenize(sentence) for sentence in tokens]
    tokens = [nltk.pos_tag(word) for word in tokens]

    grammar = """
            list: {(<NN|NNS|NNP|VB|VBG|JJ|CC|PRP|IN|TO>+<,>)+}
            and: {<NN|NNS|JJ|VB|IN|VBG>*<CC><NN|NNS|JJ|VB|IN|VBG>+}
            """
    cp = nltk.RegexpParser(grammar)
    
    additionalStopwords = ADDITIONAL_STOP_WORDS_SKILLS
    
    domain = domain.split(" ")
    for word in domain:
        additionalStopwords.append(word)
    for query in querys:
        for word in query.split(" "):
            additionalStopwords.append(word) 
    
    #Using the grammar we find lists and find potential skill from them
    for sentence in tokens:
        #for text that has a "/" in it. Splits the word into two titles/skills
        multiName = []
        result = cp.parse(sentence)
        
        for node in result:
            #creates a 3 dimensional array. 1st Dimension is the found list forms
            #2nd is individual titles within those lists, and the 3rd is the Part of Speech Tag
            name = []
            name.append([])
            name[0].append([])
            counter = 0
            wordCounter = 0;
            if type(node) is nltk.Tree:
                #results from the list grammar
                if node.label() == 'list':
                    for element in node:
                        if element[1] == ",":
                            counter = counter + 1
                            name.append([])
                            name[counter].append([])
                            wordCounter = 0
                            continue
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append([])
                            name[counter].append([])
                            wordCounter = 0
                            continue
                        else:
                            if element[0].strip() in additionalStopwords:
                                name[counter] = []
                                name.append([])
                                name[counter].append([])
                                wordCounter = 0
                                continue
                                
                            elif element[1] == "IN" or element[1] == "TO":
                                name[counter][wordCounter] = ["", ""]
                            else:
                                name[counter][wordCounter] = [element[0], element[1]]
                                name[counter].append([])
                                wordCounter += 1
                
                #results from the and grammar
                elif node.label() == 'and':
                    for element in node:
                        if element[1] == "CC":
                            counter = counter + 1
                            name.append([])
                            name[counter].append([])
                            wordCounter = 0
                            continue
                        else:
                            if element[0].strip() in additionalStopwords:
                                name[counter] = []
                                name.append([])
                                name[counter].append([])
                                wordCounter = 0
                                continue
                            elif element[1] == "IN" or element[1] == "TO":
                                name[counter][wordCounter] = ["", ""]
                            else:
                                name[counter][wordCounter] = [element[0], element[1]]
                                name[counter].append([])
                                wordCounter += 1
            
            #After finding potential job titles we do additional processing
            #and add them to the return list                   
            for n in name:
                jt = ""
                form = [" "]
                for w in n:
                    if  w:
                        if (len(n) == 1 or len(n) == 2) and (w[1] == "JJ" or w[1] == "NNS"):
                            continue
                        if "/" in w[0]:
                            multiName = w[0].split("/")
                            jt += multiName[0] + " "
                            if not jt.strip() in jobSkills:
                                jobSkills.append(jt.strip())
                                form = [" "]
                                    
                            jt = multiName[1] + " "
                            form.append(w[1])
                        else:
                            jt += w[0] + " "
                            form.append(w[1])
            
                if jt != "" and jt != " ": 
                    if not jt.strip() in jobSkills:   
                        jobSkills.append(jt.strip())       
''' END OF processSkills() FUNCTION '''


#nltk.download('all')

'''
jobName - for skills this is job title that we are finding skills for
'''
def googleSkills(jobName):
    if(GET_FULL_SNIPPET):
	file = "google/output/" + GOOGLE_SKILL_SNIPPET_FILENAME + "Full.txt"
    else:
	file = "google/output/" + GOOGLE_SKILL_SNIPPET_FILENAME + ".txt"
    j = Job()
    jobSkills = [""]
    querySkills = ["skills such as", "skills including"]
    processSkills(file, "Information Technology", jobSkills, querySkills)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(jobSkills)
    print len(jobSkills)
    # add to database
    j.getjob("Information Technology", jobName)
    j.skills = jobSkills
    j.save()
        
'''
jobName - for job titles this is the initial job title used for the queries
'''
def googleJobs(jobName):
    if(GET_FULL_SNIPPET):
	file = "google/output/" + GOOGLE_TITLE_SNIPPET_FILENAME + "Full.txt"
    else:
    	file = "google/output/" + GOOGLE_TITLE_SNIPPET_FILENAME + ".txt"
    jobTitles = [jobName]
    processTitles(file, "Information Technology", jobTitles)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(jobTitles)
    print len(jobTitles)
    #add to database
    for jt in jobTitles:
       j = Job()
       j.domain = "Information Technology"
       j.title = jt
       j.save()
    

#run(False, "software engineer", "output/outputNew.txt")
#run(True, "software engineer", "output/softwareengineerSkills.txt")

        
        





