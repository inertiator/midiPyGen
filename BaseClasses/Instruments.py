from Utilities.BasicFunctions import findKey
from BaseClasses.Tonality import Tonality

class Instruments(object):
    def __init__(self, tonality=None, lowestNote = 'C-2', highestNote = 'G8', type = 'Keyboard', role = 'Accompinament', wind = False, track = 0, program = 0):
        
        self.tonality = tonality
        self.checkTonality()
            
        self.lowestNote = lowestNote
        self.highestNote = highestNote
        self.tonality = tonality 
        self.type = type
        self.role = role
        self.wind = wind
        self.track = track
        self.program = program
        
        self.initializeDiatonics()

    def checkTonality(self):
        if self.tonality == None:
            self.tonality = Tonality()
            
    def initializeDiatonics(self):
        self.createGrandStaff()
        self.lowestNoteVal = self.grandStaff[self.lowestNote]
        self.highestNoteVal = self.grandStaff[self.highestNote]
        self.findLowestTonic()
        self.createDiatonicMap()
        self.maxDiatonicListVal = max(self.diatonicListVal)

    def createGrandStaff(self):
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
    
    def findLowestTonic(self):
        lowOct = -2
        keySig = self.tonality.keySig
        absLowestTonicVal = self.grandStaff[keySig + str(lowOct)]
        lowestTonicVal = absLowestTonicVal
        while self.lowestNoteVal > lowestTonicVal:
            lowOct = lowOct + 1
            lowestTonicVal = self.grandStaff[keySig + str(lowOct)]
        
        self.lowestTonic = findKey(self.grandStaff,lowestTonicVal)
                    
    def createDiatonicMap(self):
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
            tonalNote = self.tonality.chromatics[0] + 12*octCtr + self.lowestTonicVal
            self.diatonicRangeVal[(findKey(self.grandStaff,tonalNote))] = []
            self.diatonicRangeNum[(findKey(self.grandStaff,tonalNote))] = []
            self.octaveList.append(tonalNote)
            
            for diatonics, item in enumerate(self.tonality.chromatics):
                noteValue = self.tonality.chromatics[diatonics] + 12*octCtr + self.lowestTonicVal
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
            tonalNote = self.tonality.chromatics[0] + 12*octCtr + self.lowestTonicVal
            self.diatonicRangeVal[(findKey(self.grandStaff,tonalNote))] = []
            self.diatonicRangeNum[(findKey(self.grandStaff,tonalNote))] = []
            self.octaveList.append(tonalNote)
            
            for diatonics, item in enumerate(self.tonality.chromatics):
                noteValue = self.tonality.chromatics[diatonics] + 12*octCtr + self.lowestTonicVal
                if noteValue > self.highestNoteVal:
                    break
                self.diatonicListVal.append(noteValue)
                self.diatonicListNum.append(diatonics + 1)
                self.diatonicRangeVal[(findKey(self.grandStaff,tonalNote))].append(noteValue)
                self.diatonicRangeNum[(findKey(self.grandStaff,tonalNote))].append(diatonics + 1)
                noteCtr += 1
            octCtr += 1
        
        
   
class AcousticGrandPiano(Instruments):
    def __init__(self,numParts):
        self.lowestNote = 'A0'
        self.highestNote = 'C8'
        self.type = 'Keyboard'
        self.role = 'Accompinament'
        self.wind = False
        self.program = 0
        self.numParts = numParts
        

            
        
class Flute(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Flute,self).checkTonality()

        self.lowestNote = 'C3'
        self.highestNote = 'D6'
        self.type = 'Woodwind'
        self.role = 'Solo'
        self.wind = True
        self.bass = False
        self.track = track
        self.program = 73

        super(Flute,self).initializeDiatonics()
        
class Clarinet(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Clarinet,self).checkTonality()

        self.lowestNote = 'E2'
        self.highestNote = 'C6'
        self.type = 'Woodwind'
        self.role = 'Solo'
        self.wind = True
        self.bass = False
        self.track = track
        self.program = 71

        super(Clarinet,self).initializeDiatonics()
         

class Trumpet(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Trumpet,self).checkTonality()
        
        self.lowestNote = 'F#2'
        self.highestNote = 'D5'
        self.type = 'Brass'
        self.role = 'Solo'
        self.wind = True
        self.bass = False
        self.track = track
        self.program = 56
      
        super(Trumpet,self).initializeDiatonics()
        
class Violin(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Violin,self).checkTonality()
        
        self.lowestNote = 'G2'
        self.highestNote = 'A5'
        self.type = 'Strings'
        self.role = 'Solo'
        self.wind = False
        self.bass = False
        self.track = track
        self.program = 41
      
        super(Violin,self).initializeDiatonics()
        
class Tuba(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Tuba,self).checkTonality()
        
        self.lowestNote = 'F0'
        self.highestNote = 'F3'
        self.type = 'Brass'
        self.role = 'Bass'
        self.wind = True
        self.bass = True
        self.track = track
        self.program = 58
        
        super(Tuba,self).initializeDiatonics()

class Soprano(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Soprano,self).checkTonality()
        
        self.lowestNote = 'C3'
        self.highestNote = 'B4'
        self.type = 'Voice'
        self.role = 'Solo'
        self.wind = True
        self.bass = False
        self.track = track
        self.program = 54
      
        super(Soprano,self).initializeDiatonics()

class Alto(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Alto,self).checkTonality()
        
        self.lowestNote = 'G2'
        self.highestNote = 'F4'
        self.type = 'Voice'
        self.role = 'Solo'
        self.wind = True
        self.bass = False
        self.track = track
        self.program = 54
      
        super(Alto,self).initializeDiatonics()
        
class Tenor(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Tenor,self).checkTonality()
        
        self.lowestNote = 'C2'
        self.highestNote = 'A3'
        self.type = 'Voice'
        self.role = 'Solo'
        self.wind = True
        self.bass = False
        self.track = track
        self.program = 54
      
        super(Tenor,self).initializeDiatonics()
        
class Bass(Instruments):
    def __init__(self, tonality=None, track=0):
        self.tonality = tonality
        super(Bass,self).checkTonality()
        
        self.lowestNote = 'C1'
        self.highestNote = 'E3'
        self.type = 'Voice'
        self.role = 'Solo'
        self.wind = True
        self.bass = True
        self.track = track
        self.program = 54
      
        super(Bass,self).initializeDiatonics()