from Utilities.BasicFunctions import findKey
from BaseClasses.Tonality import Tonality

class Instruments(object):
    def __init__(self, tonality=None, lowestNote = 'C-2', highestNote = 'G8', type = 'Keyboard', role = 'Accompinament', wind = False, channel = 0, track = 0, program = 0):
        
        self.tonality = tonality
        self.checkTonality()
            
        self.lowestNote = lowestNote
        self.highestNote = highestNote
        self.tonality = tonality 
        self.type = type
        self.role = role
        self.wind = wind
        self.channel = channel
        self.track = track
        self.program = program
        
        self.initializeDiatonics()
    
    def checkTonality(self):
        if self.tonality == None:
            self.tonality = Tonality()
            
    def initializeDiatonics(self):
        self.createGrandStaff()
        self.instLowestNoteVal = self.grandStaff[self.lowestNote]
        self.instHighestNoteVal = self.grandStaff[self.highestNote]
        self.findLowestTonic()
        self.createDiatonicMap()
    
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
        while self.instLowestNoteVal > lowestTonicVal:
            lowOct = lowOct + 1
            lowestTonicVal = self.grandStaff[keySig + str(lowOct)]
        
        self.lowestTonic = findKey(self.grandStaff,lowestTonicVal)
                    
    def createDiatonicMap(self):
        self.lowestTonicVal = self.grandStaff[self.lowestTonic]
        self.diatonicRange = {}
        self.diatonicList = []
        diatonicScale = []
        self.octaveList = []
        noteValue = self.lowestTonicVal
        noteCtr = 0
        octCtr = 0
        
        if self.lowestTonicVal > self.instLowestNoteVal - 1:
            noteCtr = -1
            octCtr = -1
            noteValue = self.lowestTonicVal
            tonalNote = self.tonality.chromatics[0] + 12*octCtr + self.lowestTonicVal
            self.diatonicRange[(findKey(self.grandStaff,tonalNote))] = []
            self.octaveList.append(tonalNote)
            for diatonics, item in enumerate(self.tonality.chromatics):
                noteValue = self.tonality.chromatics[diatonics] + 12*octCtr + self.lowestTonicVal
                if noteValue < self.instLowestNoteVal:
                    pass
                else:
                    self.diatonicList.append(noteValue)
                    self.diatonicRange[(findKey(self.grandStaff,tonalNote))].append(noteValue)
                noteCtr += 1
            diatonicScale = []
            octCtr += 1

        while noteValue <= self.instHighestNoteVal:
            tonalNote = self.tonality.chromatics[0] + 12*octCtr + self.lowestTonicVal
            self.diatonicRange[(findKey(self.grandStaff,tonalNote))] = []
            self.octaveList.append(tonalNote)
            for diatonics, item in enumerate(self.tonality.chromatics):
                noteValue = self.tonality.chromatics[diatonics] + 12*octCtr + self.lowestTonicVal
                if noteValue > self.instHighestNoteVal:
                    break
                self.diatonicList.append(noteValue)
                self.diatonicRange[(findKey(self.grandStaff,tonalNote))].append(noteValue)
                noteCtr += 1
            diatonicScale = []
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
    def __init__(self, tonality=None, channel=0, track=0):
        self.tonality = tonality
        super(Flute,self).checkTonality()

        self.lowestNote = 'C4'
        self.highestNote = 'D7'
        self.type = 'Woodwind'
        self.role = 'Solo'
        self.wind = True
        self.channel = channel
        self.track = track
        self.program = 73

        super(Flute,self).initializeDiatonics()
        
class Clarinet(Instruments):
    def __init__(self, tonality=None, channel=0, track=0):
        self.tonality = tonality
        super(Clarinet,self).checkTonality()

        self.lowestNote = 'E3'
        self.highestNote = 'C7'
        self.type = 'Woodwind'
        self.role = 'Solo'
        self.wind = True
        self.channel = channel
        self.track = track
        self.program = 71

        super(Clarinet,self).initializeDiatonics()
         

class Trumpet(Instruments):
    def __init__(self, tonality=None, channel=0, track=0):
        self.tonality = tonality
        super(Trumpet,self).checkTonality()
        
        self.lowestNote = 'F#3'
        self.highestNote = 'D6'
        self.type = 'Brass'
        self.role = 'Solo'
        self.wind = True
        self.channel = channel
        self.track = track
        self.program = 56
      
        super(Trumpet,self).initializeDiatonics()
      
class Tuba(Instruments):
    def __init__(self, tonality=None, channel=0, track=0):
        self.tonality = tonality
        super(Tuba,self).checkTonality()
        
        self.lowestNote = 'D1'
        self.highestNote = 'F4'
        self.type = 'Brass'
        self.role = 'Bass'
        self.wind = True
        self.channel = channel
        self.track = track
        self.program = 58
        
        super(Tuba,self).initializeDiatonics()
