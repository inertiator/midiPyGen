

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
        
    def obtainChromatics(self):
        if self.tonalMode == 'Major':
            self.chromatics = [0,2,4,5,7,9,11]
        elif self.tonalMode == 'Minor':
            self.chromatics = [0,2,3,5,7,8,10]
        else:
            raise ValueError('ERROR: Tonality \'' + self.tonalMode + '\' not recognized!')
    
    def sharpifyKeySig(self):
        enharmonicDict = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
        if self.keySig in enharmonicDict:
            self.keySig = enharmonicDict[self.keySig]
        
    def obtainBorrowedChords():
       pass 
        
    