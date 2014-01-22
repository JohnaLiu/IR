"""
Description: Implement the core indexing and retrieval features of a boolean search engine in Python
Requirement: HW1: http://courses.cse.tamu.edu/caverlee/csce670/hw/hw1.html
File name: part1.py
Programmer: Zhijiao Liu (Johna)
Environment: 
Last modified date: 
"""

import os


def getDirList(currentDir):
	currentFile = os.listdir(currentDir)
#	print os.listdir(currentDir)
	for f in currentFile:
		if os.path.isdir(currentDir+"/"+f):
			return currentDir+"/"+f
		elif os.path.isfile(currentDir+"/"+f):
			return currentDir


currentDir = os.getcwd()
#currentFile = os.listdir(currentDir)
for f in os.listdir(currentDir):
	if os.path.isdir(currentDir+"/"+f):
		os.listdir(currentDir)
		currentDir = getDirList(currentDir)

		print currentDir
	elif os.path.isfile(currentDir):
		pass

#print os.chdir(getDirList(currentDir))

#print getDirList(currentDir)