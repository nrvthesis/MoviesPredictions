"""
This script is one of the major script.
It is used to compute almost every techniques :
    - k-NN with/out coefficients and with/out distance-weighted
    - clustering

You can use the -h or --help argument to access all the parameters.
If you don't give a test set as argument, it will be generate based
on the training set (and output two new files).
"""

import os, sys
import knnMain
import random
import getopt
import regrPoly

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def readMatrice(src):
    matrice = []
    with open(src, "r+") as read:
        for line in read.readlines():
            matrice.append(line)
    return matrice


def generateTest(matrice, percentInTraining):
    testSet = []
    number = len(matrice)*(float(percentInTraining)/100)

    for index in range(int(number)):
        r = random.randint(0, len(matrice)-1)
        testSet.append(matrice[r])
        del matrice[r]
    return testSet


def clusterLauncher(training, test, nbProcess,
                    percentInTraining, fromK, toK,
                    clustersNumber, dir, methodForCoef, classification):

    matrice = readMatrice(training)

    # generate a test set if there isn't
    if not test:
        matriceTest = generateTest(matrice, percentInTraining)
        training = "trainingGenerate.txt"
        open(training, "w+").write("".join(map(lambda line: str(line), matrice)))

        test = "testGenerate.txt"
        open(test, "w+").write("".join(map(lambda line: str(line), matriceTest)))

    else:
        matriceTest = readMatrice(test)

    result = os.system('Rscript cluster.R "' + training + '" ' + str(clustersNumber) + ' "' + test + '" > clusterMatrice.txt')


    clusters = []
    testClusters = []

    if result == 0:
        testGo = False
        with open("clusterMatrice.txt", "r") as read:

            for line in read.readlines():
                if str(line).find("Class") > -1:
                    testGo = True
                    continue

                line = line[0:-1].split(' ')

                line = filter(lambda x: x.isdigit(), line)
                line = map(lambda x : int(x), line)

                if not testGo:
                    clusters.extend(line)

                else:
                    testClusters.extend(line)

    else :
        print("error during the clustering")
        sys.exit(3)

    os.remove("clusterMatrice.txt")

    if len(clusters) != len(matrice) :
        print("error not the same number")
        exit(3)

    try:
        os.mkdir(dir)
    except OSError as e:
        print(e.strerror)
        print('error to create the result folder')
        sys.exit(3)


    prefixName = dir + "/cluster_"
    def openFile(name):
        return open(prefixName+str(name)+".txt", "w+")

    numClusters = range(1, int(clustersNumber)+1)

    writers = map(openFile, numClusters)

    tempName = prefixName
    prefixName += "test_"
    testFiles = map(openFile, numClusters)

    def createCluster(clusterNumber, row):
        writers[clusterNumber-1].write(row)


    map(createCluster, clusters, matrice)
    map(lambda w: w.close(), writers)

    writers = testFiles
    map(createCluster, testClusters, matriceTest)
    map(lambda w: w.close(), testFiles)

    for clustNumber in range(1, int(clustersNumber)+1):

        forpoly = ""
        if methodForCoef == "linear":
            result = os.system('Rscript coeffLinear.R "' +  tempName+str(clustNumber)+'.txt" > tempCoeff.txt')

            if result != 0:
                print('error during the regression')
                print("maybe because you haven't enough rows..." )
                sys.exit(9)

            with open(tempName+str(clustNumber)+"_coef.txt", "w+") as coef:
                with open('tempCoeff.txt', "r") as tempcoef:
                    coefficient = []
                    for line in tempcoef.readlines():
                        line = line[0:-1].split(' ')

                        line = filter(lambda x: isfloat(x) or x == 'NA', line)
                        line = map(lambda x : float(x) if isfloat(x) else 0, line)
                        coefficient.extend(line)
                    coef.write("\t".join(map(lambda x : str(x), coefficient[1:])))

            os.remove("tempCoeff.txt")

        elif methodForCoef == "poly":
            regrPoly.generateCoefficients(tempName+str(clustNumber), prefixName+str(clustNumber))
            forpoly = '_dataWithCoeff'


        if methodForCoef != 'linear' and methodForCoef != 'poly' :
            knnMain.arguments(["-T", tempName+str(clustNumber)+forpoly+".txt",
                               "-p", nbProcess,
                               "-f",fromK,
                               "-k", toK,
                               "-d", tempName+str(clustNumber),
                               "-t", prefixName+str(clustNumber)+forpoly+".txt",
                               "-w", classification])

        else:
            knnMain.arguments(["-T", tempName+str(clustNumber)+forpoly+".txt",
                           "-p", nbProcess,
                           "-f",fromK,
                           "-k", toK,
                           "-d", tempName+str(clustNumber),
                           "-t", prefixName+str(clustNumber)+forpoly+".txt",
                           "-c", tempName+str(clustNumber)+"_coef.txt",
                           "-w", classification])
        try:
            os.mkdir(+tempName+str(clustNumber)+"/cv")
        except:
            pass

        launch("python knnMain.py -T '"+tempName+str(clustNumber)+forpoly+".txt"+"' -d '"+tempName+str(clustNumber)+"/cv'")


def launch(instr):
    if os.system(instr) != 0:
        print("error during the computation")
        print(instr)
        sys.exit(5)

def help():
    print("-T | --trainingSet: path training set (default : dbRating.txt)")
    print("-t | --testSet : path test set (default : percentInTraining percent in training set)")
    print("-p | --nbProcess : number of process (default : 4)")
    print("-f | --fromK : number for the start of K list (default : 1)")
    print("-k | --toK : number for the end of K list (default :100)")
    print("-r | --percentInTraining : number of percent taked in training set to create a test set if no test set (default : 10)")
    print("-d | --directory : name of the directory (default: 'cluster')")
    print("-c | --clustersNumber : number of clusters (default: 6)")
    print("-m | --methodForCoef : method to compute coefficient - linear | poly | None (default: linear)")
    print("-w | --weight : classification for the knn - true | false (default: 'false')")
    print("-h | --help : help menu")

def arguments(argv):
    try:
        opts, args = getopt.getopt(argv, "T:t:p:f:k:r:c:d:m:w:h",
                                   ["trainingSet=","testSet=","nbProcess=",
                                    "fromK=","toK=","percentInTraining=",
                                    "clustersNumber=","directory=", "methodForCoef=","classification=","help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    training = "smallDBToTest.txt"
    test = None
    nbProcess = 4
    percentInTraining = 10
    fromK = 1
    toK = 100
    clustersNumber = 6
    dir = "clusters"
    methodForCoef = 'linear'
    classification='false'

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

            elif opt in ("-c", "--clustersNumber"):
                clustersNumber = arg

            elif opt in ("-m", "--methodForCoef"):
                if arg not in ("linear", "poly", "None"):
                    print("methodForCoef has to be linear or poly")
                    sys.exit(4)

                methodForCoef = arg

            elif opt in ("-w", "--weight"):
                classification = arg
    except:
        help()
        sys.exit(2)

    clusterLauncher(training, test, nbProcess,
                    percentInTraining, fromK, toK,
                    clustersNumber, dir, methodForCoef, classification)



if __name__ == '__main__':
    arguments(sys.argv[1:])