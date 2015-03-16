import numpy
import sys,os
import csv
import math
from random import uniform

learnRate = 0.1

class Unit:
    def __init__(self, n):
        self.num = n + 1
        self.weights = []
        self.out = 0
        self.input = []
        for i in xrange(0, self.num):
            self.weights.append(uniform(-0.2, 0))
            #self.weights.append(-0.01)
    def produce(self, instance):
        self.input = instance
        value = 0.0
        for i in xrange(0, self.num):
            value += self.input[i] * self.weights[i]
        if(abs(value) >= 700):
            value = 700 if value > 0 else -700
        self.out = 1.0 / (1.0 + math.exp(-1 * value))
        return self.out

    def p(self, instance):
        value = 0.0
        for i in xrange(0, self.num):
            value += instance[i] * self.weights[i]
        if(abs(value) >= 700):
            value = 700 if value > 0 else -700
        return 1.0 / (1.0 + math.exp(-1 * value))

    def updateWeights(self, si):
        for i in xrange(0, len(self.weights)):
            delta = learnRate * self.weights[i] * self.input[i]
            self.weights[i] += delta


class OutUnit:
    def __init__(self, n):
        self.num = n
        self.weights = []
        self.out = 0
        self.input = []
        for i in xrange(0, self.num):
            self.weights.append(uniform(-0.2, 0))
            #self.weights.append(-0.01)

    def produce(self, instance):
        self.input = instance
        value = 0.0
        for i in xrange(0, self.num):
            value += self.input[i] * self.weights[i]
        #if(abs(value) >= 700):
        #    value = 700 if value > 0 else -700
        self.out = 1.0 / (1.0 + math.exp(-1 * value))
        return self.out

    def p(self, instance):
        value = 0.0
        for i in xrange(0, self.num):
            value += instance[i] * self.weights[i]
        if(abs(value) >= 700):
            value = 700 if value > 0 else -700
        return 1.0 / (1.0 + math.exp(-1 * value))

    def getWeight(self, i):
        return self.weights[i]

    def updateWeights(self, si):
        for i in xrange(0, len(self.weights)):
            delta = learnRate * self.weights[i] * self.input[i]
            self.weights[i] += delta

def setYesNo(line):
    if line == "yes":
        return 1.0
    else:
        return 0.0

def readCVS(filename):
	reader = csv.reader(file(filename, 'rb'))
	return reader

def createMusicInstancs(reader):
    instances = []
    attr = []
    labels = []
    first = True;
    for line in reader:
        if not first:
         line[0] = (float(line[0]) - 1900.0) / 10.0;
         line[1] = (float(line[1]))
         line[2] = setYesNo(line[2])
         line[3] = setYesNo(line[3])
         labels.append(setYesNo(line[4]))
         line.pop()
         instances.append(line)
        else:
            attr = line
            first = False
    return instances, attr, labels;

def createFeature(reader):
    feature = []
    first = True;
    for line in reader:
        if not first:
         line[0] = (float(line[0]) );
         line[1] = (float(line[1]))
         line[2] = setYesNo(line[2])
         line[3] = setYesNo(line[3])
         feature.append(line)
        else:
            first = False
    return feature

def initNeuralNet(layersize):
    units = []
    oUnit = None
    for i in xrange(0, layersize):
        u = Unit(4)
        units.append(u)
    oUnit = OutUnit(layersize)
    return units, oUnit

def produce(instance, units, oUnit):
    instance.insert(0, 1.0)
    t = []
    for i in xrange(0, len(units)):
        u = units[i]
        t.append(u.produce(instance))
        units[i] = u
    fi = oUnit.produce(t)
    return units, oUnit

def p(instance, units, oUnit):
    instance.insert(0, 1.0)
    t = []
    for unit in units:
        t.append(unit.p(instance))
    return oUnit.p(t)

def sig(value):
    return math.tanh(value) * (1.0 - math.tanh(value))

def Backpropagation(label, units, oUnit):
    sil = sig(oUnit.out) * (label - oUnit.out)
    for i in xrange(0, len(units)):
        w = oUnit.getWeight(i)
        u = units[i]
        sih = w * sil * sig(u.out)
        u.updateWeights(sih)
        #units[i] = u
    oUnit.updateWeights(sil)
    return units, oUnit

#TODO: not sure if change instance in unit
def error(instances,labels, units, oUnit):
    err = 0.0
    for i in xrange(0, len(instances)):
        v = p(instances[i], units, oUnit)
        err +=  math.pow(v - labels[i], 2)
    return 0.5 * err

def train(instances, labels, units, oUnit):
    for i in xrange(0, len(instances)):
        produce(instances[i], units, oUnit)
        Backpropagation(labels[i], units, oUnit)
    err = error(instances, labels, units, oUnit)
    sys.stdout.write(str(err) + "\n")
    return units, oUnit



def buildNeuralNet(layersize, instances, labels):
    units, oUnit = initNeuralNet(layersize)
    for i in xrange(0, 20):
         train(instances, labels, units, oUnit)
    return units,oUnit

def predicate(features, units, oUnit):
    sys.stdout.write("TRAINING COMPLETED! NOW PREDICTING.\n")
    for feature in features:
        #print feature
        c = p(feature, units, oUnit)
        if(c > 0.5):
            sys.stdout.write("yes" + "\n")
        else:
            sys.stdout.write("no" + "\n")

def regularization(instances):
    num = 0
    for instance in instances:
        num += 1
    num = num * 1.0
    for i in xrange(0, 4):
        min = sys.maxint
        max = -sys.maxint - 1
        total = 0
        for instance in instances:
            if instance[i] < min:
                min = instance[i]
            if instance[i] > max:
                max = instance[i]
            total += instance[i]
        len = (max - min) * 1.0
        avg = total / (num)
        for instance in instances:
            instance[i] = (instance[i] - avg) / len
    return instances

def main():
    reader = readCVS(sys.argv[1])
    instances, attr, labels = createMusicInstancs(reader)
    instances = regularization(instances)
    units, oUnit = buildNeuralNet(5, instances, labels)
    reader = readCVS(sys.argv[2])
    features = createFeature(reader)
    predicate(features, units, oUnit)

main()
