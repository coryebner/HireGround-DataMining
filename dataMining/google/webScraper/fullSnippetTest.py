'''
@author - Eric Kingori
@Description - this program will test the ability of full snippet to extract information from the given links
@output - The results are displayed onto the command line
@Date - Last Revised Apr. 24 2015
'''
from __future__ import division
import fullSnippet
import google.query



'''
 #for development used to iscolate links 
j=13
print "opening this link "+ (links[j])[6:]
print "Searching for this snippet:- "+ (snippets[j])[6:]		
snippet_full=fullSnippet.run((snippets [j])[9:], (links[j])[6:], 3)
'''
def snippetTest():
	#opening the link and snippets	
	linkFile = "google/output/outputNewlinks.txt"

	f = open(linkFile)
	links = f.readlines()
	f.close()

	snippetFile = "google/output/outputNew.txt"

	f = open(snippetFile)
	snippets = f.readlines()
	f.close()
	#Begining the test
	i = 0
	fail = 0
	writeFile ="google/webScraper/output/outputNewFull.txt"
	f = open(writeFile, 'w')
	while (i<len(links)-1):
		print "----------------------------------------"
		print "link id = "+str(i)
		print "Opening this link "+ (links[i])[6:]
		print "Searching for this snippet:- "+ (snippets[i])[6:]
		
		snippet_full=fullSnippet.run((snippets [i])[9:], (links[i])[6:], 3)
		docs = [".pdf", "docx", "doc"]
		if (links[i])[6:] in docs :
			fail = fail-1		
		if (len(snippet_full)> len((snippets [i])[9:])):
			print "Found the snippet "+ ((snippets [i])[9:]) + " within: "+snippet_full
		else:
			print "Unable to find Full Snippet ***"
			fail +=1
		
		snippet_full = snippet_full.replace('\\n', ' ')
		snippet_full = snippet_full.replace('\n', ' ')
		try:
			f.write("Snippet: "+ snippet_full)	
		except UnicodeEncodeError: 
			f.write("Snippet: "+ (snippets [i])[9:]+"\n")
		i +=1
	print "-------------------------"
	print "Statistics: \nAttempts ="+ str(i) + "\nFails =" + str(fail)
	ratio= float(fail/i)
	print "The percentage of failed attempts = "+ "{:.0%}".format(ratio)
	print "The percentage of successful attempts = "+ "{:.0%}".format(float(1 - ratio))
#snippetTest()

