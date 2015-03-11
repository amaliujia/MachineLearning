import sys,os
import math

featureDic = ["Gender", "Age", "Student?", "PreviouslyDeclined?"]


def buildDic(line):
	line = line.rstrip('\n\r')
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

def buildVoteDic(line):
	line = line.rstrip('\n\r')
	kvs = line.split("\t")
	dic = {}
	for kv in kvs:
		t = kv.split(" ")
		if(t[0] != "Risk"):
			dic[t[0]] = t[1]
		
	return dic

def buildConceptSpace(featureDic):
	return [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]

def computeB(key, value):
	index = featureDic.index(key)
	if index == 0:
		if value == "Male":
			return 1
		else:
			return 0
	else:
		if value == "Young" or value == "Yes":
			return int(math.pow(2, index))
		else:
			return 0

def reduce(cs, filepath):
	file = open(filepath, 'r')
	
	for line in file:
		re, dic = buildDic(line)
		index = 0
		for k in dic:
			index += computeB(k, dic[k])	
		if re == "high":
			cs[index] = 0
		else:
			cs[index] = 1

	return cs


def printVersionSpace(cs):
	size = 1;
	for i in cs:
		if i == 0 or i == 1:
			size *= 1
		else:
			size *= 2
	sys.stdout.write(str(size)+ '\n')	

def count(cs):
	c = 0
	for i in cs:
		if i == 2:
			c += 1
	return c
def vote(cs, filepath):
	file = open(filepath, 'r')
	c = count(cs)
	for line in file:
		high = 0
		low = 0
		dic = buildVoteDic(line)
		index = 0
		for k in dic:
			index += computeB(k, dic[k])
		if cs[index] == 2:
			high += int(math.pow(2, c) / 2);
			low += int(math.pow(2, c) / 2);
		elif cs[index] == 0:
			high += int(math.pow(2, c));
		else:
			low += int(math.pow(2, c));
		sys.stdout.write(str(high) + " " + str(low) + '\n')

sys.stdout.write(str(int(math.pow(2, 4))) + '\n')
sys.stdout.write(str(int(math.pow(2, math.pow(2, 4)))) + '\n')


cs = buildConceptSpace(featureDic)
cs = reduce(cs, "4Cat-Train.labeled")
printVersionSpace(cs)
vote(cs, sys.argv[1])
