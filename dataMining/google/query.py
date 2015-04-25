from apiclient.discovery import build
from webScraper import fullSnippet
import re
from settings import GOOGLE_API_KEYS
from googleapiclient.errors import HttpError


def getSnippets(response, output, links, getFullSnippet):

    #iterate through the keys in the query response (dictionary)
    snippetCounter = 0
    linkCounter = 0
    for key in response.keys():
        #items key holds the link information
        if key == "items":
            #iterate over the items dictionary
            for itemValue in response[key]:
                #iterate over the keys in that dictionary
                for itemKey in itemValue.keys():
                    #print snippet
                    if itemKey == "snippet":
			if(getFullSnippet == False):
		                output.write("Snippet: ")
		                output.write(repr(itemValue[itemKey]))
		                output.write("\n")
			else:
				snippet = repr(itemValue[itemKey])
                        snippetCounter += 1 #counter for snippets founds
                    #print if it is a link
                    elif itemKey == "link":
			linkCounter +=1 #counter for links returned		        
			links.write("Link: ")
		        links.write(itemValue[itemKey])
		        links.write("\n")
			#if get fullSnippet is activated and the link counter mathches the Snippet counter
			if(getFullSnippet == True and linkCounter == snippetCounter):
				snippet_full = fullSnippet.run(snippet, itemValue[itemKey], 2)
				output.write("Snippet: ")
		                try:
					
					#parsing the snippet to try an remove as much niose initially as posible
					snippetArray= snippet_full.split()
					snippet_full = ' '.join(snippetArray)					
					regex = re.compile('[^a-zA-Z\s,\']')
					snippet_full=regex.sub('.', snippet_full)
					snippet_full=re.sub('\.\.+', '.', snippet_full)
					#writing new snippet					
					snippet_full=repr(snippet_full)
					output.write(snippet_full)	
				except (UnicodeEncodeError, AttributeError) as e:
					#write oriinal Snippet upon error
		                	output.write(repr(snippet))
				output.write("\n")
			
				
    print("Amount of responses " + str(snippetCounter))
    
''' END OF getSnippets() FUNCTION '''
    
def runTitles(initialTitle, outputFile, getFullSnippet):
    #api_key = "AIzaSyCHwlWEjEcdeH1KRnmIi9fq5Dnx2JBeVRw"
    search_Engine_ID = "016745198537660285174:espiwqmbexg"
    
    #domain = "Information Technology"
    jobSynonym = ["jobs", "occupations", "professions"]
    form = ["such as", "including", "like"]
    
    #counter = 0;
    query = "\"* Jobs such as Software Engineer\""
    
    blacklist = ["\"* Information Technology occupations including\"", "\"* Information Technology occupations like\"",
                 "\"* Information Technology professions such as\"", "\"* Information Technology professions including\"",
                 "\"* Information Technology professions like\""]
    
    blacklist2 = [("occupations", "including"), ("occupations", "like"), ("professions", "including"), ("professions", "like")]
     #this activates the full Snippet Capability
    if(getFullSnippet ==  True):
        output = open(("google/output/" + outputFile + "Full.txt"), 'w+')    
    else:
	 output = open(("google/output/" + outputFile + ".txt"), 'w+')

    links = open(("google/output/" + outputFile + "links.txt"), 'w+')
    
    currentAPIKey = 0;
    
   
    
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEYS[currentAPIKey])
        
    for js in jobSynonym:
        for fm in form:
            badQuery = False
            for bl in blacklist2:
                if js == bl[0] and fm == bl[1]:
                    badQuery = True
                    
            if badQuery:
                continue
                    
            query = "\"* " + js + " " + fm + " " + initialTitle +"\""
                    
            if query in blacklist:
                continue
                    
            print "Query is: " + query
            
            try:
                response = service.cse().list(q = query, cx = search_Engine_ID).execute()
                getSnippets(response, output, links, getFullSnippet)
                #pprint.pprint(response, output)
            except HttpError, HttpErrorArg:
                argString = str(HttpErrorArg)
                location = argString.find("returned \"Daily Limit Exceeded\"")
                
                if location != -1:
                    print "Daily Limit of queries exceeded, switching API key"
                    currentAPIKey += 1
                
                    if currentAPIKey >= len(GOOGLE_API_KEYS):
                        print "No Usable API keys remaining"
                        print "Exiting..."
                        exit()
                    else:
                        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEYS[currentAPIKey])
    
                else:
                    print HttpErrorArg
                    print "Exiting..."
                    exit()
                       
          

def runSkills(initialTitle, searchTitle, outputFile, getFullSnippet):    
    #api_key = "AIzaSyCHwlWEjEcdeH1KRnmIi9fq5Dnx2JBeVRw"
    search_Engine_ID = "016745198537660285174:espiwqmbexg"
    
    #domain = "Information Technology"
    form = ["such as", "including", "like"]
    
    currentAPIKey = 0;
    
    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEYS[currentAPIKey])
    if(getFullSnippet):
	output = open(("google/output/" + outputFile + "Full.txt"), 'w+')
    else: 
	output = open(("google/output/" + outputFile + ".txt"), 'w+')
    links = open(("google/output/" + outputFile + "links.txt"), 'w+')
        
    for fm in form:
        if fm == "like":
            continue
            
        query = "\"" + searchTitle + " skills " + fm + "\"" 
            
        print "Query is: " + query
            
            
        try:
            response = service.cse().list(q = query, cx = search_Engine_ID).execute()
            getSnippets(response, output, links, getFullSnippet)
            #pprint.pprint(response, output)
        except HttpError, HttpErrorArg:
            argString = str(HttpErrorArg)
            location = argString.find("returned \"Daily Limit Exceeded\"")
                
            if location != -1:
                print "Daily Limit of queries exceeded, switching API key"
                currentAPIKey += 1
                
                if currentAPIKey >= len(GOOGLE_API_KEYS):
                    print "No Usable API keys remaining"
                    print "Exiting..."
                    exit()
                else:
                    service = build("customsearch", "v1", developerKey=GOOGLE_API_KEYS[currentAPIKey])
    
            else:
                print HttpErrorArg
                print "Exiting..."
                exit()
        
#runTitles("software engineer", "testOutput")
#runSkills("software engineer", "software engineering", "testSkills")
