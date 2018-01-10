from Utilities.BasicFunctions import findKey


class Tonality(object):
    def __init__(self, keySig = 'C', tonalMode = 'Major'):
        '''
        Every song of practically every genre is made is made up of a tonality.
        This class is inherited by the instruments and forms the basis of their diatonic range.
        ------------------------------------------------
        INPUT       TYPE    DESCRIPTION
        ------------------------------------------------
        keySig      string  Key of this song in (ABCDEFG and in Sharps or Flats). 
                            This code will always assume sharps for simplicity.
        tonalMode   string  Type of mode of this song, e.g. Major, Minor, Dorian, etc
        '''
        self.keySig = keySig
        self.sharpifyKeySig()
        self.tonalMode = tonalMode
        self.obtainChromatics()
        self.createGrandStaff()
        self.lowestNote = 'A0'
        self.highestNote = 'C8'
        self.lowestNoteVal = self.grandStaff[self.lowestNote]
        self.highestNoteVal = self.grandStaff[self.highestNote]
        self.findLowestTonic()
        self.createDiatonicMap()
        self.maxDiatonicListVal = max(self.diatonicListVal)
        
    def obtainChromatics(self):
        '''
        In a pure chromatic sense, this function determines diatonic values for each scale.
        A fundamental concept, this is highly needed to link diatonic scale degrees with their chromatic counterparts.
        Ex: [0,2,4,5,7,9,11] in Chromatic will be [1,2,3,4,5,6,7] in Diatonic
        Currently have major and minor, but can be extended to Dorian, Lydian, Phrygian, etc.
        '''
        if self.tonalMode == 'Major':
            self.chromatics = [0,2,4,5,7,9,11]
        elif self.tonalMode == 'Minor':
            self.chromatics = [0,2,3,5,7,8,10]
        else:
            raise ValueError('ERROR: Tonality \'' + self.tonalMode + '\' not recognized!')
    
    def sharpifyKeySig(self):
        '''
        midiPyGen works off of a pure sharp system. SORRY MUSIC PEOPLE, THIS IS JUST HOW IT ENDED UP :( 
        User is still able to input a flat key signature but this function converts it to sharps.
        '''
        enharmonicDict = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
        if self.keySig in enharmonicDict:
            self.keySig = enharmonicDict[self.keySig]

    def createGrandStaff(self):
        '''
        This function creates a grand staff (also seen in Instruments))
        Grand Staff creates a dictionary for a value for each pitch in the 128 available MIDI values 
        Octaves are represented by numbers after noteLetters, e.g. C0, E4
        '''
        self.grandStaff = {};
        stfCtr = 0
        noteLetters = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        noteOctaves = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
        noteDiatonics = [1, 2, 3, 4, 5, 6, 7]

        for octaves in noteOctaves:
            for letters in noteLetters:
                self.grandStaff[str(letters)+str(octaves)] = stfCtr
                stfCtr += 1
                if stfCtr >= 128:
                    break        
    
    def createDiatonicMap(self):
        '''
        This function takes the grand staff and combines it with the highest and lowest values.
        The final products are:
        self.diatonicListVal: A list of the entire range of diatonic chromatic values (absolute MIDI pitches) for this instrument (or in grand total if inside Tonality.py)
        self.diatonicListNum: A list of the entire range of diatonic degree numbers for this instrument (or in grand total if inside Tonality.py)
        self.diatonicRangeVal: Dictionary of the diatonic chromatic values with the keySignature as keys (rarely Used)
        self.diatonicRangeNum: Dictionary of the diatonic degree numbers with the keySignature as keys (rarely Used)
        '''
        self.lowestTonicVal = self.grandStaff[self.lowestTonic]
        self.diatonicRangeVal = {}
        self.diatonicListVal = []
        self.diatonicRangeNum = {}
        self.diatonicListNum = []
        self.octaveList = []
        noteValue = self.lowestTonicVal
        noteCtr = 0
        octCtr = 0
        
        if self.lowestTonicVal > self.lowestNoteVal:
            noteCtr = -1
            octCtr = -1
            noteValue = self.lowestTonicVal
            tonalNote = self.chromatics[0] + 12*octCtr + self.lowestTonicVal
            self.diatonicRangeVal[(findKey(self.grandStaff,tonalNote))] = []
            self.diatonicRangeNum[(findKey(self.grandStaff,tonalNote))] = []
            self.octaveList.append(tonalNote)
            
            for diatonics, item in enumerate(self.chromatics):
                noteValue = self.chromatics[diatonics] + 12*octCtr + self.lowestTonicVal
                if noteValue < self.lowestNoteVal:
                    pass
                else:
                    self.diatonicListVal.append(noteValue)
                    self.diatonicListNum.append(diatonics + 1)
                    self.diatonicRangeVal[(findKey(self.grandStaff,tonalNote))].append(noteValue)
                    self.diatonicRangeNum[(findKey(self.grandStaff,tonalNote))].append(diatonics + 1)
                noteCtr += 1
            octCtr += 1

        while noteValue <= self.highestNoteVal:
            tonalNote = self.chromatics[0] + 12*octCtr + self.lowestTonicVal
            self.diatonicRangeVal[(findKey(self.grandStaff,tonalNote))] = []
            self.diatonicRangeNum[(findKey(self.grandStaff,tonalNote))] = []
            self.octaveList.append(tonalNote)
            
            for diatonics, item in enumerate(self.chromatics):
                noteValue = self.chromatics[diatonics] + 12*octCtr + self.lowestTonicVal
                if noteValue > self.highestNoteVal:
                    break
                self.diatonicListVal.append(noteValue)
                self.diatonicListNum.append(diatonics + 1)
                self.diatonicRangeVal[(findKey(self.grandStaff,tonalNote))].append(noteValue)
                self.diatonicRangeNum[(findKey(self.grandStaff,tonalNote))].append(diatonics + 1)
                noteCtr += 1
            octCtr += 1
    
    def findLowestTonic(self):
        '''
        Given an instrument (or entire range if inside Tonality.py), find the lowest tonic within its range
        '''
        lowOct = -2
        keySig = self.keySig
        absLowestTonicVal = self.grandStaff[keySig + str(lowOct)]
        self.lowestTonicVal = absLowestTonicVal
        while self.lowestNoteVal > self.lowestTonicVal:
            lowOct = lowOct + 1
            self.lowestTonicVal = self.grandStaff[keySig + str(lowOct)]
        
        self.lowestTonic = findKey(self.grandStaff,self.lowestTonicVal)
        
        
    def findBorrowedKey(self,borrowedRoot):
        '''
        To spice up some chord progressions, people have been borrowing chords for centuries.
        A borrowed chord is essentially a diatonic chord taken from a different key.
        In roman numerals they're usually shown like as follows: Chord-->V/V<--Key. First number is the chord, second number is the key that the chord is borrowing from.
        (Ex. If we're in the key of C, the key diatonic is 5 is G. In the new key (G), the 5th diatonic is D, which means the resulting chord is D)
        This function takes in the borrowedKey diatonic and converts it to a key signature for the Tonality class to use
        ------------------------------------------------
        INPUT           TYPE     DESCRIPTION
        ------------------------------------------------
        borrowedRoot    int     Root of borrowed key as a diatonic from the home key, the number after the slash in a borrowed chord
                                e.g. (If in an C major song, we're borrowing a chord from F major, the borrowedRoot would be 4 
        ------------------------------------------------
        OUTPUT          TYPE    DESCRIPTION
        ------------------------------------------------
        newKey          string  Borrowed Key Signature        
        '''
        diat = borrowedRoot
        diatIdx = diat - 1
        borrowedVal = self.lowestTonicVal + self.chromatics[diatIdx]
        newKeyLong = findKey(self.grandStaff,borrowedVal)
        if newKeyLong[1] == '#':
            newKeyShort = newKeyLong[0:2]
        else:
            newKeyShort = newKeyLong[0]
        return newKeyShort
        
        
        
        