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
    assert n > 2
    sum = 0.0
    for distance in rowOfDistances:
        sum += distance
    return sum / (n - 2)

def calculateNettoDivergenceList(distanceMatrix):
    nettoDivergenceList = []
    for rowOfDistances in distanceMatrix:
        nettoDivergenceList.append(nettoDivergence(rowOfDistances))

    return nettoDivergenceList

def getMergedGroup(distanceMatrix, minimumElementsAsTuple, minimumTuple, nettoDivergenceList):
    distance = distanceMatrix[minimumTuple[0]][minimumTuple[1]]
    distance1 = (distance + nettoDivergenceList[minimumTuple[0]] - nettoDivergenceList[minimumTuple[1]]) / 2
    distance2 = (distance + nettoDivergenceList[minimumTuple[1]] - nettoDivergenceList[minimumTuple[0]]) / 2

    return frozenset({(distance1, minimumElementsAsTuple[0]), (distance2, minimumElementsAsTuple[1])})

def addMergedGroup(labelGroups, mergedGroup):
    labelGroups.append(mergedGroup)
    return labelGroups


def eraseGroups(labelGroups, minimumTuple):
    element1, element2 = labelGroups[minimumTuple[0]], labelGroups[minimumTuple[1]]
    labelGroups.remove(element1)
    labelGroups.remove(element2)
    return labelGroups


def calculateNextDistanceMatrix(distanceMatrix, minimumTupel):
    # Initiate n+1 row and n+1 column
    n = len(distanceMatrix)
    for index in range(n):
        distanceMatrix[index].append(0.0)
    distanceMatrix.append([0.0] * (n + 1))

    distance = distanceMatrix[minimumTupel[0]][minimumTupel[1]]
    for x in range(n):
        distanceMatrix[n][x] = distanceMatrix[x][n] = (
                                                          distanceMatrix[minimumTupel[0]][x] +
                                                          distanceMatrix[minimumTupel[1]][x] - distance) / 2

    assert minimumTupel[0] < minimumTupel[1]
    del distanceMatrix[minimumTupel[1]]
    del distanceMatrix[minimumTupel[0]]
    for x in range(n - 1):
        del distanceMatrix[x][minimumTupel[1]]
        del distanceMatrix[x][minimumTupel[0]]
    return distanceMatrix

def getNewickTree(treeOfSets):
    string = ''
    for element in treeOfSets:
        if type(element) == tuple:
            string += getNewickTree(element[1]) + ':' + str(element[0]) + ','
        elif type(element) == str:
            return element
    if string[-1] == ',':
        string = '(' + string[0:-1] + ')'
    else:
        string = '(' + string + ')'
    return string

def getLastMergedGroup(distanceMatrix, minimumElementsAsTuple, minimumTuple, nettoDivergenceList):
    distance = distanceMatrix[minimumTuple[0]][minimumTuple[1]]
    distance1 = (distance + nettoDivergenceList[minimumTuple[0]] - nettoDivergenceList[minimumTuple[1]]) / 2
    distance2 = (distance + nettoDivergenceList[minimumTuple[1]] - nettoDivergenceList[minimumTuple[0]]) / 2

    nextdistanceMatrix = calculateNextDistanceMatrix(distanceMatrix, minimumTuple)
    distance3 = nextdistanceMatrix[0][1]
    return frozenset({(distance1, minimumElementsAsTuple[0]), (distance2, minimumElementsAsTuple[1]), (distance3, minimumElementsAsTuple[2])})

def calculateNJ(labelGroups, distanceMatrix):
    itemNumber = len(labelGroups)
    currentItemNumber = len(labelGroups)
    while currentItemNumber > 2:

        # labelGroups = [frozenset({label}) for label in labelList]
        nettoDivergenceList = calculateNettoDivergenceList(distanceMatrix)
        minimumTuple = calculateIntermediateMatrix(distanceMatrix, nettoDivergenceList)

        if len(labelGroups) == 3:
            index = list({0,1, 2}.difference({minimumTuple[0], minimumTuple[1]}))[0]
            minimumElementsAsTuple = (labelGroups[minimumTuple[0]], labelGroups[minimumTuple[1]], labelGroups[index])
            mergedGroup = getLastMergedGroup(distanceMatrix, minimumElementsAsTuple, minimumTuple, nettoDivergenceList)
            return getNewickTree(mergedGroup)
        else:
            minimumElementsAsTuple = (labelGroups[minimumTuple[0]], labelGroups[minimumTuple[1]])
            mergedGroup = getMergedGroup(distanceMatrix, minimumElementsAsTuple, minimumTuple, nettoDivergenceList)
            distanceMatrix = calculateNextDistanceMatrix(distanceMatrix, minimumTuple)
            labelGroups = addMergedGroup(labelGroups, mergedGroup)
            labelGroups = eraseGroups(labelGroups, minimumTuple)

            #return calculateNJ(nextLabelGroups, nextdistanceMatrix)
            currentItemNumber = len(labelGroups)
            if currentItemNumber % 10 == 9:
                print(str(itemNumber - currentItemNumber+1) + ' of ' + str(itemNumber))