from alignfree.fastafileopener import parseFasta
from alignfree.spectracalculator import calculateSpectra
from alignfree.distancematrix import getDistanceMatrix
from alignfree.neighborjoining import calculateNJ


def main():
    filePath = 'GBOL-Spinnentiere.fasta'
    targetPath ='GBOL-Spinnentiere.tre'
    kmerLength = 5

    print('Open Fasta File')
    fastaFile = open(filePath, 'r')
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