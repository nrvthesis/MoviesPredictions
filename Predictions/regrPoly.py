"""
Script to compute the coefficients from
the quadratic regression.

"""
import os, sys

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def createTempFile(numberOfParameters, src, intercept):
    with open("coeffPolyTemp.R", 'w+') as writer:
        path = "coeffPoly.R" if not intercept else "coeffPolyStd.R"
        with open(path, 'r') as temp:
            for line in temp.readlines():

                if line.find("*") == -1:
                    writer.write(line)

                else:
                    line = line.split("*")

                    parameters = []
                    allColumns = ["V" + str(i) for i in range(1,numberOfParameters+1)]

                    for col in allColumns:
                        scale = ' <- scale(data$' + col +')\n' if not intercept else ' <- data$' + col +'\n'
                        writer.write(col + scale)

                    for (index, col) in enumerate(allColumns):

                        parameters.append(col)

                        for beforeI in range(0,index+1):
                            parameters.append('I(' + col + '*' + allColumns[beforeI] + ")")

                    writer.write(line[0])
                    writer.write(" + ".join(parameters))
                    writer.write(line[1])

def generateCoefficients(clustName, testName, intercept = False):
    print('regression for '+clustName)
    numberOfParameters = -1

    with open(clustName +'.txt', "r") as read:
        for line in read.readlines():
            #because of the last value which is the rating
            numberOfParameters = len(line.split("\t")) - 1
            break

    if numberOfParameters == -1:
        print("problem in the paramters")
        sys.exit(6)

    createTempFile(numberOfParameters, clustName, intercept)

    result = os.system('Rscript coeffPolyTemp.R "' +  clustName +'.txt"> tempCoeff.txt')

    if result != 0:
        print('error during the regression')
        print("maybe because you haven't enough rows..." )
        sys.exit(9)

    prefix = "_regr" if intercept else "_"
    with open(clustName + prefix + "coef.txt", "w+") as coef:
        with open('tempCoeff.txt', "r") as tempcoef:
            coefficient = []
            for line in tempcoef.readlines():
                line = line[0:-1].split(' ')

                line = filter(lambda x: isfloat(x) or x == 'NA', line)
                line = map(lambda x : float(x) if isfloat(x) else 0, line)
                coefficient.extend(line)
            if intercept == False:
                coef.write("\t".join(map(lambda x : str(x), coefficient[1:])))
            else:
                coef.write("\t".join(map(lambda x : str(x), coefficient)))


    os.remove("tempCoeff.txt")


    generateNewFile(clustName)
    generateNewFile(testName)


def generateNewFile(src):
    with open(src +'.txt', "r") as read:
        with open(src+'_dataWithCoeff.txt', "w") as writer:
            for line in read.readlines():
                line = line.strip().split("\t")
                newline = []

                for (index, col) in enumerate(line):

                    if index == len(line)-1:
                        newline.append(col)
                        break

                    newline.append(col)

                    if not (isfloat(col)):
                        print("error this col is not a float")
                        sys.exit(6)

                    num = float(col)

                    for beforeI in range(0,index+1):
                        newline.append(str(num * float(line[beforeI])))

                writer.write("\t".join(newline) +'\n')





