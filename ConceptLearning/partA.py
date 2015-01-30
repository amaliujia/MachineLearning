import os,sys
import math

features = ["Gender", "Age", "Student?", "PreviouslyDeclined?", "HairLength", "Employed?", "TypeOfColateral", "FirstLoan", "LifeInsurance"]

def parseFile(filename):
	file = open(filename, 'r')
	return file

def computeInputSpace(file):
	line = file.readline()
	line = line.rstrip('\n\r')
	words = line.split("\t")
	file.close()
	return int(math.pow(2, len(words) - 1)), len(words) - 1 

def computeConceptSpace(size):
	return int(math.pow(2, size)) 

def computeHypothesisSpace(size):
	return int(math.pow(3, size))

def updateHyphothesis(line, h):
	kvs = line.split("\t")
	dic = {}
	re = True 
	for kv in kvs:
		t = kv.split(" ")
		if(t[0] != "Risk"):
			dic[t[0]] = t[1]
		else:
			re = t[1]
	
	if re == "low" :
		return h

	for key in h:
		if h[key] == "null" :
			h[key] = dic[key]
		elif h[key] == "?" :
			break
		elif h[key] != dic[key] :
			h[key] = "?"

	return h

def printH(h):
	with open("partA4.txt",  "a") as f:
		count = 0
		for key in features:
			if count != 0 :
				f.write("\t")
			f.write(h[key])
			count += 1
		f.write("\n")

def ifMiss(dic, re, h):
	for f in features:
		if h[f] == "?":
			continue
		elif h[f] == dic[f]:
			continue
		else:
			return not re
	return re 

def buildDic(line):
	kvs = line.split("\t")
	dic = {}
	re = True 
	for kv in kvs:
		t = kv.split(" ")
		if(t[0] != "Risk"):
			dic[t[0]] = t[1]
		else:
			re = t[1]
	return re, dic

def missRate(file, h):
	total = 0.0
	miss = 0.0
	for line in file :
		re, dic = buildDic(line)
		if ifMiss(dic, re, h):
			miss += 1
		total += 1
	return miss / total

def findS(file):
	h = {"Gender" : "null", "Age" : "null", "Student?" : "null", "PreviouslyDeclined?" : "null", "HairLength" : "null" , "Employed?" : "null", "TypeOfColateral" : "null", "FirstLoan" : "null", "LifeInsurance" : "null"}
	count = 0	
	for line in file:
		line = line.rstrip('\n\r')
		h = updateHyphothesis(line, h)	
		if count % 30 == 0 and count != 0:
			printH(h)
		count += 1
	file.close()
	return h

def ifRisky(dic, h):
    for f in features:
        if h[f] == "?":
            continue
        elif h[f] == dic[f]:
            continue
        else:
            return False
    return True

def printToStd(result):
	sys.stdout.write(result + '\n')

def test(file, h):
	for line in file:
		re, dic = buildDic(line)
		if ifRisky(dic, h):
			printToStd("high")
		else:
			printToStd("low")	
	file.close()

file = parseFile("9Cat-Train.labeled")
size, wordslen = computeInputSpace(file)
sizeC = computeConceptSpace(size)
sizeH = computeHypothesisSpace(wordslen)
sys.stdout.write(str(size) + '\n')
sys.stdout.write(str(len(str(sizeC))) + '\n')
sys.stdout.write(str(sizeH) + '\n')
h = findS(parseFile("9Cat-Train.labeled"))
rate = missRate(parseFile("9Cat-Dev.labeled"), h)
sys.stdout.write(str(rate) + '\n')
#test(parseFile(sys.argv[1]), h)
