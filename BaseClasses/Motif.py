import random
from copy import deepcopy
from BaseClasses.ChordProgression import ChordProgression

class Motif(object):
    def __init__(self, length, timeMeter, tonality, instDict, chordSlice, inpMotif=None):
        self.length = length
        self.timeMeter = timeMeter
        self.instDict = instDict
        self.tonality = tonality
        self.chordSlice = chordSlice
        self.timeArr = []
        self.diatArr = []
        self.diatList = []
        self.analyzeChord()
        
    def analyzeChord(self):
        self.chordProg = ChordProgression(self.chordSlice, self.tonality, self.instDict)
        self.chordProg.prog = self.chordSlice
        for iChord, chord in enumerate(self.chordProg.prog):            
            self.diatList.append(self.chordProg.getDiatList(iChord,chord))
                
    def generateRandomMotifs(self):
        pass
        
    def createMotifFromChords(self):
        print('Creating Motif...')
        print('Total measures is: ' + str(self.length))
    
class Period(object):
    def __init__(self, timeMeter, tonality, chordProg, measures, instDict):
        self.timeMeter = timeMeter
        self.tonality = tonality
        self.chordProg = chordProg
        self.measures = measures
        self.instDict = instDict
        self.progNum = {}
        self.progVal = {}
        
        
    def createAntecedentConsequent(self):
        self.motifLength = int(self.measures/2)
        self.antChord = self.chordProg[0:self.motifLength]
        self.conChord = self.chordProg[self.motifLength-1:]
        
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nCreating motif for antecedent...')
        ant = Motif(self.motifLength,self.timeMeter,self.tonality,self.instDict, self.antChord)
        self.ant = ant
        self.ant.createMotifFromChords()
        
        print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\nCreating motif for consequent...')
        cons = Motif(self.motifLength,self.timeMeter,self.tonality,self.instDict, self.antChord, ant)
        self.cons = cons
        self.cons.createMotifFromChords()
        
            
        
        





