"""
This script is used to compact results from the clustering.
Used int the FullTest.py
"""

import math
import sys, os

if (len(sys.argv) < 2):
    print("no folder specify")
    sys.exit(2)

name = sys.argv[1] + "/cluster_"
file = "resultStat.txt"

sumOfClusters = 0
nbTotTest = 0
for i in range(1, 7):
    if not os.path.isfile(name+str(i)+'/'+file):
        continue

    with open(name+str(i)+'/'+file, 'r') as read:
        eqmClust = -1
        nbTest = -1

        for line in read.readlines():
            if line.find('(avg value)') > -1:
                eqmClust = float(line.split('(avg value)')[1].split('(')[0].strip().replace(',','.'))

            if line.find('number of test set :') >-1 :
                nbTest = float(line.split(':')[1].strip().replace(',','.'))

            if eqmClust != -1 and nbTest != -1:
                break

        sumOfClusters += (eqmClust**2)*nbTest
        nbTotTest += nbTest

print("eqm : " + str(math.sqrt(sumOfClusters/nbTotTest)))
print("number of test : " + str(nbTotTest))