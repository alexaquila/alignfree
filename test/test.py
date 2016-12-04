import unittest

from alignfree.fastafileopener import validateSequence


class TestParserFunctions(unittest.TestCase):
    def setUp(self):
        self.failfasta = ('name', 'ATCGA/ATCGAacgtnyrmwskhvdb')
        self.goodfasta = ('name', 'ATCGAacgtnyrmwskhvdb')

    def test_failWhenUnknownCharacter(self):
        self.assertRaises(ValueError, self.unknownCharacter)

    def unknownCharacter(self):
        validateSequence(self.failfasta[1])
    def test_doNotFailWithKnownCharacters(self):
        try:
            validateSequence(self.goodfasta[1])
        except ValueError:
            self.fail('Raising ValueError for no reason')

from alignfree.spectracalculator import getMultiples, getReplacement, shrinkMultipleKmers

class TestSpectraFunctions(unittest.TestCase):
    def setUp(self):
        self.kmer = ('atcga')
        self.kmerWierd = ('anvgy')
        self.kmerVeryWierd = ('nnnnn')
        self.spectrumToReduce = [('aaa', 1.0), ('aaa', 1.0), ('aaa', 1.2), ('aat', 1.0)]
        self.spectrumReduced = [('aaa', 3.2), ('aat', 1.0)]

    def test_dict(self):
        assert getReplacement('n') == {'a','c','g','t'}
        self.assertRaises(Exception, self.getReplacement)

    def getReplacement(self):
        getReplacement('f')

    def test_combinations(self):
        multiples1 = getMultiples(self.kmer)
        multiples2 = getMultiples(self.kmerWierd)
        multiples3 = getMultiples(self.kmerVeryWierd)

        assert len(multiples1) == 1
        assert len(multiples2) == 4*3*2
        assert len(multiples3) == 4*4*4*4*4

    def test_multipleKmerReduction(self):
        assert shrinkMultipleKmers(self.spectrumToReduce) == self.spectrumReduced


from alignfree.distancematrix import getDistanceMatrix, multiplicationVector

class TestDistanceMatrixFunctions(unittest.TestCase):
    def setUp(self):
        self.spectraReduced1 = [('aaa', 3.2), ('aat', 1.0), ('ttt', 4.0)]
        self.spectraReduced2 = [('aaa', 3.2), ('act', 1.0),('aga', 1.0), ('ttt', 2.0)]

    def test_multilpication(self):
        weight1 = multiplicationVector(self.spectraReduced1, self.spectraReduced2)
        weight2 = multiplicationVector(self.spectraReduced1, self.spectraReduced2)

        assert weight1 == weight2
        assert weight1 == 3.2*3.2 + 4.0*2.0


from alignfree.neighborjoining import calculateNettoDivergenceList, calculateIntermediateMatrix, eraseGroups, \
    getMergedGroup, calculateNextDistanceMatrix

class TestNJ(unittest.TestCase):
    def setUp(self):
        # Example from https://de.wikipedia.org/wiki/Neighbor-Joining-Algorithmus
        self.distMatrix = [[0.0, 3.0, 14.0, 12.0],
                           [3.0, 0.0, 13.0, 11.0],
                           [14.0, 13.0, 0.0, 4.0],
                           [12.0, 11.0, 4.0, 0.0]]
        self.labelList = ['Mensch', 'Maus', 'Rose','Tulpe' ]
        self.labelGroups =  list(map(lambda x : frozenset({x}),  self.labelList))
        self.erasedLabelGroups = list(map(frozenset, [{'Rose'}, {'Tulpe'} ]))

        self.nextLabelGroups = list(map(frozenset, [{'Rose'}, {'Tulpe'} ,{ frozenset({'Mensch'}), frozenset({'Maus'})}]))
        self.firstDivergence = [14.5 , 13.5, 15.5, 13.5]
        self.firstIntermediateMatrix = [[0.0, -25.0, -16.0, -16.0],
                                       [0.0, 0.0, -16.0, -16.0],
                                       [0.0, 0.0, 0.0, -25.0],
                                       [0.0, 0.0, 0.0, 0.0]]
        self.smallestTuple = (0,1)
        self.smallestFirst, self.smallestSec = self.labelGroups[0], self.labelGroups[1]
        self.firstMergedGroup = frozenset({
                                            (2.0, frozenset({'Mensch'})) ,
                                            (1.0, frozenset({'Maus'}))})

        self.nextDistMatrix = [[0.0, 4.0, 12.0],
                               [4.0, 0.0, 10.0],
                               [12.0, 10.0, 0.0]]

    def test_nettoDivergence(self):
        assert calculateNettoDivergenceList(self.distMatrix) == self.firstDivergence

    def test_intermediateMatrix(self):
        assert calculateIntermediateMatrix(self.distMatrix, self.firstDivergence) == self.smallestTuple

    def test_eraseGroups(self):
        erased = eraseGroups( self.labelGroups, self.smallestTuple)
        assert erased == self.erasedLabelGroups


    def test_getMergedGroup(self):
        merged = getMergedGroup(self.distMatrix, (self.smallestFirst, self.smallestSec), self.smallestTuple, self.firstDivergence)
        assert merged == self.firstMergedGroup


    def test_calulateNextDistanceMatrix(self):
        nextDistMatrix = calculateNextDistanceMatrix(self.distMatrix, self.smallestTuple)
        assert nextDistMatrix == self.nextDistMatrix

if __name__ == '__main__':
    unittest.main()
