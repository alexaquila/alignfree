
def validateSequence(sequence):
    allowedCharacters = {'a','c','g','t','n','y','r','m','w','s','k','h','v','d','b'}
    sequence = sequence.lower()
    for base in sequence:
        if not base in allowedCharacters:
            raise ValueError("illegal character in sequence: " + base)
    return sequence

def parseFasta(fastaFile):
    sequences = []
    currentSequence, currentLabel = '', ''
    for line in  fastaFile:
        stripedLine = line.strip()
        # If it begins with a '>', accept line as the label
        if stripedLine.startswith('>'):
            # Write previous label and sequence to sequences
            if not currentSequence == '':
                validatedSequence = validateSequence(currentSequence)
                sequences.append((currentLabel, validatedSequence))
                currentSequence = ''
            # Get new label
            currentLabel = stripedLine[1:-1]
        elif stripedLine.startswith (';'):
            continue
        else:
            currentSequence += stripedLine
    # Append last element
    if not currentLabel == '':
        validatedSequence = validateSequence(currentSequence)
        sequences.append((currentLabel, validatedSequence))
    return sequences