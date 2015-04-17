import sys, os
from logsum import log_sum
import math

def createPrior(Prior):
    f = file(Prior, 'r')
    p = {}
    for line in f:
        line = line.strip()
        a = line.split(" ")
        p[a[0]] = float(a[1])
    return p

def createDev(dev):
    f = file(dev, 'r')
    sentences = []
    for line in f:
        sentences.append(line.strip())
    return sentences

def createTrans(trans):
    f = file(trans, 'r')
    Trans ={}
    labels = []
    for line in f:
        c = line.strip();
        sp = c.split(" ")
        tmp = {}
        label = sp[0]
        for i in range(1, len(sp)):
            a = sp[i].split(":")
            tmp[a[0]] = float(a[1])
        Trans[label] = tmp
        labels.append(label)
    return Trans, labels

def createEmit(emits):
    f = file(emits, 'r')
    Trans ={}
    for line in f:
        c = line.strip();
        sp = c.split(" ")
        tmp = {}
        label = sp[0]
        for i in range(1, len(sp)):
            a = sp[i].split(":")
            tmp[a[0]] = float(a[1])
        Trans[label] = tmp
    return Trans

def createMatrix(emits={}, prior={}, labels=[], os=[]):
    x = []
    l = len(os)
    for i in xrange(0, len(prior)):
        x.append([-1] * l)
    for i in xrange(0, len(prior)):
        x[i][len(os) - 1] = 1
    return x

def backward_recursive(os, i, j, trans={}, emits={}, prior={}, labels=[], matrix=None):
    tmp = 0
    if matrix[0][j+1] == -1:
        matrix[0][j+1] = backward_recursive(os, 0, j+1, trans, emits, prior, labels, matrix)
    tmp = matrix[0][j+1]
    tmp += math.log(emits[labels[0]][os[j+1]])
    tmp += math.log(trans[labels[i]][labels[0]])

    for z in xrange(1, len(labels)):
        if matrix[z][j+1] == -1:
            matrix[z][j+1] = backward_recursive(os, z, j+1, trans, emits, prior, labels, matrix)
        tmp2 = matrix[z][j+1]
        tmp2 += math.log(emits[labels[z]][os[j+1]])
        tmp2 += math.log(trans[labels[i]][labels[z]])

        tmp = log_sum(tmp, tmp2)

    matrix[i][j] = tmp
    return matrix[i][j]

def backward(sentence="", trans=None, emits=None, prior=None, labels=[]):
    os = sentence.split(" ")
    matrix = createMatrix(emits, prior, labels, os)
    for i in xrange(0, len(labels)):
        if(matrix[i][0] == -1):
            matrix[i][0] = backward_recursive(os, i, 0, trans, emits, prior, labels, matrix)
        # if matrix[i][0] == -1:
        #     tmp = math.log(prior[labels[i]])
        #     tmp += math.log(emits[labels[i]][os[0]])
        #     for j in xrange(0, len(labels)):
        #         if matrix[j][1] == -1:
        #             matrix[i][1] = backward_recursive(os, i, 1, trans, emits, prior, labels, matrix)
        #         tmp += matrix[i][1]
        #     matrix[i][0] = tmp


    result = matrix[0][0]
    result += math.log(prior[labels[0]])
    result += math.log(emits[labels[0]][os[0]])
    for z in xrange(1, len(labels)):
        tmp = matrix[z][0]
        tmp += math.log(prior[labels[z]])
        tmp += math.log(emits[labels[z]][os[0]])
        result = log_sum(result, tmp)
    result += -1.0
    sys.stdout.write(str(result) + "\n")



def main():
    dev_file = sys.argv[1]
    trans_file = sys.argv[2]
    emits_file = sys.argv[3]
    prior_file = sys.argv[4]
    sentences = createDev(dev_file)
    trans, labels = createTrans(trans_file)
    emits = createEmit(emits_file)
    prior = createPrior(prior_file)
    for i in xrange(0, len(sentences)):
        backward(sentences[i], trans, emits, prior, labels)


main()