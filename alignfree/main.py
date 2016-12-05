from alignfree.fastafileopener import parseFasta
from alignfree.spectracalculator import calculateSpectra
from alignfree.distancematrix import getDistanceMatrix
from alignfree.neighborjoining import calculateNJ


def main():
    filePath = 'nym.fas'
    targetPath ='nym.tree'
    kmerLength = 5


    fastaFile = open(filePath, 'r')
    sequences = parseFasta(fastaFile)

    labelList, spectra = calculateSpectra(sequences, kmerLength)

    distanceMatrix = getDistanceMatrix(spectra)

    newickString = calculateNJ(labelList, distanceMatrix) + ';'

    targetFile = open(targetPath, 'w')
    targetFile.write(newickString)

if __name__ == '__main__':
    main()