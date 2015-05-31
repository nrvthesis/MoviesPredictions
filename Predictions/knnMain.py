"""
Script to compute a k-NN technique.
If you want to know every possibility of
this script, run : python knnMain.py --help
"""

from knnProcess import Engine
import sys, time
from multiprocessing import Manager
import copy
import math
import datetime
import getopt
import os
import numpy as np
import random

def readMatrice(src):
    matrice = []
    res = []
    with open(src, "r") as read:
        for line in read.readlines():
            line = line[:-1].split()
            matrice.append([float(i) for i in line[:-1]])
            res.append(float(line[-1]))
    return matrice, res


def generateTest(matrice, resultColumn, percentInTraining):
    testSet = []
    testSetResult = []
    number = len(matrice)*(float(percentInTraining)/100)

    for index in range(int(number)):
        r = random.randint(0, len(matrice)-1)
        testSet.append(matrice[r])
        testSetResult.append(resultColumn[r])
        del matrice[r]
        del resultColumn[r]
    return (testSet, testSetResult)

def generateMaxMinColumns(matrice):
    maxMin = []
    transpose = map(None, *matrice)

    for column in transpose:
        maxMin.append((max(column), min(column)))
    return maxMin


def coefficient(coef):
    with open(coef, "r") as read:
        return [float(i) for i in read.readline().strip().split("\t")]


def runMain(training, test,
            nbProcess, percentInTraining ,
            fromK, toK, coef, dir, classification):
    """ matrice = the whole training matrice
    resultColumn = the result column
    testSet = the set we want to predict
    maxMinColumns = (maximum, mininmum)  of a each columns """


    begin = time.time()

    matrice, resultColumn = readMatrice(training)

    testSet, testSetResult = readMatrice(test) if test else generateTest(matrice, resultColumn, percentInTraining)

    numberOfTest = len(testSet)

    #no calcul
    if len(testSet) == 0:
        print("test set is empty...")
        return

    #because bug if just one line because of map function
    if len(testSet) == 1:
        testSet.append(copy.deepcopy(testSet[0]))
        testSetResult.append(copy.deepcopy(testSetResult[0]))

    if len(matrice[0])-1 == len(testSet[0]):
        def appendMap(a, b):
            a.append(b)
            return a
        testSet = map(appendMap, testSet, testSetResult)
        testSetResult = map(lambda x: 0.0, testSet)

    if len(matrice[0]) != len(testSet[0]):
        print("wrong matrice (training or set)")
        print("not the same number of column")
        sys.exit(3)

    coefArray = coefficient(coef) if coef else [1.0 for _ in range(len(matrice[0]))]

    if len(coefArray) != len(matrice[0]):
        print("coef has wrong length")
        return

    maxMinColumns = generateMaxMinColumns(matrice)
    setPerProcess = len(testSet)/nbProcess

    matriceStd = Engine.updateMatriceStd(matrice, maxMinColumns, coefArray)

    listProcess = []

    #resultList =  [ row=1 ([ k1, k=2, ....], trueValue), row=2 .... ]
    resultList= Manager().list()

    for i in range(nbProcess):

        if i == nbProcess-1 :
            set = testSet[(i*setPerProcess):]
            setResult = testSetResult[(i*setPerProcess):]
        else:
            set = testSet[(i*setPerProcess) : ((i*setPerProcess)+setPerProcess)]
            setResult = testSetResult[(i*setPerProcess) : ((i*setPerProcess)+setPerProcess)]

        info = {"processNumber":i, "numberOfProcess":nbProcess, "matrice":matrice,
                "resultColumn":resultColumn, "testSet":set, "testSetResult":setResult, "resultList":resultList,
                "maxMinColumns":maxMinColumns, "matriceStd":matriceStd,
                "fromK":fromK, "toK":toK, "coef":coefArray, "classification":classification}

        process = Engine(info)
        listProcess.append(process)
        process.start()

    for process in listProcess:
        process.join()

    with open(dir+"resultMatrice.txt", "w") as resultFile:

        resultFile.write("\t".join(map(lambda nb: "k="+str(nb), range(fromK, toK+1))) + "\ttrueValue\n")

        resultFile.write("\n".join(
            map( lambda row: "\t".join(map(lambda col: str(col), row[0])) + "\t" + str(row[1]),
                 resultList)).replace('.', ','))


    with open(dir+"resultStat.txt", "w") as statFile:

        statFile.write("\t".join(map(lambda nb: "k="+str(nb), range(fromK, toK+1))) + "\n")

        statFile.write("average of ecart : \n")

        temp = map(None, *resultList)

        calc = map(lambda k:
                str(sum(map(lambda val, true: abs(val-true), k, temp[1]))/float(len(k))),
                map(None, *temp[0]))

        statFile.write("\t".join(calc).replace('.', ',')+"\n")


        statFile.write("average value : \n")
        #this compute the average of each estimation for each k
        statFile.write("\t".join(map(lambda k: str(sum(k)/float(len(k))), map(None, *map(None, *resultList)[0]))).replace('.', ',')+"\n")


        def calcValue(f):
            return map(lambda k:
                str(f(k)),
                map(None, *temp[0]))

        varianceValue = calcValue(stat_variance)
        ecartValue = calcValue(stat_ecart_type)
        medianValue = calcValue(median)
        carreAverageValue = map(lambda k:
                str(math.sqrt(sum(map(lambda val, true: (val-true)**2, k, temp[1]))/float(len(k)))),
                map(None, *temp[0]))


        index = 0
        calcf = map(lambda f: float(f), carreAverageValue)
        minK = min(calcf)
        for ind ,i in enumerate(calcf):
            if i == minK:
                index = ind
                break

        statFile.write("variance value : \n")
        statFile.write("\t".join(varianceValue).replace('.', ',')+"\n")

        statFile.write("ecart-type value : \n")
        statFile.write("\t".join(ecartValue).replace('.', ',')+"\n")

        statFile.write("median value : \n")
        statFile.write("\t".join(medianValue).replace('.', ',')+"\n")

        statFile.write("average value ( sqrt( sum((x'-x)**2) /len(X) ) ): \n")
        statFile.write("\t".join(carreAverageValue).replace('.', ',')+"\n\n")


        statFile.write("average of true value (setTest) : " + str(sum(temp[1])/float(len(temp[1]))).replace('.', ',') + "\n")
        statFile.write("median of true value (setTest) : " + str(median(temp[1])).replace('.', ',') + "\n")
        statFile.write("variance of true value (setTest) : " + str(stat_variance(temp[1])).replace('.', ',') + "\n")
        statFile.write("ecart type of true value (setTest) : " + str(stat_ecart_type(temp[1])).replace('.', ',') + "\n\n")
        statFile.write("K optimal is : (avg of ecart) " + str(calc[index]).replace('.', ',') + " - (avg value) " + str(minK).replace('.', ',') + " (k = "+str(index+1)+")\n\n")

        statFile.write("average of true value (Training) : " + str(sum(resultColumn)/float(len(resultColumn))).replace('.', ',') + "\n")
        statFile.write("median of true value (Training) : " + str(median(resultColumn)).replace('.', ',') + "\n")
        statFile.write("variance of true value (Training) : " + str(stat_variance(resultColumn)).replace('.', ',') + "\n")
        statFile.write("ecart type of true value (Training) : " + str(stat_ecart_type(resultColumn)).replace('.', ',') + "\n\n")

        statFile.write("number of training set : "+ str(len(resultColumn)).replace('.', ',') +"\n" )
        statFile.write("number of test set : "+ str(numberOfTest).replace('.', ',') +"\n" )
        statFile.write("number of both sets : "+ str(len(resultColumn) + numberOfTest).replace('.', ',') +"\n\n" )

        statFile.write("time of execution " + str(time.time() - begin).replace('.', ',') + " with "+ str(nbProcess) +" process\n")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        statFile.write("date :  "+ date +"\n")



#From website -----------------------
def stat_variance( echantillon ) :
    return np.var(echantillon)


def stat_ecart_type( echantillon ) :
    return np.std(echantillon)


def median(lst):
    return np.mean(lst)

#-------------------------------------------

def help():
    print("-T | --trainingSet: path training set (default : dbRating.txt)")
    print("-t | --testSet : path test set (default : percentInTraining percent in training set)")
    print("-p | --nbProcess : number of process (default : 4)")
    print("-f | --fromK : number for the start of K list (default : 1)")
    print("-k | --toK : number for the end of K list (default :100)")
    print("-r | --percentInTraining : number of percent taked in training set to create a test set if no test set (default : 10)")
    print("-c | --coefficient : path for coefficient (default : an array of [1, 1, 1, ...])")
    print("-d | --directory : name of the directory (default: 'result')")
    print("-w | --weight : classification for the knn - true | false (default: 'false')")
    print("-h | --help : help menu")

def arguments(argv):

    try:
        opts, args = getopt.getopt(argv, "T:t:p:f:k:r:c:d:w:h",
                                   ["trainingSet=","testSet=","nbProcess=",
                                    "fromK=","toK=","percentInTraining=",
                                    "coefficient=","directory=","weight=", "help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    training = "dbRating.txt"
    test = None
    nbProcess = 4
    percentInTraining = 10
    fromK = 1
    toK = 100
    coef = None
    dir = "test"
    classification='false'
    #if not opts:
    #    help()
    #    sys.exit(2)

    try:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                help()
                sys.exit(2)

            elif opt in ("-T", "--trainingSet"):
                training = arg

            elif opt in ("-t", "--testSet"):
                test = arg

            elif opt in ("-p", "--nbProcess"):
                nbProcess = int(arg)

            elif opt in ("-r", "--percentInTraining"):
                percentInTraining = int(arg)

            elif opt in ("-f", "--fromK"):
                fromK = int(arg)

            elif opt in ("-k", "--toK"):
                toK = int(arg)

            elif opt in ("-d", "--directory"):
                dir = arg

            elif opt in ("-c", "--coefficient"):
                coef = arg

            elif opt in ("-w", "--weight"):
                classification = arg
    except:
        help()
        sys.exit(2)

    os.mkdir(dir)

    dir += "/"

    runMain(training, test, nbProcess, percentInTraining, fromK, toK, coef, dir, classification)


if __name__ == '__main__':
    #arguments(["-T","smallDBToTest.txt",
    #                       "-w", 'false',
    #                       "-t", "testGenerate.txt"])

    arguments(sys.argv[1:])
