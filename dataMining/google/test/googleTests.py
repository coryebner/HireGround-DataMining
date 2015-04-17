from google.googleProcessing import processTitles
import pprint

def test():
    inputfile = "google/test/test.txt"
    
    expectedJobTitles = ["system analyst",
    "functional consultant",
    "business analyst",
    "programmer",
    "computer scientist",
    "support specialist",
    "network administrator",
    "computer systems administrator",
    "analyst",
    "interface designer",
    "web development",
    "database administrator",
    "database analyst",
    "system analyst",
    "computer consultant",
    "software architect",
    "customer service",
    "University lecturer",
    "defence research scientist",
    "telecommunications engineer",
    "mechanical engineer",
    "electrical engineer",
    "aerospace engineer",
    "civil engineer",
    "DevOps developer",
    "data scientist",
    "application developer",
    "cloud architect",
    "build lead",
    "hardware engineer",
    "Information Systems Manager",
    "social worker",
    "primary school teacher",
    "computer programmer",
    "interaction designer"]
    
    retrievedJobTitles = ["software engineer"]
    
    processTitles(inputfile, "test", retrievedJobTitles)
    
    count = 0
    for title in expectedJobTitles:
        for retrievedTitle in retrievedJobTitles:
            if retrievedTitle == title:
                count = count + 1
                
    for title in expectedJobTitles:
        if not title in retrievedJobTitles:
            print title
            
        
                
                
                
    recall = count/float(len(expectedJobTitles))
    accuracy = count/float(len(retrievedJobTitles))
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(retrievedJobTitles)
    print len(retrievedJobTitles)
    
    
    print "recall is: " + str(recall) + " accuracy is: " + str(accuracy)


