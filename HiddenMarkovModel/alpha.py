import sys, os
from logsum import log_sum
import math

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
    #l = len(emits[labels[0]])
    l = len(os)
    # x axis is state
    # y axis is observation
    for i in xrange(0, len(prior)):
        x.append([-1] * l)
    return x


def forward_recursive(os, i, j, trans={}, emits={}, prior={}, labels=[], matrix=None):
    if matrix[i][j] == -1:
        if j == 0:
            matrix[i][j] = math.log(prior[labels[i]]) + math.log(emits[labels[i]][os[j]])
        else:
            tmp = math.log(emits[labels[i]][os[j]])
            tmp2 = 0
            if matrix[0][j-1] != -1:
                tmp2 = matrix[0][j-1]
            else:
                tmp2 = forward_recursive(os, 0, j-1, trans, emits, prior, labels, matrix)

            tmp2 += math.log(trans[labels[0]][labels[i]])

            for t in xrange(1, len(prior)):
                if matrix[t][j-1] != -1:
                    tmp2 = log_sum(tmp2, matrix[t][j-1] + math.log(trans[labels[t]][labels[i]]))
                else:
                    matrix[t][j-1] = forward_recursive(os, t, j-1, trans, emits, prior, labels, matrix)
                    tmp2 = log_sum(tmp2, matrix[t][j-1] + math.log(trans[labels[t]][labels[i]]))

            tmp += tmp2
            matrix[i][j] = tmp
    return matrix[i][j]

def forward(sentence="", trans=None, emits=None, prior=None, labels=[]):
    os = sentence.split(" ");
    matrix = createMatrix(emits, prior, labels, os)
    t = len(os)
    for i in xrange(0, len(prior)):
        if matrix[i][t-1] == -1:
            matrix[i][t-1] = forward_recursive(os, i, t-1, trans, emits, prior, labels, matrix)

    tmp = matrix[0][t-1]
    for i in xrange(1, len(prior)):
        tmp = log_sum(tmp, matrix[i][t-1])
    sys.stdout.write(str(tmp) + "\n")

def createPrior(Prior):
    f = file(Prior, 'r')
    p = {}
    for line in f:
        line = line.strip()
        a = line.split(" ")
        p[a[0]] = float(a[1])
    return p

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
        forward(sentences[i], trans, emits, prior, labels)

main()