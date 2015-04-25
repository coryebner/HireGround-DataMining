'''
@author - Eric Kingori
@Discription - this program will extract a full snippet from the link given the original snippet and link
@limitations - This program cannot extract snippets from pdfs, word documents, powerpointslides and etc
@limitations - If the snippet contains majority or all of the information it will return the original snippet
@output - If succesful it will return the entire sentence or lines where the original snippet was found, if
unsuccesful it returns the original snippet
'''
from __future__ import division
import os
import tagScraper
import re
import os.path  
import nltk, re, pprint
from bs4 import BeautifulSoup
from nltk import word_tokenize

#This method parses the snippet and opens the text from the link and returns the raw data

def run(snippet, link, tolerance):
	#parsing Snippet to multiple lines
	print "Parsing snippet.."
	snippet = snippet.replace('\\n', '\n')
	snippet = snippet.replace('\\xb7 ', '\n')
	p=re.compile('(u\'| u")')
	snippet = p.sub("", snippet)	
	snippet = snippet.replace("... ", "\n")
	
	snippetLines = re.split('\n', snippet)

	filename = 'output/scrapedData.txt'
	#for debug and deveolopment
	#print "snippet Lines " 
	#print snippetLines
 
	#opening the link and getting raw data
	print "Accesing website for data..."
	try:	
		docs = [".pdf", "docx", "doc"]
		if link in docs :
			print "Cannot extract from structured documents such a PDFs, DOCx, DOC"
		else:
			read= tagScraper.remote(link, filename, False )
	
			read = read.decode('utf8')
	except Exception, e:
		print ("unable to extract data from website")
		return snippet
	
	return getSentences(read, snippetLines, snippet, tolerance)


#this method takes in the raw data and for every sentence the method compares it with the snippets, if the snippet is contained it returns the full sentence if not it switches to a word by word comparisons 
def getSentences(read,snippetLines, snippet, tolerance):
	try:    
		#getting the sentences		
		print "Looking for full snippet within sentences of the data returned.."
               	found = False;
                sent_detector= nltk.data.load('tokenizers/punkt/english.pickle')
                sentences = sent_detector.tokenize(read.strip())
		#comparing every sentence to snippet
		for sentence in sentences:
				#print sentence
				for line in snippetLines:
					if (len(line)>3):
						if line in sentence:
							print "Found full snippet in sentences"
							found= True
							return sentence
		#if not found switching to word by word comparisons  
		if(found == False):
			print "Unable to detect snippet using sentences switching to word comparisons.."
			i=0
			maxFound=0
			read = re.split("\n", read)
			for line in read:
				#print "------------"
				#print line
				words = re.split(" ", line)
				words_Snippet = re.split(" ", snippetLines[i])
				j=0				
				for word in words_Snippet:
					if word in words:
						j+=1
				
				if (j>5 and len(line)<len(snippet)*tolerance):
					found = True										
					return line
					
		if (found == False):
			# This area can be used to improve the algorithm if need be	
			print "Returning original "		
			return snippet			
											
				 
				
	except Exception, e:
		print (str(e))




snippet = u'Find IT - Software jobs such as software engineer/programmer, functional \nconsultant/business analyst, system analyst and others in Singapore. View all IT\n\xa0...'
link = "http://job-search.jobstreet.com.sg/singapore/browse/computer-software-it-jobs/"
#if running locally uncomment the line below
#run (snippet, link, 2)


