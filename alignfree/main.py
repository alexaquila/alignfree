import sys

from alignfree.fastafileopener import parseFasta
from alignfree.spectracalculator import calculateSpectra
from alignfree.distancematrix import getDistanceMatrix, getStringFromMatrix
from alignfree.neighborjoining import calculateNJ
from alignfree.userinterface import getParameter

def main():

    fastaFile, targetPath, kmerLength = getParameter(sys.argv)

    print('Open Fasta File')
    sequences = parseFasta(fastaFile)
    print('Calculate Spectra')
    labelList, spectra = calculateSpectra(sequences, kmerLength)

    print('Get distance-matrix')
    distanceMatrix = getDistanceMatrix(spectra)

    csvString = getStringFromMatrix(distanceMatrix, labelList)
    print('Calculate NJ')
    newickString = calculateNJ([frozenset({label}) for label in labelList], distanceMatrix) + ';'

    targetCSV = open(targetPath + '.csv', 'w')
    targetCSV.write(csvString)

    targetTree = open(targetPath + '.tre', 'w')
    targetTree.write(newickString)

if __name__ == '__main__':
    main()