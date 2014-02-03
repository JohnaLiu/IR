"""
Description: Implement the core indexing and retrieval features of
a boolean search engine in Python
Requirement: HW1: http://courses.cse.tamu.edu/caverlee/csce670/hw/hw1.html
File name: part1.py
Programmer: Zhijiao Liu (Johna) 
Environment: 
Last modified date:
"""


import os, io, re, sys

docID = {}

def scanFolder(rootDir): 
    list_dirs = os.walk(rootDir) 
    

    count = 1
    for root, dirs, files in list_dirs: 
#        for d in dirs: 
#            print os.path.join(root, d) 
        garbage = ":;(){}[]!$%*&=?,.+-\\\/\"\"'"      
        for f in files:            
            a, b = os.path.splitext(f)
            if b == ".txt":
                docList = {}
                txt = open(os.path.join(root, f), "r").readlines() 
                for line in txt:
                        l = re.split(" ",line) 

                        for term in l:
                                term = term.strip()
                                term = term.lower()
                                for i in range(0, len(garbage)):
                                    term = term.replace(garbage[i],'')
#                                if term != '' or term != ':' or term != ',' or term != '.' or term != '\n' or term != '\r':
                                if not docList.has_key(term):
                                            docList.update({term: 1})
                                elif docList.has_key(term):
                                            docList[term]+=1
                del docList['']
                count+=1
                docID.update({a: docList})
    print docID.viewkeys()
#    print docID

def searchFile(qTerm):
    count = 0
    result = []
#    for i in range(len(qTerm)):
    for f in docID:
        if docID[f].has_key(qTerm[0]):
            if f not in result:
                result.append(f)
            count+=1

    print "first",result
        
    for t in range(1,len(qTerm)):
        for f in result:
            if docID[f].has_key(qTerm[t]):
                if f not in result:
                    result.remove(f)
            else:
                result.remove(f)
            count+=1

    print result
 
    if len(result) == 0:
        print "Sorry, no match."




currentDir = os.getcwd()
scanFolder(currentDir)
#print docID['a9900013']
print "Finish indexing!"
#print "Please input your query: "
while True:
    query = raw_input("Please input your query: ")
    qTerm = query.split(' ')
    for q in range(len(qTerm)):
        qTerm[q] = qTerm[q].lower()


#    print qTerm
    for t in qTerm:
#        print t
        if t == "exit":
            print "88"
            sys.exit(0)
    print qTerm
    searchFile(qTerm)
