__author__ = "Justin Milanovic"
__version__ = "1.0.0"
__email__ = "justinmilanovic@gmail.com"
__status__ = "Development"

import pymongo

class Job(object):
    
    def __init__(self):
        self._id = None
        self._domain = None
        self._title = None
        self._skills = []
        
        #con = Connection()
        #db = con.testdatabase
        #self.dbconnect = db.jobs        
    
    def save(self):
        if self._id == None:
            self.dbconnect.save({'domain':self._domain, 'title':self._title, 'skills':self._skills})
        else:
            self.dbconnect.save({'_id':self._id, 'domain':self._domain, 'title':self._title, 'skills':self._skills})
            
    def remove(self):
        self.dbconnect.remove({'_id':self._id})
    
            
    def getall(self):    
        return self.dbconnect.find()

    def getdomain(self,domain):    
        return self.dbconnect.find_one({'domain':domain,})
        
    def getjob(self, domain, title):    
        document = self.dbconnect.find_one({'domain':domain, 'title':title})
        if document != None:
            self._id = document['_id']
            self._domain = document['domain']
            self._title = document['title']
            if document['skills'] == '':
                self._skills = []
            else:
                self._skills = document['skills']
        else:
            print(domain + ' ' + title + ' does not exist')

    def printdomain(self, domain):
        item = self.getdomain(domain)
        self.printcursor(item)
            
    def printtitle(self, domain, title):
        item = self.getjob(domain, title)
        self.printcursor(item)
    
    def printall(self):
        objects = self.getall()
        self.printcursor(objects)        
    
    def printcursor(self, items):

        for item in items:
            print("object id: " + str(item['_id']))
            if 'domain' in item:
                print("job domain: " + item['domain'])
            if 'title' in item:
                print("job title: " + item['title'])
            if 'skills' in item:
                print("job skills:")
            
                temp_list = item['skills']
                
                if len(temp_list) != 0:
                    temp_list.sort()
            
                for x in temp_list:
                    print('\t' + x)
            print('-'*40)
        
    @property
    def domain(self):
        return self._domain
    
    @domain.setter
    def domain(self, value):
        self._domain = value
 
    @property
    def title(self):
        return self._domain
    
    @title.setter
    def title(self, value):
        self._title = value
            
    @property
    def skills(self):
        return self._skills
    
    @skills.setter
    def skills(self, value):
        self._skills.append(value)

    def removeskill(self, value):
        self.skills.remove(value)


if __name__ == '__main__':
    pass
    
        