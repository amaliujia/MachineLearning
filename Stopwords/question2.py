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
	words =	list(set(words))
	words.sort()
	return words


file = open(sys.argv[1], 'r')
line = readLineFromFile(file)
words = line.split(" ")
words = processList(words)
dic = {};

for word in words:
	if not dic.get(word):
		dic[word] = 1
	else:
		dic[word] += 1

result = ""
words = removeDuplicateFromList(words)

for word in words:
	result += word + ":" + str(dic.get(word)) + ","
	
result = result.rstrip(',')
sys.stdout.write(result)
