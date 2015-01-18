import sys

def readLineFromFile(file):
    line = file.readline()
    line = line.rstrip('\n')
    return line

def processList(words):
	words = line.split(" ")
	words = [word.lower() for word in words]
	words = list(set(words))
	words.sort()
	return words

file = open(sys.argv[1], 'r')
line = readLineFromFile(file) 
words = line.split(" ")
words = processList(words)
result = ",".join(words)
sys.stdout.write(result)
	
