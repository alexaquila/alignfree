import itertools

def getReplacement(baseIdent):
    replacements = {'a':{'a'}, 'c':{'c'}, 'g':{'g'}, 't':{'t'},
                    'y':{'c','t'}, 'r':{'a','g'}, 'm':{'a','c'}, 'w':{'a','t'}, 's':{'g','c'}, 'k':{'g','t'},
                    'h': {'a','c','t'}, 'v': {'a','c','g'}, 'd': {'a','g','t'}, 'b':{'g','c','t'},
                    'n':{'a','c','g','t'}
                    }
    return replacements[baseIdent]

def getMultiples(rawKmer):
    multiples = ()
    for base in rawKmer:
        multiples  += (getReplacement(base),)

    allCombinationsAsTuple = list(itertools.product(*multiples))
    ret = []

    for combination in allCombinationsAsTuple:
        newString = ''
        for base in combination:
            newString += base
        ret += [ (newString, 1.0/len(allCombinationsAsTuple))]
    return ret

def shrinkMultipleKmers(spectrum):
    shrinkedSpectrum = []
    shrinkedSpectrum.append(spectrum[0])
    for kmer in spectrum[1:]:
        if shrinkedSpectrum[-1][0] == kmer[0]:
            shrinkedSpectrum[-1] = kmer[0], kmer[1]+shrinkedSpectrum[-1][1]
        else:
            shrinkedSpectrum.append(kmer)
    return shrinkedSpectrum

def calculateSpectrum(sequence, kmerLength):
    rawKmerList, shrinkedSequence = [], sequence
    while len(shrinkedSequence) >= kmerLength:
        rawKmerList.append(shrinkedSequence[0:kmerLength])
        shrinkedSequence = shrinkedSequence[1:]


    # contains list of dict with entries spectrum and probability
    spectrum = []
    for rawKmer in rawKmerList:

        spectrum += getMultiples(rawKmer)

    # Sort elements by string alphabetically
    spectrum = sorted(spectrum, key=lambda x : x[0])
    # Shrink multiple elements with same sequence to one
    spectrum = shrinkMultipleKmers(spectrum)
    return spectrum

def calculateSpectra(sequences, kmerLength):
    spectra = []
    labelList = []
    for label, sequence in sequences:
        spectra.append(calculateSpectrum(sequence, kmerLength))
        labelList.append(label)
    return labelList, spectra