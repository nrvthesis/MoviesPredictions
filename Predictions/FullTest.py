"""
Script useful for a batch test.
It takes one argument, the directory name
where the results will be put.

"""

import sys, os
import RegressionCoeff

def launch(instr):
    if os.system(instr) != 0:
        print("error during the computation")
        print(instr)
        sys.exit(5)

def runComputation(folder):

    # Use the db21.txt by default, generate two subsets then they use for the other computations

    launch("python clusterManager.py -T db21.txt -w false -m None -d "+ folder + "/clustersNoCoeffNoWeight")
    launch("python compactResult.py " + folder + "/clustersNoCoeffNoWeight > " + folder + "/clustersNoCoeffNoWeight/compactResult.txt")

    launch("cp trainingGenerate.txt " + folder + "/.")
    launch("cp testGenerate.txt " + folder + "/.")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -m linear -w false -d "+ folder + "/clustersLinNoWeight")
    launch("python compactResult.py " + folder + "/clustersLinNoWeight > " + folder + "/clustersLinNoWeight/compactResult.txt")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -m poly -w false -d "+ folder + "/clustersPolyNoWeight")
    launch("python compactResult.py " + folder + "/clustersPolyNoWeight > " + folder + "/clustersPolyNoWeight/compactResult.txt")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -m None -w true -d "+ folder + "/clustersNoCoeffWeight")
    launch("python compactResult.py " + folder + "/clustersNoCoeffWeight > " + folder + "/clustersNoCoeffWeight/compactResult.txt")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -m linear -w true -d "+ folder + "/clustersLinWeight")
    launch("python compactResult.py " + folder + "/clustersLinWeight > " + folder + "/clustersLinWeight/compactResult.txt")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -m poly -w true -d "+ folder + "/clustersPolyWeight")
    launch("python compactResult.py " + folder + "/clustersPolyWeight > " + folder + "/clustersPolyWeight/compactResult.txt")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -c 1 -m None -w true -d "+ folder + "/KnnNoCoeffWeight")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -c 1 -m linear -w true -d "+ folder + "/KnnLinWeight")
    RegressionCoeff.generateLinearCoeff(folder + "/KnnLinWeight/cluster_1", folder)
    launch("python Utils.py "+ folder + "/KnnLinWeight/cluster_test_1.txt " + folder + "/CoeffLinear.txt " + folder + "/LinearRegr.txt linear")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -c 1 -m poly -w true -d "+ folder + "/KnnPolyWeight")
    RegressionCoeff.generatePolyCoeff(folder + "/KnnPolyWeight/cluster_1", folder + "/KnnPolyWeight/cluster_test_1")
    launch("python Utils.py "+ folder + "/KnnPolyWeight/cluster_test_1_dataWithCoeff.txt " + folder + "/KnnPolyWeight/cluster_1_regrcoef.txt " + folder + "/PolyRegr.txt linear stand")

    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -c 1 -m None -w false -d "+ folder + "/KnnNoCoefNofWeight")
    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -c 1 -m linear -w false -d "+ folder + "/KnnLinNoWeight")
    launch("python clusterManager.py -T trainingGenerate.txt -t testGenerate.txt -c 1 -m poly -w false -d "+ folder + "/KnnPolyNoWeight")

if __name__ == '__main__':

    args = sys.argv[1:]

    if len(args) < 1:
        print("you have to specify the name of the folder")
        sys.exit(1)

    try :
        os.mkdir(args[0])
    except:
        print("can't create the folder")
        sys.exit(2)

    runComputation(args[0])