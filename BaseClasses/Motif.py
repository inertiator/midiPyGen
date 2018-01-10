import random
from copy import deepcopy
from BaseClasses.ChordProgression import ChordProgression

class Motif(object):
    def __init__(self, beatsPerChord, length, timeMeter, tonality, instDict, chordSlice, inpMotif=None):
        self.length = length
        self.timeMeter = timeMeter
        self.beatsPerChord = beatsPerChord
        self.beats = self.length*self.beatsPerChord
        self.instDict = instDict
        self.tonality = tonality
        self.chordSlice = chordSlice
        self.inpMotif = inpMotif
        self.timeArr = []
        self.diatArr = []
        self.diatList = []
        self.analyzeChord()
        
    def createSubdivisions(self):
        notional = [0.5,1,1.5,2,3,4,6]
        self.subDiv = []
        for i in notional:
            if i > self.timeMeter.numBeatsPerMeasure:
                break
            else:
                self.subDiv.append(i)
        
    def analyzeChord(self):
        self.chordProg = ChordProgression(self.chordSlice, self.tonality, self.instDict)
        self.chordProg.setupOrderOfRangeMB()
        self.chordProg.prog = self.chordSlice
        for iChord, chord in enumerate(self.chordProg.prog):            
            self.diatList.append(self.chordProg.getDiatList(iChord,chord))
                
    def generateMotifDiats(self):
        motD = []
        for chord in self.diatList:
            randDiatIdx = random.randint(0,len(chord)-1)
            motD.append(chord[randDiatIdx])
        return motD
        
    def generateRandomRhythms(self):
        ryt = []
        self.subMot = self.beats/4
        while sum(ryt) is not self.subMot:
            randIdx = random.randint(0,len(self.subDiv)-1)
            ryt.append(self.subDiv[randIdx])
            if sum(ryt) > self.subMot:
                randIdx = random.randint(0,len(ryt)-1)
                del ryt[randIdx]
            elif sum(ryt) == self.subMot:
                break
        return ryt
    
    def combineRandomRhythms(self):
        first = self.generateRandomRhythms()
        second = self.generateRandomRhythms()
        rytTot = first + second + first + second
        return rytTot 
        
    def createRandomFill(self,motD,rytTot):
        bCtr = 0
        motTot = []
        dCtr = 0
        for i,ryt in enumerate(rytTot):
            if i == 0 or bCtr == self.beatsPerChord:
                bCtr = 0
                motTot.append(motD[dCtr])
                dCtr += 1
            else:
                switch = 0
                while switch == 0:
                    randDiat = random.randint(1,7)
                    if abs(randDiat - motTot[i-1]) < 5:
                        motTot.append(randDiat)
                        switch = 1
            bCtr += ryt
        return motTot
            
    def createConsMotif(self):
        self.motTot = deepcopy(self.inpMotif.motTot)
        self.rytTot = deepcopy(self.inpMotif.rytTot)
        bCtr = 0
        switch = 0
        for i,ryt in enumerate(self.rytTot):
            if (sum(self.rytTot) - bCtr) == self.beatsPerChord:
                self.motTot[i] = self.motTot[i]
                self.rytTot[i] = 4
                endIdx = i
            bCtr += ryt
        self.motTot = self.motTot[:endIdx+1]
        self.rytTot = self.rytTot[:endIdx+1]
        
        
        
    def createMotifFromChords(self):
        print('Creating Motif...')
        print('Total measures is: ' + str(self.length))
        self.createSubdivisions()
        self.motD = self.generateMotifDiats()
        self.rytTot = self.combineRandomRhythms()
        self.motTot = self.createRandomFill(self.motD,self.rytTot)
        
    
class Period(object):
    def __init__(self, beatsPerChord, timeMeter, tonality, chordProg, measures, instDict):
        self.timeMeter = timeMeter
        self.beatsPerChord = beatsPerChord
        self.tonality = tonality
        self.chordProg = chordProg
        self.measures = measures
        self.instDict = instDict
        self.progNum = {}
        self.progVal = {}
        self.diatTol = 3
        
        
    def fillMelodyVals(self):
        iChord = 0
        print('\nMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM\nFilling in values for melody...')
        for inst,instKey in enumerate(self.instDict):
            self.progNum[instKey] = []
            self.progVal[instKey] = []
            for iMot,mot in enumerate(self.motPeriod):
                if iMot == 0 or bCtr == self.beatsPerChord:
                    bCtr = 0
                    chord = self.chordProg[iChord]
                    newInstDict = {}
                    newInstDict[instKey] = deepcopy(self.instDict[instKey])
                    self.nextChord = ChordProgression(chord, self.tonality, newInstDict)
                    self.nextChord.setupOrderOfRangeMB()
                    self.nextChord.prog = self.chordProg[iChord]
                    self.nextChord.inv = [None]
                    diatList = self.nextChord.getDiatList(0,chord)
                    iChord += 1
                if iMot == 0:
                    totalRange = len(self.nextChord.instDict[instKey].diatonicListVal)
                    halfRange = int(totalRange/2)
                    halfNum = self.nextChord.instDict[instKey].diatonicListNum[halfRange]
                    halfVal = self.nextChord.instDict[instKey].diatonicListVal[halfRange]
                    meloNum = self.motPeriod[iMot]
                    dNum = meloNum - halfNum
                    if dNum < -self.diatTol:
                        dNum = 7 + dNum
                    elif dNum > self.diatTol:
                        dNum = dNum - 7
                    self.progNum[instKey].append(self.nextChord.instDict[instKey].diatonicListNum[halfRange + dNum])
                    self.progVal[instKey].append(self.nextChord.instDict[instKey].diatonicListVal[halfRange + dNum])
                else:
                    previousPartVal = self.progVal[instKey][iMot-1]
                    previousPartIdx = min(range(len(self.nextChord.instDict[instKey].diatonicListVal)), key=lambda i: abs(self.nextChord.instDict[instKey].diatonicListVal[i]-previousPartVal))
                    previousPartNum = self.nextChord.instDict[instKey].diatonicListNum[previousPartIdx]
                    meloNum = self.motPeriod[iMot]
                    dNum = meloNum - previousPartNum
                    if dNum < -self.diatTol:
                        dNum = 7 + dNum
                    elif dNum > self.diatTol:
                        dNum = dNum - 7
                    tempNewVal = self.nextChord.instDict[instKey].diatonicListVal[previousPartIdx + dNum]
                    tempNewIdx = self.nextChord.instDict[instKey].diatonicListVal.index(tempNewVal)
                    dChordValFC = tempNewVal - self.progVal[instKey][0] 
                    self.progNum[instKey].append(self.nextChord.instDict[instKey].diatonicListNum[previousPartIdx + dNum])
                    self.progVal[instKey].append(self.nextChord.instDict[instKey].diatonicListVal[previousPartIdx + dNum])
                bCtr += self.rytPeriod[iMot]
        
    def createAntecedentConsequent(self):
        self.motifLength = int(self.measures/2)
        self.antChord = self.chordProg[0:self.motifLength]
        self.conChord = self.chordProg[self.motifLength-1:]
        
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nCreating motif for antecedent...')
        ant = Motif(self.beatsPerChord,self.motifLength,self.timeMeter,self.tonality,self.instDict, self.antChord)
        self.ant = ant
        self.ant.createMotifFromChords()
        
        print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\nCreating motif for consequent...')
        cons = Motif(self.beatsPerChord,self.motifLength,self.timeMeter,self.tonality,self.instDict, self.antChord, ant)
        self.cons = cons
        self.cons.createConsMotif()
        
        self.motPeriod = self.ant.motTot + self.cons.motTot
        self.rytPeriod = self.ant.rytTot + self.cons.rytTot
        self.dTime = self.rytPeriod
        self.fillMelodyVals()
        
            
        
        





