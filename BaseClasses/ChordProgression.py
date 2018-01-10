from Utilities.BasicFunctions import findKey
from BaseClasses.Tonality import Tonality

from collections import Counter
from collections import defaultdict
from copy import deepcopy
import random
import math
import operator
class ChordProgression(object):
    def __init__(self, cadence, tonality, instDict):
        self.cadence = cadence
        self.diatTol = 3
        self.valTol = 5
        self.dChordNumMinTol = 3
        self.dChordNumTotTol = 5
        self.dChordValFCtol = 5
        self.rangeTol = 3
        self.instDict = instDict
        self.tonality = tonality
        self.inv = []
        self.prog = []
        self.checkForCadence()
        if len(self.prog) == 0:
            self.prog = self.cadence
        if len(self.inv) == 0:
            for i in range(len(self.prog)):
                self.inv.append(None)
    
    def checkForCadence(self):
        if self.cadence == 'Plagal':
            self.prog = ['4','1']
            self.inv = ['4/6',None]
        if self.cadence == 'Deceptive':
            self.prog = ['5','6']
        if self.cadence == 'CanonX2':
            #Prefer Major Key
            self.prog = ['1','5','6','3','4','1','4','5','1','5','6','3','4','1','4','5','1']
        if self.cadence == 'Radioactive':
            #Prefer Minor Key
            self.prog = ['1','3','7','7B5']
            self.prog = 6*self.prog
            self.prog.append('1')
        if self.cadence == 'ForgetYou':
            #Prefer Major Key
            self.prog = ['1','5B5','4','1']
            self.prog = 6*self.prog
            self.prog.append('1')
        if self.cadence == 'Blues':
            #Prefer Major Key
            self.prog = ['5B4','5B4B4','5B4','5B4B4']
            self.prog = 4*self.prog
        if self.cadence == 'BluesTestABA':
            #Prefer Major Key
            self.prog = []
            self.a = ['5B4','5B4B4','5B4','5B4B4','5B4','5B4B4','5B4','5B4B4']
            self.b = ['4B4','5B4B4','4B4','5B4B4','4B4','5B5','5S','5S']
            self.prog = self.a + self.b + self.a
            self.prog.append('1')  
        if self.cadence == 'Gymnopedie':
            #Prefer Major Key
            self.prog = ['4S','1S']
            self.prog = 8*self.prog     
        if self.cadence == 'Funky':
            #Prefer Minor Key
            self.prog = ['1S','7B5']
            self.prog = 12*self.prog  
            self.prog.append('1')
        if self.cadence == 'Ending':
            #Prefer Major Key
            self.prog = ['1','5B4','4','4B4B4B4','4B4','1']

    def loopDiatonic(self,i):
        if i > 7:
            return i - 7
        else:
            return i
    
    def inversionPicker(self, mod, diatList, inversion):
        if mod == 'T':
            if inversion == '4/6':
                order = [2,0,1]
            elif inversion == '6':
                order = [1,2,0]
            elif inversion == None:
                order = [0,1,2]
        elif mod == 'S' or mod == 'B':
            if inversion == '6/5':
                order = [1,2,3,0]
            elif inversion == '4/3':
                order = [2,3,0,1]
            elif inversion == '4/2':
                order = [3,0,1,2]
            elif inversion == None:
                order = [0,1,2,3]
        
        diatList = [diatList[i] for i in order]
        return diatList
        
    def findInstLowestBass(self,instKey,bass):
        iLowestBassVal = 128
        iLowestBassKey = ''
        iLowestBassNum = bass
        for i,val in enumerate(self.instDict[instKey].diatonicListVal):
            if self.instDict[instKey].diatonicListNum[i] == bass:
                if val < iLowestBassVal:
                    iLowestBassVal = val 
        #import pdb
        #pdb.set_trace()
        return iLowestBassVal, iLowestBassNum

    def checkForDuplicates(self,chordList):
        dupleList = [k for k, v in Counter(chordList).items() if v > 1]
        dupSum = 0
        for iDup in dupleList:
            dupSum = dupSum + iDup
        if dupSum == 0:
            hasDuplicates = False
        else:
            hasDuplicates = True
        dict = defaultdict(list)
        for i,item in enumerate(chordList):
            dict[item].append(i)
        dict = {k:v for k,v in dict.items() if len(v) > 1}
        return hasDuplicates, dict

    def checkForCloseness(self,chordList):
        tooClose = False
        for i in chordList:
            for k in chordList:
                if k is not i:
                    if abs(k - i) == 1:
                        tooClose = True
        return tooClose
        
    def findFitness(self, instDiatList, iChord, diatListInv):
        diatUse = {}
        progVal = {}
        for dt in diatListInv:
            diatUse[dt] = False
        
        dChordNum = []
        dChordValFC = []
        for inst,instKey in enumerate(self.orderOfRangeMB):
            dChordNum.append(0)
            dChordValFC.append(0)
            
        for inst,instKey in enumerate(self.orderOfRangeMB):
            previousPartVal = self.instPartsVal[instKey][iChord-1]
            previousPartIdx = min(range(len(self.instDict[instKey].diatonicListVal)), key=lambda i: abs(self.instDict[instKey].diatonicListVal[i]-previousPartVal))
            previousPartNum = self.instDict[instKey].diatonicListNum[previousPartIdx]
            diat = instDiatList[inst]
            dChordNum[inst] = diat - previousPartNum  
            if dChordNum[inst] < -self.diatTol:
                dChordNum[inst] = 7 + dChordNum[inst]
            elif dChordNum[inst] > self.diatTol:
                dChordNum[inst] = dChordNum[inst] - 7
            tempNewVal = self.instDict[instKey].diatonicListVal[previousPartIdx + dChordNum[inst]]
            progVal[instKey] = tempNewVal
            tempNewIdx = self.instDict[instKey].diatonicListVal.index(tempNewVal)
            dChordValFC[inst] = tempNewVal - self.instPartsVal[instKey][0]
            if tempNewIdx + self.rangeTol >= len(self.instDict[instKey].diatonicListNum) or tempNewIdx - self.diatTol < 0:
                dChordNum[inst] = 99
            diatUse[diat] = True
        diatUseList = list(diatUse.values())
        hasDuplicates, dupleDict = self.checkForDuplicates(list(progVal.values()))
        tooCloseSev = self.checkForCloseness(list(progVal.values()))
        for inst,instKey in enumerate(self.orderOfRangeMB):
            if not all(diatUseList) == True:
                dChordNum[inst] = 99
            if hasDuplicates:
                dChordNum[inst] = 99
            if tooCloseSev:
                dChordNum[inst] = 99
        
            
        dChordValFirstTot = 0
        dChordNumTot = 0
        for idcn, dcn in enumerate(dChordNum):
            dChordNumTot += abs(dcn)
            dChordValFirstTot += abs(dChordValFC[idcn])
        
        fitness = dChordNumTot + dChordValFirstTot
        return fitness
    
    def generatePopulation(self,sizePopulation,diatListInv,iChord):
        population = []
        i = 0
        while i < sizePopulation:
            population.append(self.generateRandomParts(diatListInv,iChord))
            i += 1
        return population
    
    def computePerfPopulation(self,population,iChord, diatListInv):
        populationPerf = {}
        for i,individual in enumerate(population):
            populationPerf[i] = self.findFitness(individual,iChord, diatListInv)
        return sorted(populationPerf.items(), key=operator.itemgetter(1))
    def selectFromPopulation(self,population,populationSorted,best_sample,lucky_few):
        nextGeneration = []
        for i in range(best_sample):
            nextGeneration.append(populationSorted[i])
        for i in range(lucky_few):
            nextGeneration.append(random.choice(populationSorted))
        random.shuffle(nextGeneration)
        return nextGeneration
        
        
    def createChild(self, ind1,ind2):
        child = []
        for iDiat, diat in enumerate(ind1):
            child.append(0)
        
        for iDiat,diat in enumerate(ind1):
            if (int(100*random.random()) < 50):
                child[iDiat] = ind1[iDiat]
            else:
                child[iDiat] = ind2[iDiat]
        return child
            
    def createChildren(self, breeders, number_of_child):
        nextPopulation = []
        for i in range(int(len(breeders)/2)):
            for j in range(number_of_child):
                nextPopulation.append(self.createChild(breeders[i], breeders[len(breeders) -1 -i]))
        return nextPopulation
        
    def generateRandomParts(self,diatListInv,iChord):
        diatUse = []
        instUse = []
        instDiatList = []
        for iDiat,diat in enumerate(diatListInv):
            diatUse.append(False)
        for inst,instKey in enumerate(self.orderOfRangeMB):
            instUse.append(False)
            instDiatList.append(-1)
        iD = 0
        iI = 0
        while all(diatUse) is False and all(instUse) is False:
            for inst,instKey in enumerate(self.orderOfRangeMB):
                previousPartVal = self.instPartsVal[instKey][iChord-1]
                previousPartIdx = min(range(len(self.instDict[instKey].diatonicListVal)), key=lambda i: abs(self.instDict[instKey].diatonicListVal[i]-previousPartVal))
                previousPartNum = self.instDict[instKey].diatonicListNum[previousPartIdx]
                randDiatIdx = random.randint(0,len(diatListInv)-1)
                diat = diatListInv[randDiatIdx]
                dChordNum = diat - previousPartNum  
                if dChordNum < -self.diatTol:
                    dChordNum = 7 + dChordNum
                elif dChordNum > self.diatTol:
                    dChordNum = dChordNum - 7
                tempNewVal = self.instDict[instKey].diatonicListVal[previousPartIdx + dChordNum]
                tempNewIdx = self.instDict[instKey].diatonicListVal.index(tempNewVal)

                diatUse[randDiatIdx] = True
                instUse[inst] = True
                instDiatList[inst] = diat
                iI += 1
                if iI > 30:
                    break
            iD += 1
            if iD > 30:
                break
        return instDiatList
        
    def resolveProgression(self, iChord, diatListInv):
        #Find halfway diatonic note
        print('\nNEW CHORD:\n')
        print('Currently on chord: ' + str(diatListInv))
        print('iChord: ' + str(iChord))
        progVal = {}
        progNum = {}
        hasDuplicates = True
        
        chordUse = []
        instUse = []
        dChordNumMin = []
        
        for i,diat in enumerate(diatListInv):
            chordUse.append(False)
            dChordNumMin.append(None)
        for inst,instKey in enumerate(self.orderOfRange):    
            instUse.append(False)
        
        
        if iChord > 0:
            #Genetic Algorithm
            print('Using Genetic Algorithm to find optimum solution...')
            if len(self.orderOfRange)<6:
                #Making population bigger if ensemble is too small
                sizePopulation = math.factorial(6) 
            else:
                sizePopulation = math.factorial(len(self.orderOfRangeMB))
            print('Creating initial population...')
            population = self.generatePopulation(sizePopulation,diatListInv,iChord)
            populationPerf = self.computePerfPopulation(population,iChord,diatListInv)
            best_sample = int(len(population)/2)
            lucky_few = int(len(population)) - best_sample
            print('Selecting best individuals based on fitness...')
            nextGeneration = self.selectFromPopulation(population,populationPerf,best_sample,lucky_few)
            nextGenPop = []
            for ng in nextGeneration:
                nextGenPop.append(population[ng[0]])
            number_of_child = 2
            print('Breeding...')
            nextPopulation = self.createChildren(nextGenPop, number_of_child)
            nextPopulationPerf = self.computePerfPopulation(nextPopulation,iChord,diatListInv)
            print('Finished evolution!')
            instDiatList = nextPopulation[nextPopulationPerf[0][0]]
            print('Final (non-bass) parts are: ' + str(instDiatList))
            for i,diat in enumerate(instDiatList):
                if diat == -1:
                    print('Initial population: ' + str(population))
                    print('Initial performance: ' + str(populationPerf))
                    print('NextGeneration: ' + str(nextGenPop))
                    print('Next Population: ' + str(nextPopulation))
                    print('Next Performance: ' + str(nextPopulationPerf))
                    raise ValueError('Could not converge on: ' + self.orderOfRangeMB[i])

        #import pdb
        #pdb.set_trace()
        breakCtr = 0
        chordUseSwitch = 0
        print('Populating chord....')
        for inst,instKey in enumerate(self.orderOfRange):
            if iChord == 0:
                if self.instDict[instKey].bass:
                    iLowestBassVal, iLowestBassNum = self.findInstLowestBass(instKey,diatListInv[0])
                    progVal[instKey] = iLowestBassVal
                    progNum[instKey] = iLowestBassNum
                    chordUse[0] = True
                    instUse[inst] = True
                elif all(chordUse) is False:
                    switch = 0
                    for iDiat,diat in enumerate(diatListInv):
                        if chordUse[iDiat] == False and switch == 0:
                            totalRange = len(self.instDict[instKey].diatonicListVal)
                            halfRange = int(totalRange/2)
                            halfNum = self.instDict[instKey].diatonicListNum[halfRange]
                            halfVal = self.instDict[instKey].diatonicListVal[halfRange]
                            chordNum = diatListInv[iDiat]
                            dNum = chordNum - halfNum
                            if dNum < -self.diatTol:
                                dNum = 7 + dNum
                            elif dNum > self.diatTol:
                                dNum = dNum - 7
                            progNum[instKey] = self.instDict[instKey].diatonicListNum[halfRange + dNum]
                            progVal[instKey] = self.instDict[instKey].diatonicListVal[halfRange + dNum]
                            chordUse[iDiat] = True
                            instUse[inst] = True
                            switch = 1
                elif instUse[inst] == False:
                    switch = 0
                    for iDiat,diat in enumerate(diatListInv):
                        if switch == 0:
                            totalRange = len(self.instDict[instKey].diatonicListVal)
                            halfRange = int(totalRange/2)
                            halfNum = self.instDict[instKey].diatonicListNum[halfRange]
                            halfVal = self.instDict[instKey].diatonicListVal[halfRange]
                            chordNum = diatListInv[iDiat]
                            dNum = chordNum - halfNum
                            if dNum < -self.diatTol:
                                dNum = 7 + dNum
                            elif dNum > self.diatTol:
                                dNum = dNum - 7
                            progNum[instKey] = self.instDict[instKey].diatonicListNum[halfRange + dNum]
                            progVal[instKey] = self.instDict[instKey].diatonicListVal[halfRange + dNum]
                            chordUse[iDiat] = True
                            instUse[inst] = True
                            switch = 1

            else:
                if self.instDict[instKey].bass:
                    iLowestBassVal, iLowestBassNum = self.findInstLowestBass(instKey,diatListInv[0])
                    progVal[instKey] = iLowestBassVal
                    progNum[instKey] = iLowestBassNum
                    chordUse[0] = True
                    instUse[inst] = True
                else:
                    dChordNum = []
                    dChordValFC = []
                    for inst,instKey in enumerate(self.orderOfRangeMB):
                        dChordNum.append(0)
                        dChordValFC.append(0)
                        
                    for inst,instKey in enumerate(self.orderOfRangeMB):
                        previousPartVal = self.instPartsVal[instKey][iChord-1]
                        previousPartIdx = min(range(len(self.instDict[instKey].diatonicListVal)), key=lambda i: abs(self.instDict[instKey].diatonicListVal[i]-previousPartVal))
                        previousPartNum = self.instDict[instKey].diatonicListNum[previousPartIdx]
                        diat = instDiatList[inst]
                        dChordNum[inst] = diat - previousPartNum  
                        if dChordNum[inst] < -self.diatTol:
                            dChordNum[inst] = 7 + dChordNum[inst]
                        elif dChordNum[inst] > self.diatTol:
                            dChordNum[inst] = dChordNum[inst] - 7
                        tempNewVal = self.instDict[instKey].diatonicListVal[previousPartIdx + dChordNum[inst]]
                        tempNewIdx = self.instDict[instKey].diatonicListVal.index(tempNewVal)
                        dChordValFC[inst] = tempNewVal - self.instPartsVal[instKey][0]
                                    
                        progNum[instKey] = self.instDict[instKey].diatonicListNum[previousPartIdx + dChordNum[inst]]
                        progVal[instKey] = self.instDict[instKey].diatonicListVal[previousPartIdx + dChordNum[inst]]
                        instUse[inst] = True
                    
            #import pdb
            #pdb.set_trace()
        print('Completed instrument loop')
        #import pdb
        #pdb.set_trace()
        
        
        dupTestVals = []
        for inst,instKey in enumerate(self.orderOfRange):
            if not self.instDict[instKey].bass:
                dupTestVals.append(progVal[instKey])
 
        for inst in progNum:
            diatKey = findKey(self.instDict[inst].grandStaff,progVal[inst])
            print('Instrument: ' + inst + ' Diatonic: ' + str(progNum[inst]) + ' Value: ' + str(progVal[inst]) + ' Key: ' + str(diatKey))
        return progNum, progVal
            
    def getDiatList(self,iChord,chord):
        root = int(chord[0])
        third = self.loopDiatonic(root + 2)
        fifth = self.loopDiatonic(root + 4)

        if len(chord) == 1:
            mod = 'T'
        elif len(chord) > 1:
            mod = chord[1]
        print('\nCreating diatonic list...')
        if len(chord)>1:
            if len(chord) < 4:
                if chord[1] == 'S':
                    print('Making a seventh chord: ' + chord[0])
                    #Seventh chord
                    seventh = self.loopDiatonic(root + 6)
                    diatList = [root,third,fifth,seventh]
                    diatListInv = self.inversionPicker(mod, diatList, self.inv[iChord])
                elif chord[1] == 'B':
                    #Borrowed chord (usually will be seventh chord by this point) Will not implement triad
                    borrowedRoot = int(chord[2])
                    borrowedKey = self.tonality.findBorrowedKey(borrowedRoot)
                    borrowedTonality = Tonality(borrowedKey,self.tonality.tonalMode)
                    print('Borrowing chord: ' + chord[0] + ' from key: ' + borrowedKey)
                    for instKey in self.instDict:
                        self.instDict[instKey].tonality = borrowedTonality
                        self.instDict[instKey].initializeDiatonics()
                    if chord[0] == '4' or len(self.orderOfRangeMB) < 4:
                        diatList = [root,third,fifth]
                        diatListInv = self.inversionPicker('T', diatList, self.inv[iChord])
                    else:
                        print('Making a seventh chord: ' + chord[0] + ' from key: ' + borrowedKey)
                        seventh = self.loopDiatonic(root + 6)
                        diatList = [root,third,fifth,seventh]
                        diatListInv = self.inversionPicker(mod, diatList, self.inv[iChord])  
            else:
                if chord[3] == 'B':
                    #Double borrow!
                    #Borrowed chord (usually will be seventh chord by this point) Will not implement triad
                    borrowedRoot = int(chord[2])
                    borrowedKey = self.tonality.findBorrowedKey(borrowedRoot)
                    borrowedTonality = Tonality(borrowedKey,self.tonality.tonalMode)
                    print('First Borrowing chord: ' + chord[0] + ' from key: ' + borrowedKey)
                    for instKey in self.instDict:
                        self.instDict[instKey].tonality = borrowedTonality
                        self.instDict[instKey].initializeDiatonics()
                    i = 3
                    while i + 2 <= len(chord):
                        borrowedRoot = int(chord[i+1])
                        borrowedKey = borrowedTonality.findBorrowedKey(borrowedRoot)
                        borrowedTonality = Tonality(borrowedKey,self.tonality.tonalMode)
                        print('Next Borrowing chord: ' + chord[0] + ' from key: ' + borrowedKey)
                        for instKey in self.instDict:
                            self.instDict[instKey].tonality = borrowedTonality
                            self.instDict[instKey].initializeDiatonics()
                        if chord[0] == '4' or len(self.orderOfRangeMB) < 4:
                            diatList = [root,third,fifth]
                            diatListInv = self.inversionPicker('T', diatList, self.inv[iChord])
                        else:
                            print('Making a seventh chord: ' + chord[0] + ' from key: ' + borrowedKey)
                            seventh = self.loopDiatonic(root + 6)
                            diatList = [root,third,fifth,seventh]
                            diatListInv = self.inversionPicker(mod, diatList, self.inv[iChord]) 
                        i += 2
        else:
            diatList = [root,third,fifth]
            diatListInv = self.inversionPicker(mod, diatList, self.inv[iChord])
        print('Finished diatonic list...')
        return diatListInv
            
    def setupOrderOfRangeMB(self):
        maxDiatonicListVal = {}
        for instKey in self.instDict:
            maxDiatonicListVal[instKey] = self.instDict[instKey].maxDiatonicListVal
        self.orderOfRange = sorted(maxDiatonicListVal,key=maxDiatonicListVal.get)
        self.orderOfRangeMB = []
        for inst,instKey in enumerate(self.orderOfRange):
            if not self.instDict[instKey].bass:
                self.orderOfRangeMB.append(instKey)
    
    def harmonizeParts(self):
        self.instPartsVal = {}
        self.instPartsNum = {}
        self.instPartsKey = {}
        self.setupOrderOfRangeMB()
        
        
        for instKey in self.instDict:
            self.instPartsVal[instKey] = []
            self.instPartsNum[instKey] = []
            self.instPartsKey[instKey] = []
            
        for iChord, chord in enumerate(self.prog):            
            diatListInv = self.getDiatList(iChord,chord)
  
            progNum, progVal = self.resolveProgression(iChord, diatListInv)
            for instKey in self.instDict:
                self.instPartsVal[instKey].append(progVal[instKey])
                self.instPartsNum[instKey].append(progNum[instKey])
                self.instPartsKey[instKey].append(findKey(self.instDict[instKey].grandStaff,progVal[instKey]))
            
            if len(chord)>1:
                if chord[1] == 'B':
                    for instKey in self.instDict:
                        self.instDict[instKey].tonality = self.tonality
                        self.instDict[instKey].initializeDiatonics()
            
                
                
            
        
        
        