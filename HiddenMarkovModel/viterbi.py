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
    l = len(os)
    for i in xrange(0, len(prior)):
        x.append([-1] * l)
    for i in xrange(0, len(prior)):
        x[i][0] = math.log(prior[labels[i]]) + math.log(emits[labels[i]][os[0]])
    return x

def createPath(emits={}, prior={}, labels=[], os=[]):
    x = []
    l = len(os)
    for i in xrange(0, len(prior)):
        x.append([-1] * l)
    for i in xrange(0, len(prior)):
        x[i][0] = -1
    return x



def createPrior(Prior):
    f = file(Prior, 'r')
    p = {}
    for line in f:
        line = line.strip()
        a = line.split(" ")
        p[a[0]] = float(a[1])
    return p

def Viterbi(sentence="", trans=None, emits=None, prior=None, labels=None):
    os = sentence.split(" ");
    matrix = createMatrix(emits, prior, labels, os)
    result = []
    pre = 0
    for i in xrange(0, len(os)):
        if i == 0:
            m = -1
            maxV = -float("inf")
            for j in xrange(0, len(prior)):
                matrix[j][i] = math.log(prior[labels[j]]) + math.log(emits[labels[j]][os[i]])
                if matrix[j][i] > maxV:
                    maxV =  matrix[j][i]
                    m = j
            result.append(labels[m])
            pre = maxV
        else:
            m = -1
            maxV = -float("inf")
            for j in xrange(0, len(prior)):
                tmp = math.log(trans[labels[j-1]][labels[j]])
                tmp += math.log(emits[labels[j]][os[i]]);
                tmp += pre
                matrix[j][i] = tmp
                if matrix[j][i] > maxV:
                    maxV = matrix[j][i]
                    m = j
            result.append(labels[m])
            pre = maxV
                # maxVM = -float("inf")
                # for z in xrange(0, len(prior)):
                #     tmp = matrix[z][i-1]
                #     tmp += math.log(trans[labels[z]][labels[j]])
                #     tmp += math.log(emits[labels[j]][os[i]]);
                #     if maxVM < tmp:
                #         maxVM = tmp
                # matrix[j][i] = maxVM
                # if matrix[j][i] > maxV:
                #     maxV = matrix[j][i]
                #     m = j

    #return result
    #sys.stdout.write(result)
    for o, r in zip(os, result):
        sys.stdout.write(o + "_" + r + " ")
    sys.stdout.write("\n")

def Viterbi_2(sentence="", trans=None, emits=None, prior=None, labels=None):
    os = sentence.split(" ")
    matrix = createMatrix(emits, prior, labels, os)
    pathMatrix = createPath(emits, prior, labels, os)

    final = -1
    for i in xrange(1, len(os)):
        for j in xrange(0, len(prior)):
            m = -1
            maxV = float("-inf")
            tmp = math.log(emits[labels[j]][os[i]]);
            for z in xrange(0, len(prior)):
                c = math.log(trans[labels[z]][labels[j]])
                if (tmp + c + matrix[z][i-1]) > maxV :
                        m = z
                        maxV = tmp + c + matrix[z][i-1]
            matrix[j][i] = maxV
            pathMatrix[j][i] = m

    if i == (len(os) - 1) :
        maxV = float("-inf")
        for j in xrange(0, len(prior)):
            if matrix[j][len(os) - 1] > maxV:
                maxV = matrix[j][len(os) - 1]
                final = j


    result = []
    for i in range(0, len(os)):
        result = [labels[final]] + result
        #j = len(os) - i - 1
        j = len(os) - i - 1
        final = pathMatrix[final][j]

    #return result
    pp = ""
    for o, r in zip(os, result):
        pp += o + "_" + r + " "
        #sys.stdout.write(o + "_" + r + " ")
    pp = pp[:-1]
    sys.stdout.write(pp)
    sys.stdout.write("\n")


def main():
    dev_file = sys.argv[1]
    trans_file = sys.argv[2]
    emits_file = sys.argv[3]
    prior_file = sys.argv[4]
    sentences = createDev(dev_file)
    trans, labels = createTrans(trans_file)
    emits = createEmit(emits_file)
    prior = createPrior(prior_file)
    f = open('output.txt', 'w')
    for i in xrange(0, len(sentences)):
         Viterbi_2(sentences[i], trans, emits, prior, labels)
        # os = sentences[i].split(" ");
        # for o, r in zip(os, result):
        #     f.write(o + "_" + r + " ")
        # f.write("\n")

main()