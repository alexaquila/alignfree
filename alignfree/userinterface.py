MIN_LENGTH = 2
MAX_LENGTH = 50

def getParameter(args):
    # Check if arguments have the correct length
    if len(args) == 4:
        return getParameterFromArgs(args)
    else:
        return getFastaFromUserInput(), getTargetPath(), getKmerLength()

def getParameterFromArgs(args):
    try:
        fastaFile = open(args[1], 'r')
        kmerLength = int(args[3])
        if  kmerLength < MIN_LENGTH or kmerLength > MAX_LENGTH:
                raise Exception(0, 'Kmer-length must be a number between '+
                  str(MIN_LENGTH) + ' and ' +
                  str(MAX_LENGTH))
        return fastaFile, args[2], kmerLength
    except Exception as e:
        print(e.args)
        print('The arguments given do not match the expected values.' +
              '\nError: ' + str(e.args[1]) + '\n' +
              'Please enter: \n' +
              '\t - file path to fasta file\n'+
              '\t - target path\n' +
              '\t - kmer-length.\n' +
              'If no arguments are given, the parameter can bes set interactively.'
              )
        raise SystemExit

def getFastaFromUserInput():
    filePath = None
    fastaFile = None
    while filePath == None:
        try:
            filePath = raw_input('Please enter the path to the fasta file: ')
            fastaFile = open(filePath, 'r')
        except IOError:
            filePath = None
            print('Please enter a valid filepath.')
    return fastaFile


def getTargetPath():
    filePath = None
    while filePath == None:
        try:
            filePath = raw_input('Please enter the path to the target tree file: ')
        except IOError:
            filePath = None
            print('Please enter a valid filepath.')
    return filePath

def getKmerLength():
    kmerLength = 0
    while kmerLength < MIN_LENGTH or kmerLength > MAX_LENGTH:
        try:
            kmerLength = int(raw_input('Please enter the desired kmer-length: '))
            if kmerLength < MIN_LENGTH or kmerLength > MAX_LENGTH:
                raise Exception
        except Exception:
            kmerLength = None
            print('Please enter a number between ' +
                  str(MIN_LENGTH) + ' and ' +
                  str(MAX_LENGTH))
    return kmerLength
