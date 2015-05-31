"""
Script useful to compact all the results tests.
If you generate tests with the FullTest.py script,
you can use this script to compact every results.
So if your directory is like this :
    -Test1
    -Test2
    -Test3
And if Test folder contains the results,
run : python routine.py 3
"""

import sys, os


def parse(inFile, outFile, predIndex):
    real = []
    pred = []
    with open(inFile, "r") as inFile:
        inFile.readline()
        for line in inFile.readlines():
            real.append(float(line.split("\t")[-1].replace(",", ".")))
            pred.append(float(line.split("\t")[int(predIndex)].replace(",", ".")))

    with open("NicoResult/" + outFile, "w") as oFile:
        for r, p in zip(real, pred):
            oFile.write(str(r) + "\t" + str(p) + "\n")


def extractK(folder, n):
    listK = []
    for i in range(n):
        with open(folder + "/cluster_" + str(i + 1) + "/cv/resultStat.txt", "r") as cv:
            allLines = cv.read()
            allLines = allLines.split("K optimal is :")
            k = allLines[1].split("k = ")
            k = k[1].split(")")
            k = k[0]
            listK.append(int(k))
    return listK


def extractMatrice(folder, listK, n):
    os.system("mkdir NicoResult/" + folder)
    for i in range(n):
        parse(folder + "/cluster_" + str(i + 1) + "/resultMatrice.txt",
              folder + "/cluster_" + str(i + 1) + "matrice.txt", listK[i] - 1)
    os.system("cat NicoResult/" + folder + "/* > NicoResult/" + folder + "/compact.txt")

    with open("NicoResult/" + folder + "/compact.txt", "r") as compactFile:
        somme = 0
        n = 0
        for line in compactFile.readlines():
            tab = line.split("\t")
            somme += (float(tab[0]) - float(tab[1])) ** 2
            n += 1

    mse = somme / n
    with open("NicoResult/MSE.txt", "a") as result:
        result.write("MSE of " + folder + " = " + str(mse) + "\n")


clusterFolder = ["clustersLinNoWeight", "clustersLinWeight", "clustersPolyNoWeight", "clustersNoCoeffWeight",
                 "clustersNoCoeffNoWeight", "clustersPolyWeight"]
knnFolder = ["KnnNoCoeffWeight", "KnnPolyNoWeight", "KnnPolyWeight", "KnnLinWeight", "KnnLinNoWeight",
             "KnnNoCoefNofWeight"]

for i in range(int(sys.argv[1])):
    os.chdir("Test" + str(i + 1))
    os.system("rm -r NicoResult")
    os.system("mkdir NicoResult")

    for meth in clusterFolder:
        listK = extractK(meth, 6)
        extractMatrice(meth, listK, 6)

    for meth in knnFolder:
        listK = extractK(meth, 1)
        extractMatrice(meth, listK, 1)
    os.chdir("..")

clusterFolder.extend(knnFolder)
os.system("rm -r Compact")
os.system("mkdir Compact")
for i in range(int(sys.argv[1])):
    # For kNN and clusters
    for meth in clusterFolder:
        with open("Test" + str(i + 1) + "/NicoResult/" + meth + "/compact.txt", "r") as coucou:
            content = coucou.read()
        with open("Compact/" + meth + ".txt", "a") as coucou:
            coucou.write(content)

    # Get average of training set
    with open("Test" + str(i + 1) + "/KnnPolyWeight/cluster_1/resultStat.txt", "r") as coucou:
        content = coucou.read()
    sp1 = content.split("average of true value (Training) : ")
    sp2 = sp1[1].split("\n")
    av = float(sp2[0].replace(",", "."))

    with open("Test" + str(i + 1) + "/testGenerate.txt", "r") as resultFile:
        content = resultFile.readlines()

    real = []
    for line in content:
        splited = line.split("\t")
        real.append(float(splited[-1].strip()))

    with open("Compact/average.txt", "a") as coucou:
        for i in real:
            coucou.write(str(i) + "\t" + str(av) + "\n")


def computeMSE(content):
    somme = 0
    n = 0
    for line in content:
        tab = line.split("\t")
        somme += (float(tab[0]) - float(tab[1])) ** 2
        n += 1

    mse = somme / n
    return mse


with open("MSE.txt", "w") as result:
    pass

for meth in clusterFolder:
    with open("Compact/" + meth + ".txt", "r") as compactFile:
        content = compactFile.readlines()

    mse = computeMSE(content)

    with open("MSE.txt", "a") as result:
        result.write("MSE of " + meth + " = " + str(mse) + "\n")

############# AVERAGE
with open("Compact/average.txt", "r") as compactFile:
    content = compactFile.readlines()

mse = computeMSE(content)
with open("MSE.txt", "a") as result:
    result.write("MSE of average = " + str(mse) + "\n")

############# REGRESSION
for i in range(int(sys.argv[1])):
    with open("Test" + str(i + 1) + "/LinearRegr.txt", "r") as coucou:
        content = coucou.read()
    with open("Compact/linear.txt", "a") as coucou:
        coucou.write(content)

    with open("Test" + str(i + 1) + "/PolyRegr.txt", "r") as coucou:
        content = coucou.read()
    with open("Compact/poly.txt", "a") as coucou:
        coucou.write(content)

with open("Compact/linear.txt", "r") as compactFile:
    content = compactFile.readlines()
mse = computeMSE(content)
with open("MSE.txt", "a") as result:
    result.write("MSE of linear = " + str(mse) + "\n")

with open("Compact/poly.txt", "r") as compactFile:
    content = compactFile.readlines()
mse = computeMSE(content)
with open("MSE.txt", "a") as result:
    result.write("MSE of poly = " + str(mse) + "\n")
