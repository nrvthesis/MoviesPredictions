"""
Contain some functions to manipulate
the text data set.
We can compute the formula of the
linear regression like this:
    python Utils.py testSet.txt coeff.txt output.txt"
"""

import sys, os, math
import numpy

def rebuild(src, dst):
    for line in src.readlines():
        array = line.split("\t")
        if int(array[5]) > 2010:
            dst.write(line)

def selectLatestMovies():
    with open("goodMovies.txt", "r") as read:
        with open("dbNewMovies2.txt", "w") as write:
            rebuild(read, write)

def dropCol(src, dst):
    for line in src.readlines():
        array = line.split("\t")
        #delete element here
        del array[35]
        for (index, item) in enumerate(array):
            if index == len(array)-1 :
                dst.write(str(item))
            else:
                dst.write(str(item) + "\t")


def drop(src, dst):
    with open(src, "r") as read:
        with open(dst, "w") as write:
            dropCol(read, write)

def extract(inputFile):
    with open(inputFile, "r") as resultFile:
        content = resultFile.readlines()
    resultList = []
    for line in content:
        splited = line.strip().split("\t")
        resultList.append(splited)
    return resultList

def trunc(f, n):
    return ('%.*f' % (n + 1, f))[:-1]

def diff(k):
    resultList = extract("resultFinal.txt")

    numK = len(resultList[0])-1
    numLines = len(resultList)

    for i in range(numK):
        sume = 0
        for line in resultList:
            sume += abs(float(line[i+1])-float(line[0]))
        diff = sume/numLines
        with open("README.txt", "a") as readme:
            readme.write("k = "+str(k[i])+" ---> Moyenne des ecarts = "+str(trunc(float(diff),5))+"\n")

#Standardization of the matrice
def stand(matrice, out):
    field = len(matrice[0])
    lines = len(matrice)
    final = []
    for i in range(field-1) :
        lis = []
        for j in range(lines) :
            lis.append(float(matrice[j][i]))
        maxi = max(lis)
        mini = min(lis)
        nLis = []
        for n in range(lines):
            if (maxi-mini) != 0:
                nLis.append((lis[n]-mini)/(maxi-mini))
            else:   
                nLis.append(0.0)
        final.append(nLis)
        
    with open(out, "w") as res:
        for i in range(lines):
            #add index in front of the line
            #res.write(str(i+1)+"\t") 
            for j in range(field-1):
                res.write(str(final[j][i])+"\t")
            res.write(matrice[i][field-1]+"\n")

def linearRegression(matrice, coef, out):
    with open(coef,"r") as coefFile:
        content = coefFile.readline()
    coef = content.split("\t")
    coef = list(map(float, coef))

    resTab=[]
    for line in matrice:
      res = coef[0]
      for (index, field) in enumerate(line[:-1]):
        res += float(field)*coef[index+1]
      resTab.append(res)

    real = []
    somme = 0
    with open(out, "w") as resFile:
        for (index,line) in enumerate(matrice):
            real.append(line[-1])
            resFile.write(str(line[-1])+"\t"+str(resTab[index])+"\n")
            somme += (float(line[-1]) - resTab[index])**2

    print("MSE "+str(math.sqrt(somme/len(resTab))))

#Compare the ratings with the average of all the ratings
def resultAverage(matrice):
    result = []
    for line in matrice:
        result.append(float(line[-1]))
    av = sum(result)/len(result)
    print('La moyenne des vrais resultats : '+str(av))

    ecarts = 0
    for res in result:
        ecart = abs(res-av)
        ecarts += ecart * ecart

    ecarts = math.sqrt(ecarts/len(result))

    print('Moyenne des ecarts : '+str(ecarts))

def addIndex(matrice):
    with open("db21Head.txt", "w") as resFile:
        for (n, line) in enumerate(matrice):
            resFile.write(str(n+1)+"\t")
            for (index, el) in enumerate(line):
                resFile.write(str(el))
                if index != len(line)-1:
                    resFile.write("\t")
            resFile.write("\n")

#Launch standardization of input file
#matrice = extract(sys.argv[1])
#stand(matrice, sys.argv[2])

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("python Utils.py testSet.txt coeff.txt output.txt")
        sys.exit(1)

    matriceStand = extract(sys.argv[1])
    #Launch linear regression of input file
    linearRegression(matriceStand, sys.argv[2], sys.argv[3])


