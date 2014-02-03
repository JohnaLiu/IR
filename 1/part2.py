"""
Description: Implement the core indexing and retrieval features of
a boolean search engine in Python
Requirement: HW1: http://courses.cse.tamu.edu/caverlee/csce670/hw/hw1.html
File name: part1.py
Programmer: Zhijiao Liu (Johna) 
Environment: 
Last modified date:
"""

from __future__ import division
import os, io, re, sys, math, operator


docID = {}
N = 0  #total number of scanned files

def scanFolder(rootDir): 
    list_dirs = os.walk(rootDir) 
    
    global N 
    count = 1
    for root, dirs, files in list_dirs: 
#        for d in dirs: 
#            print os.path.join(root, d) 
        garbage = ":;(){}[]!$%*&=?,.+-\\\/\"\"'"      
        for f in files:            
            a, b = os.path.splitext(f)
            if b == ".txt":
                N = N + 1
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
 
    if len(result) == 0:
        print "Sorry, no match."
    return result

def tfidf(qTerm,result):
    tfidf = {}
#   print result
    for i in range(len(qTerm)):
        tf = {}
        df = len(result)
        for f in result:         
            tf.update({f:docID[f].get(qTerm[i])})
            tfidf.update({qTerm[i]: [0,tf]})
        tfidf.update({qTerm[i]: [df,tf]})
    print tfidf
    score = {}
    for t in qTerm:

        idf = math.log10(N/df)
        print "N,df",N,df,idf
        for d in result:
            Wtf = 1.0 + math.log10(tfidf[t][1].get(d))
            s = Wtf * idf
            print Wtf,idf
            score.update({d:s})
 #   print score
    sorted_score = sorted(score.iteritems(), key=operator.itemgetter(1), reverse=True)
    print sorted_score




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
    satisfiedDoc = searchFile(qTerm)
    tfidf(qTerm,satisfiedDoc)
