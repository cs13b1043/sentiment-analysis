import os
import re
from osa import *

crawledDir = "epinions_crawling/pros_cons dataset/"
def getCategory(nxtlines, cats):
	category=""
	for catname in cats.keys():
		if catname in nxtlines:
			category = catname
			break
	return category
	
def getRelation(ecf):
	e1 = []
	e2 = []
	features = []
	cw = ""
	
	index = 0;
	for i in range(1, len(ecf)+1):
		if ecf[-i] == "(":
			index = -i
			break
		elif ecf[-i] == ")":
			continue
		else:
			cw = cw + ecf[-i]
	cw = cw[::-1] #reverse the string
	ecf = ecf[:index]
	
	
	lst = re.findall(r'[1-3]_[^1-3_]+', ecf)
	#_2600 no, _47jkdf yes, _dgj87 no
	
	for ele in lst:
		if ele[0:2] == "1_":
			e1 = e1 + [ele[2:]]
		if ele[0:2] == "2_":
			e2 = e2 + [ele[2:]]
		if ele[0:2] == "3_":
			features = features + [ele[2:]]
	
	return (e1, e2, cw, features)

def printPreferredEntities(ecf, rel, catlst, fo):
	e1 = rel[0]
	e2 = rel[1]
	cw = rel[2]
	features = rel[3]
	
	if (not e1 and not e2) or (not cw):
		return
	
	fo.write(str(e1) + " " + str(e2) + " " + str(cw) + " " + str(features) + "\n")
	
	#if feature list is empty check the count of occurence of cw in pros and cons

	if features==[]:
		if preferredEntityF(cw, catlst)==1:
			if e1:
				fo.write("Preferred Entity: " + str(e1)+"\n")
			else:
				fo.write(str(e2) + "is not preferred\n")
		else:
			if e2:
				fo.write("Preferred Entity: " + str(e2)+"\n")
			else:
				fo.write(str(e1) + "is not preferred\n")		


	#for each feature check osa(feature, cw) in pros and cons			
	
	for feature in features:
		
		if preferredEntity(feature, cw, catlst)==1:
			if e1:
				fo.write("Preferred Entity for feature '" + str(feature) + "': " + str(e1)+"\n")
			else:
				fo.write(str(e2) + "is not preferred\n")
		
		else:
			if e2:
				fo.write("Preferred Entity for feature '" + str(feature) + "': " + str(e2)+"\n")
			else:
				fo.write(str(e1) + "is not preferred\n")
	
def preferredEntity(feature, cw, catlst):
	prosFileNames = []
	consFileNames = []
	for cat in catlst:
		prosFileNames = prosFileNames + [crawledDir + cat + "_pros.txt"]
		consFileNames = consFileNames + [crawledDir + cat + "_cons.txt"]
	pos = OSA(cw,feature, prosFileNames) - OSA(cw,feature, consFileNames)
	if pos >= 0:
		return 1
	else:
		return 2

def preferredEntityF(cw, catlst):
	prosFileNames = []
	consFileNames = []
	for cat in catlst:
		prosFileNames = prosFileNames + [crawledDir + cat + "_pros.txt"]
		consFileNames = consFileNames + [crawledDir + cat + "_cons.txt"]
	pos = count(cw, prosFileNames) - count(cw, consFileNames)
	if pos >= 0:
		return 1
	else:
		return 2

"""
	name of all categories from epinions.com
"""
allCatsList = []

fileslst = os.listdir(crawledDir)
for i in fileslst:
	if not i.endswith("meta.txt"):
		allCatsList = allCatsList + [i[:-9]]
	
allCatsList = list(set(allCatsList))
#print allCatsList

inputFile = 'data/labeledSentences.txt'
catmetaFile = 'categories.txt'
outputFile = 'output.txt'
		
"""
	category - category list from epinions.com
"""
fc = open(catmetaFile)
cats = {}
while True:
	line = fc.readline()[:-1]
	if not line:
		break
	num = int(fc.readline())
	lst = []
	for i in range(num):
		lst = lst + [fc.readline()[:-1]]
	cats[line] = lst
	
	fc.readline()
	
"""
	Read input file
"""
f = open(inputFile)
catlst = []
fo = open(outputFile, 'w')
while True:
	line = f.readline()
	if not line:
		break
	
	if line.startswith('**************'):
		nxtline = f.readline()
		
		nxtlines = ""
		while not nxtline.startswith('**************'):
			nxtlines = nxtlines + nxtline
			nxtline = f.readline()
		
		if nxtlines == "":
			continue
		
		category = getCategory(nxtlines, cats)	
		
		# matching category in input with epinions.com category names
		if category == "":
			catlst = allCatsList
		else:
			catlst = cats[category]
		
	if "<cs-1>" in line or "<cs-3>" in line:
		while not ("</cs-1>" in line or "</cs-3>" in line):
			line = f.readline()
		
		ecf = f.readline()[:-1]
		rel = getRelation(ecf)
		
		printPreferredEntities(ecf, rel, catlst, fo)
		fo.write("\n")
		
fo.close()
f.close()
