import math


def calculateIntermediateMatrix(distanceMatrix, nettoDivergenceList):
    n = len(nettoDivergenceList)
    # M = [[0.0 for x in range(n)] for y in range(n)]
    minimumValue, minimumTuple = float('inf'), (0, 0)
    for x in range(n):
        for y in range(x + 1, n):
            M = distanceMatrix[x][y] - nettoDivergenceList[x] - nettoDivergenceList[y]
            if M < minimumValue:
                minimumValue = M
                minimumTuple = (x, y)
    return minimumTuple


def nettoDivergence(rowOfDistances):
    n = len(rowOfDistances)
    assert n > 3
    sum = 0.0
    for distance in rowOfDistances:
        sum += distance
    return sum / (n - 2)


def calculateNettoDivergenceList(distanceMatrix):
    nettoDivergenceList = []
    for rowOfDistances in distanceMatrix:
        nettoDivergenceList.append(nettoDivergence(rowOfDistances))

    return nettoDivergenceList


def mergeGroups(distanceMatrix, labelGroups, minimumTuple):
    index1, index2 = minimumTuple[0], minimumTuple[1]
    print(minimumTuple)
    distance = distanceMatrix[index1][index2]
    distanceElement1 = distance 
    element1, element2 = labelGroups[index1], labelGroups[index2]
    newGroup = frozenset({element1, element2})
    labelGroups.remove(element1)
    labelGroups.remove(element2)

    labelGroups.append(newGroup)
    return labelGroups


def calculateNJ(labelList, distanceMatrix):
    labelGroups = [frozenset({label}) for label in labelList]
    nettoDivergenceList = calculateNettoDivergenceList(distanceMatrix)
    minimumTuple = calculateIntermediateMatrix(distanceMatrix, nettoDivergenceList)

    labelGroups = mergeGroups(distanceMatrix, labelGroups, minimumTuple)
