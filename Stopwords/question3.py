import sys

def readLineFromFile(file):
    line = file.readline()
    line = line.rstrip('\n')
    return line

def processList(words):
    words = line.split(" ")
    words = [word.lower() for word in words]
    words.sort()
    return words

def removeDuplicateFromList(words):
    words = list(set(words))
    words.sort()
    return words

def readStopwordsFromFile(file):
	words = [] 
	for line in file:
		line = line.rstrip('\n') 
		words.append(line)
	return words

def countWords(words):
	dic = {}
	for word in words:
		if not dic.get(word):
			dic[word] = 1
		else:
			dic[word] += 1
	return dic

def removeStopwords(words, stopwords):
	for stopword in stopwords:
		while stopword in words:
			words.remove(stopword)
	return words	

def printlinebyline(words):
	for word in words:
		print word

# read words from file1
file = open(sys.argv[1], 'r')
line = readLineFromFile(file)
words = line.split(" ")

# transfer every word into lower case
words = processList(words)

# read stopwords from file2
stopwordsFile = open(sys.argv[2], 'r')
stopwords = readStopwordsFromFile(stopwordsFile)

# remove stopwords
words = removeStopwords(words, stopwords)

#count words
words.sort() 
dic = countWords(words)
result = ""
words = removeDuplicateFromList(words)

for word in words:
    result += word + ":" + str(dic.get(word)) + ","

result = result.rstrip(',')
sys.stdout.write(result)
