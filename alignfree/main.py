import sys

from alignfree.fastafileopener import parseFasta
from alignfree.spectracalculator import calculateSpectra
from alignfree.distancematrix import getDistanceMatrix
from alignfree.neighborjoining import calculateNJ
from alignfree.userinterface import (
    getFastaFromUserInput,
    getKmerLength,
    getTargetPath,
    getParameter
)

def main():

    fastaFile, targetPath, kmerLength = getParameter(sys.argv)

    print('Open Fasta File')
    sequences = parseFasta(fastaFile)
    print('Calculate Spectra')
    labelList, spectra = calculateSpectra(sequences, kmerLength)

    print('Get distance-matrix')
    distanceMatrix = getDistanceMatrix(spectra)

    print('Calculate NJ')
    newickString = '(' + calculateNJ(labelList, distanceMatrix) + ');'

    targetFile = open(targetPath, 'w')
    targetFile.write(newickString)

if __name__ == '__main__':
    main()