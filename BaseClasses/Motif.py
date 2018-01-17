import random
import math
import operator
from copy import deepcopy
from BaseClasses.ChordProgression import ChordProgression
from Utilities.BasicFunctions import findKey

class Motif(object):
    def __init__(self, beatsPerChord, length, timeMeter, tonality, instDict, chordSlice, diatTol, inpMotif=None):
        self.length = length
        self.timeMeter = timeMeter
        self.beatsPerChord = beatsPerChord
        self.beats = self.length*self.beatsPerChord
        self.instDict = instDict
        self.tonality = tonality
        self.chordSlice = chordSlice
        self.inpMotif = inpMotif
        self.diatTol = diatTol
        self.timeArr = []
        self.diatArr = []
        self.diatList = []
        self.analyzeChord()
        
    def createSubdivisions(self):
        notional = [0.5,1,1.5,2,3,4,6]
        self.subDiv = []
        for i in notional:
            if i > self.timeMeter.numBeatsPerMeasure-1:
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
        rI = random.randint(0,3)
        if rI == 0:
            rytTot = first + second + first + second
        elif rI == 1:
            rytTot = first + first + second + second
        elif rI == 2:
            rytTot = second + first + second + first
        elif rI == 3:
            rytTot = second + second + first + first
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
                self.rytTot[i] = self.beatsPerChord
                endIdx = i
                break
            bCtr += ryt
        self.motTot = self.motTot[:endIdx+1]
        self.rytTot = self.rytTot[:endIdx+1]
        
    def generateRandomMotif(self):
        motD = self.generateMotifDiats()
        rytTot = self.combineRandomRhythms()
        motTot = self.createRandomFill(motD,rytTot)
        return motTot, rytTot
        
    def generatePopulation(self,sizePopulation):
        population = []
        i = 0
        while i < sizePopulation:
            population.append(self.generateRandomMotif())
            i += 1
        return population
        
    def computePerfPopulation(self,population):
        populationPerf = {}
        for i,individual in enumerate(population):
            populationPerf[i] = self.findFitness(individual)
        return sorted(populationPerf.items(), key=operator.itemgetter(1))
        
    def findFitness(self, individual):
        
        motTot = individual[0]
        rytTot = individual[1]
        dNum = []
        dChordValFC = []
        progVal = {}
        for iC,chord in enumerate(motTot):
            dNum.append(0)
            dChordValFC.append(0)
        iChord = 0
        for inst,instKey in enumerate(self.instDict):
            progVal[instKey] = []
            for iMot,mot in enumerate(motTot):
                if iMot == 0 or bCtr == self.beatsPerChord:
                    bCtr = 0
                    chord = self.chordProg.prog[iChord]
                    newInstDict = {}
                    newInstDict[instKey] = deepcopy(self.instDict[instKey])
                    self.nextChord = ChordProgression(chord, self.tonality, newInstDict)
                    self.nextChord.setupOrderOfRangeMB()
                    self.nextChord.prog = chord
                    self.nextChord.inv = [None]
                    diatList = self.nextChord.getDiatList(0,chord,vb=0)
                    iChord += 1
                if iMot == 0:
                    totalRange = len(self.nextChord.instDict[instKey].diatonicListVal)
                    halfRange = int(totalRange/2)
                    halfNum = self.nextChord.instDict[instKey].diatonicListNum[halfRange]
                    halfVal = self.nextChord.instDict[instKey].diatonicListVal[halfRange]
                    meloNum = motTot[iMot]
                    dNum[iMot] = meloNum - halfNum
                    if dNum[iMot] < -self.diatTol:
                        dNum[iMot] = 7 + dNum[iMot]
                    elif dNum[iMot] > self.diatTol:
                        dNum[iMot] = dNum[iMot] - 7
                    progVal[instKey].append(self.nextChord.instDict[instKey].diatonicListVal[halfRange + dNum[iMot]])
                else:
                    previousPartVal = progVal[instKey][iMot-1]
                    previousPartIdx = min(range(len(self.nextChord.instDict[instKey].diatonicListVal)), key=lambda i: abs(self.nextChord.instDict[instKey].diatonicListVal[i]-previousPartVal))
                    previousPartNum = self.nextChord.instDict[instKey].diatonicListNum[previousPartIdx]
                    meloNum = motTot[iMot]
                    dNum[iMot] = meloNum - previousPartNum
                    if dNum[iMot] < -self.diatTol:
                        dNum[iMot] = 7 + dNum[iMot]
                    elif dNum[iMot] > self.diatTol:
                        dNum[iMot] = dNum[iMot] - 7
                    try:
                        tempNewVal = self.nextChord.instDict[instKey].diatonicListVal[previousPartIdx + dNum[iMot]]
                        progVal[instKey].append(tempNewVal)
                        tempNewIdx = self.nextChord.instDict[instKey].diatonicListVal.index(tempNewVal)
                        dChordValFC[iMot] = tempNewVal - progVal[instKey][0]
                    except:
                        tempNewVal = 0
                        progVal[instKey].append(0)
                        tempNewIdx = 0
                        dChordValFC[iMot] = 999
                        
                    
                bCtr += rytTot[iMot]

        dChordValFirstTot = 0
        dNumTot = 0
        for idcn, dcn in enumerate(dNum):
            dNumTot += abs(dcn)
            dChordValFirstTot += abs(dChordValFC[idcn])
        
        fitness = (dNumTot + dChordValFirstTot)/len(motTot)
        return fitness
        
        
    def createMotifFromChords(self):
        print('Creating Motif...')
        print('Total measures is: ' + str(self.length))
        print('Using Genetic Algorithm to find optimum solution...')
        self.createSubdivisions()
        sizePopulation = math.factorial(3)
        print('Creating initial population...')
        population = self.generatePopulation(sizePopulation)
        populationPerf = self.computePerfPopulation(population)
        print('Finished evolution!')
        chosenOne = population[populationPerf[0][0]]
        self.motTot = chosenOne[0]
        self.rytTot = chosenOne[1]

        

        
    
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
        self.progKey = {}
        self.diatTol = 3
        
        
    def fillMelodyVals(self):
        iChord = 0
        print('\nMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM\nFilling in values for melody...')
        for inst,instKey in enumerate(self.instDict):
            self.progNum[instKey] = []
            self.progVal[instKey] = []
            self.progKey[instKey] = []
            for iMot,mot in enumerate(self.motPeriod):
                if iMot == 0 or bCtr == self.beatsPerChord:
                    bCtr = 0
                    chord = self.chordProg[iChord]
                    newInstDict = {}
                    newInstDict[instKey] = deepcopy(self.instDict[instKey])
                    self.nextChord = ChordProgression(chord, self.tonality, newInstDict)
                    self.nextChord.setupOrderOfRangeMB()
                    self.nextChord.prog = chord
                    self.nextChord.inv = [None]
                    diatList = self.nextChord.getDiatList(0,chord,vb=0)
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
                    self.progKey[instKey].append(findKey(self.nextChord.instDict[instKey].grandStaff,self.nextChord.instDict[instKey].diatonicListVal[halfRange + dNum]))
                else:
                    previousPartVal = self.progVal[instKey][iMot-1]
                    previousPartIdx = min(range(len(self.nextChord.instDict[instKey].diatonicListVal)), key=lambda i: abs(self.nextChord.instDict[instKey].diatonicListVal[i]-previousPartVal))
                    previousPartNum = self.nextChord.instDict[instKey].diatonicListNum[previousPartIdx]
                    meloNum = self.motPeriod[iMot]
                    print(meloNum)
                    dNum = meloNum - previousPartNum
                    if dNum < -self.diatTol:
                        dNum = 7 + dNum
                    elif dNum > self.diatTol:
                        dNum = dNum - 7
                    tempNewVal = self.nextChord.instDict[instKey].diatonicListVal[previousPartIdx + dNum]
                    tempNewIdx = self.nextChord.instDict[instKey].diatonicListVal.index(tempNewVal)
                    print(tempNewVal)
                    dChordValFC = tempNewVal - self.progVal[instKey][0] 
                    self.progVal[instKey].append(tempNewVal)
                    self.progKey[instKey].append(findKey(self.nextChord.instDict[instKey].grandStaff,tempNewVal))
                    self.progNum[instKey].append(self.nextChord.instDict[instKey].diatonicListNum[previousPartIdx + dNum])

                bCtr += self.rytPeriod[iMot]
        
    def createAntecedentConsequent(self):
        self.motifLength = int(self.measures/2)
        self.antChord = self.chordProg[0:self.motifLength]
        self.conChord = self.chordProg[self.motifLength-1:]
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nCreating motif for antecedent...')
        ant = Motif(self.beatsPerChord,self.motifLength,self.timeMeter,self.tonality,self.instDict, self.antChord, self.diatTol)
        self.ant = ant
        self.ant.createMotifFromChords()
        
        print('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\nCreating motif for consequent...')
        cons = Motif(self.beatsPerChord,self.motifLength,self.timeMeter,self.tonality,self.instDict, self.conChord, self.diatTol, ant)
        self.cons = cons
        self.cons.createConsMotif()
        
        self.motPeriod = self.ant.motTot + self.cons.motTot
        self.rytPeriod = self.ant.rytTot + self.cons.rytTot
        self.dTime = self.rytPeriod
        self.fillMelodyVals()
        
    def generateAccompinament(self):
        pass
        
            
        
        





