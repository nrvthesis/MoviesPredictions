"""
Script useful to generate the coefficients
from the linear and quadratic regression.
These methods are important to be able to reuse
the intercept and feature coefficients for the
formula of the linear and quadratic regression.

"""
import os
import sys
import regrPoly
import Utils

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def generateLinearCoeff(training, folder):

    result = os.system('Rscript coeffLinearStd.R "' +  training +'.txt" > ' + folder + '/tempCoeff.txt')

    if result != 0:
        print('error during the regression')
        print("maybe because you haven't enough rows..." )
        sys.exit(9)

    with open(folder + '/CoeffLinear.txt', "w+") as coef:
        with open(folder + '/tempCoeff.txt', "r") as tempcoef:
            coefficient = []
            for line in tempcoef.readlines():
                line = line.strip().split(' ')

                line = filter(lambda x: isfloat(x) or x == 'NA', line)
                line = map(lambda x : float(x) if isfloat(x) else 0, line)
                coefficient.extend(line)
            coef.write("\t".join(map(lambda x : str(x), coefficient)))

    os.remove(folder + '/tempCoeff.txt')

def generatePolyCoeff(training, test):
    regrPoly.generateCoefficients(training, test, intercept=True)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("python RegressionCoeff.py trainingSet testSetForPoly|folderForLinear linear|poly")

    if sys.argv[3] == 'poly':
        generatePolyCoeff(sys.argv[1], sys.argv[2])
    elif sys.argv[3] == 'linear':
        generateLinearCoeff(sys.argv[1], sys.argv[2])
    else:
        print("linear or poly")
