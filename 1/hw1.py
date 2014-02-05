"""
Description: Implement the core indexing and retrieval features of a boolean search engine in Python
Requirement: HW1: http://courses.cse.tamu.edu/caverlee/csce670/hw/hw1.html
File name: hw1.py
Programmer: Zhijiao Liu (Johna) 
Environment: Python 2.7.5, Mac OS 10.9.1
Last modified date: 02/04/2014
"""

from __future__ import division
import os, io, re, sys, math, operator, time, sets


docTermDic = {}
termDic = {}
tfidfVector = {}
docList = []
N = 0  #total number of scanned files
T = 0  #total number of scanned terms
S = 0.0 #for getting the indexing time

def scanFolder(rootDir): 
    t1 = time.time()
    list_dirs = os.walk(rootDir)
    
    global N, T, S

    for root, dirs, files in list_dirs: 
        garbage = ":;(){}[]!$%*&=?,.+'/\\" 

        for f in files:            
            a, b = os.path.splitext(f)
            if b == ".txt":
                N = N + 1
                docTerm = {}
                txt = open(os.path.join(root, f), "r").readlines() 
                termInDoc = {}
                for line in txt:
                        l = re.split(" |'",line) 

                        for term in l:
                                term = term.strip()
                                term = term.lower()
                                for i in range(0, len(garbage)):
                                    term = term.replace(garbage[i],'')
                                if not termDic.has_key(term):
                                    termDic.update({term: {a: 1}})
                                elif termDic.has_key(term):
                                    if not termDic[term].has_key(a):
                                        termDic[term].update({a: 1})
                                    elif termDic[term].has_key(a):
                                        termDic[term][a]+=1    
                                if not docTerm.has_key(term):
                                            docTerm.update({term: 1})
                                elif docTerm.has_key(term):
                                            docTerm[term]+=1

                del termDic['']
                del docTerm['']
                docList.append(a)

                for t in docTerm.keys():
                    docTerm[t] = 1.0 + math.log10(docTerm[t])     #calculate the weight of tf: w = 1+log10(tf)
                docTermDic.update({a: docTerm})
    tfidf()
    t2 = time.time()
    S = t2 - t1
    T = len(termDic)

    

def searchFileForPart1(qTerm):
    query = qTerm
    if termDic.has_key(qTerm[0]):
        result = set(termDic[qTerm[0]])
        result = reduce(set.intersection, (termDic[t].keys() for t in qTerm), result)
        if len(result) != 0:
            print "Total # of result: ", len(result)
            c = 1
            for r in result:
                if c <= 50:
                    print c,": ",r
                    c+=1
        else:
            print "Sorry, no match."
    else:
        print "Sorry, no match."

def searchFileForPart2(qTerm):
    count = 0
    result = []
    for t in qTerm:
        if termDic.has_key(t):
            for d in termDic[t].keys():
                if d not in result:
                    result.append(d)
    if len(result) == 0:
        print "Sorry, no match."
    print "Total # of result: ", len(result)
    return result


def tfidf():
    dfDic = {}
    for doc in docTermDic.keys():
        tfidf = {}
        for t in docTermDic[doc].keys():
            idf = math.log10(N/len(termDic[t]))           #get idf: log10(N/df)
            tfidf.update({t:docTermDic[doc][t]*idf})
        tfidfVector.update({doc: tfidf})   
 

def cosineSim(qTerm,result):
    docVector = tfidfVector
    queryVector = {}
    qV = {}
    for term in qTerm:       
        for doc in result:
            if termDic.has_key(term):
                if termDic[term].has_key(doc):
                    qV.update({term: termDic[term][doc]})               
            queryVector.update({doc: qV})

    docCosineSim = {}
    
    for doc in result:
        lDoc = 0.0
        lQuery = 0.0
        for key in docVector[doc].keys():
            lDoc = math.pow(docVector[doc][key],2) + lDoc
        absDocV = math.sqrt(lDoc)
        for key in queryVector[doc].keys():
            lQuery = math.pow(queryVector[doc][key],2) + lQuery
        absQueryV = math.sqrt(lQuery)

        dotMulti = 0.0

        for key in qTerm:
            if not docVector[doc].has_key(key):
                dotMulti = 0.0 + dotMulti           
            else:
                dotMulti = queryVector[doc][key]*docVector[doc][key] + dotMulti 

        if dotMulti == 0.0:
            cosSim = 0.0
        else:
            cosSim = dotMulti/(absDocV*absQueryV)    #calculate cosine similarity

        docCosineSim.update({doc:cosSim})
    sorted_docCosineSim = sorted(docCosineSim.iteritems(), key=operator.itemgetter(1),reverse=True)

    if len(sorted_docCosineSim) != 0:
        if len(sorted_docCosineSim) <= 50:
            for d in len(sorted_docCosineSim):
                print d+1,": ",sorted_docCosineSim[d]
        else:
            for d in range(50):
                print d+1,": ",sorted_docCosineSim[d]





currentDir = os.getcwd()
scanFolder(currentDir)
print "Finish indexing!"
print "You have ",N," files and ",T," terms. Use ",S," seconds."
print "=========================================="
print "1. Part 1: Boolean Retrieval"
print "2. Part 2: Vector Space Retrieval"
print "Use .. to go back to the selection manu."
print "=========================================="
while True:
    selection = raw_input("Your selection of the functions: ")
    if selection == '1':
        while True:
            query = raw_input("Please input your query: ")
            qTerm = query.split(' ')
            for q in range(len(qTerm)):
                qTerm[q] = qTerm[q].strip()
                qTerm[q] = qTerm[q].lower()
            breakP = 0
            for t in qTerm:
                if t == "..":
                    breakP = 1
                if t == "exit":
                    print "Thanks for using this program."
                    sys.exit(0)
            if breakP == 1:
                break
            else:
                searchFileForPart1(qTerm)
    elif selection == '2':
        while True:
            query = raw_input("Please input your query: ")
            qTerm = query.split(' ')
            for q in range(len(qTerm)):
                qTerm[q] = qTerm[q].strip()
                qTerm[q] = qTerm[q].lower()
            breakP = 0
            for t in qTerm:
                if t == "..":
                    breakP = 1
                if t == "exit":
                    print "Thanks for using this program."
                    sys.exit(0)
            if breakP == 1:
                break
            else:
                satisfiedDoc = searchFileForPart2(qTerm)
                if len(satisfiedDoc) != 0:
                    cosineSim(qTerm,satisfiedDoc)
    else:
        print "Wrong number. Please select again."


