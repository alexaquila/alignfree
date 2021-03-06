import math

def multiplicationVector(X, Y):
    x, y = 0, 0
    weight = 0.0

    while x < len(X) and  y < len(Y):
        while x < len(X) and X[x][0] < Y[y][0]:
            x += 1
        while y < len(Y) and x < len(X) and Y[y][0] < X[x][0]:
            y += 1
        while y < len(Y)  and x < len(X) and Y[y][0] == X[x][0]:
            weight += X[x][1] * Y[y][1]
            x += 1
            y += 1
    return weight

def calculateSim(distanceMatrix, spectra):
    numberOfSpectra = len(spectra)
    # Calculate magnitude of every vector
    magnitude = []
    for spectrum in spectra:
        magnitude.append(multiplicationVector(spectrum, spectrum))
    for x in range(numberOfSpectra):
        if x % 10 == 9:
            print('Calculated the distances of ' + str(x+1) + ' of ' + str(numberOfSpectra) + ' specimen.')
        for y in range(x + 1, numberOfSpectra):
            K_X_Y = multiplicationVector(spectra[x], spectra[y])
            K_X_X = magnitude[x]
            K_Y_Y = magnitude[y]
            distanceMatrix[x][y] = distanceMatrix[y][x] = 1 - K_X_Y/math.sqrt(K_X_X*K_Y_Y)

def printMatrix(matrix):
    for row in matrix:
        print(row)


def formatRow(row):
    if not row ==[]:
        outputString =str(row[0])
        for element in row[1:]:
            outputString += ',' + str(element)
        return outputString
    else:
        return ''

def getMatrixStringFromMatrix(matrix, labelList):
    outputString = formatRow(labelList)
    for row in matrix:
        outputString += '\n' + formatRow(row)
    return outputString

def getColumnStringFromMatrix(matrix, labelList):
    outputString = ''
    n = len(matrix)
    for row in range(0,n-1):
        for column in range(row+1, n):
            outputString += labelList[row] + ','
            outputString += labelList[column] + ','
            outputString += str(matrix[row][column]) + '\n'
    return outputString

def getDistanceMatrix(spectra):
    numberOfSpectra = len(spectra)
    distanceMatrix =[[0.0 for x in range(numberOfSpectra) ] for y in range(numberOfSpectra)]
    calculateSim(distanceMatrix, spectra)
    return distanceMatrix
