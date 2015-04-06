'''
Created on Oct 23, 2014

@author: Cory
@author: Matt
'''

import pprint
import nltk
from nltk.corpus import stopwords

def processTitles(file, domain, jobTitles):
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
    
    stop = stopwords.words('english')
    additionalStopwords = ["list", "others", "benefits", "after", "uses", "use",
                           "jobs", "job", "professionals", "professionals" "occupations", "including",
                           "like", "such", "as", "interview", "various", "salary", "experience",
                           "facts", "enjoy", "industry", "professions", "number", "high-paying"]
    
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
    
    additionalStopwords = ["list", "others", "benefits", "after", "uses", "use",
                           "jobs", "job", "professionals", "professionals" "occupations", "including",
                           "like", "such", "as", "interview", "various", "salary", "experience",
                           "facts", "enjoy", "industry", "professions", "number", "high-paying",
                           "skill", "skills", "get", "help"]
    
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

def run(doSkills):
    querySkills = ["skills such as", "skills including"]
    jobTitles = ["software engineer"]
    jobSkills = [""]
    
    #processTitles("output/outputNew.txt", "Information Technology", jobTitles)
    processSkills("output/softwareengineerSkills.txt", "Information Technology", jobSkills, querySkills)
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(jobSkills)
    print len(jobSkills)


run(False)

        
        





