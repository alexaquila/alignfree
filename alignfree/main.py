from alignfree.fastafileopener import parseFasta
from alignfree.spectracalculator import calculateSpectra
from alignfree.distancematrix import getDistanceMatrix
from alignfree.neighborjoining import calculateNJ


def main():
    filePath = 'nym.fas'
    kmerLength = 5


    fastaFile = open(filePath, 'r')
    sequences = parseFasta(fastaFile)

    labelList, spectra = calculateSpectra(sequences, kmerLength)

    distanceMatrix = getDistanceMatrix(spectra)

    calculateNJ(labelList, distanceMatrix)

if __name__ == '__main__':
    main()