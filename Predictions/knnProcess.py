from multiprocessing import Process
from math import sqrt

"""
Class used by the knnMain script.
Each instance of the Engine class is a new process (fork).
This class handle the computation of the knn technique.
"""
class Engine(Process):
    def __init__(self, info):

        Process.__init__(self)
        self.processNumber = info.get("processNumber")
        self.numberOfProcess = info.get("numberOfProcess")
        self.matrice = info.get("matrice")
        self.matriceStd = info.get("matriceStd")
        self.resultColumn = info.get("resultColumn")
        self.testSet = info.get("testSet")
        self.testSetResult = info.get("testSetResult")
        self.resultList = info.get("resultList")
        self.maxMinColumns = info.get("maxMinColumns")
        self.fromK = info.get("fromK")
        self.toK = info.get("toK")
        self.coef = info.get("coef")
        self.standForARowTest = False
        self.classification = info.get("classification")

    def run(self):

        maxMin = self.maxMinColumns
        finalMatrice=[]

        currentMatriceStd = self.matriceStd

        for (test, trueResult) in zip(self.testSet, self.testSetResult):

            stand = self.standardisationOfMatAndTest(currentMatriceStd, test, self.maxMinColumns)

            listOrderDistResult = self.distEuclid(*stand)[self.fromK-1:self.toK]

            resultKnn = self.averageResultFromDistEucl(listOrderDistResult)

            finalMatrice.append((resultKnn, trueResult))

        self.resultList.extend(finalMatrice)


    def standardisationOfMatAndTest(self, matriceStd, test, maxMin):

        better = self.rowBetterThanMaxMin(test)

        if better :
            #update matrice + test
            self.standForARowTest = True
            currentMatriceStd = self.updateMatriceStd(self.matrice, better, self.coef)
            currentTestStd = self.generateRowStd(test, better, self.coef)

        elif not self.standForARowTest :
            #update test
            currentMatriceStd = matriceStd
            currentTestStd = self.generateRowStd(test, maxMin, self.coef)

        else :
            #update test + matrice
            self.standForARowTest = False
            currentMatriceStd = self.updateMatriceStd(self.matrice, maxMin, self.coef)
            currentTestStd = self.generateRowStd(test, maxMin, self.coef)

        return (currentMatriceStd, currentTestStd)


    def averageResultFromDistEucl(self, listDistResult):

        castFloat = float

        if self.classification == 'true':
            l = lambda nb: sum(
                map (lambda stat: stat[1]/stat[0] if stat[0] > 0 else stat[1]/0.000001 , map(None, listDistResult[0:nb+1]))
            ) / sum (map(lambda dist: 1.0/dist if dist > 0 else 1.0/0.000001 ,map(None, *listDistResult[0:nb+1])[0] if nb>0
                                                            else (map(None, *listDistResult[0:nb+1])[0],) ))

        else:
            l = lambda nb: sum(
            map(None, *listDistResult[0:nb+1])[1] if nb>0
            else (map(None, *listDistResult[0:nb+1])[1],)
            ) /castFloat(nb+1)

        return map(l, range(len(listDistResult)))


    def distEuclid(self, matrice, testLine):

        resultColumn = self.resultColumn
        l = lambda col, test: pow( (col - test), 2)
        result = map(lambda row, result: (sqrt(sum(map(l, row, testLine))), result), matrice, resultColumn)
        result.sort()
        return result


    def rowBetterThanMaxMin(self, rows):

        mm = self.maxMinColumns
        better = False
        res = []
        for index in range(len(rows)):
            if mm[index] < rows[index]:
                better = True
                res.append(mm[index])
            else:
                res.append(rows[index])

        return res if better else None

    def generateRowStd(self, row, maxMin, coef):

        standardisation = lambda item, mM, c: ((item-mM[1])/(mM[0]-mM[1])*c) if (mM[0]-mM[1]) else 0.0
        return map(standardisation , row, maxMin, coef)

    @classmethod
    def updateMatriceStd(self, matrice, maxMin, coef):

        standardisation = lambda item, mM, c: ((item-mM[1])/(mM[0]-mM[1])*c) if (mM[0]-mM[1]) else 0.0
        std = map(lambda row:
            map(standardisation, row, maxMin, coef),
                  matrice)
        return std

