from Utilities.BasicFunctions import findKey
from collections import Counter
from collections import defaultdict
from copy import deepcopy
import random
import math
import operator
class ChordProgression(object):
    def __init__(self, cadence, instDict):
        self.cadence = cadence
        self.diatTol = 3
        self.valTol = 5
        self.dChordNumMinTol = 3
        self.dChordNumTotTol = 5
        self.dChordValFCtol = 5
        self.rangeTol = 3
        
        self.instDict = instDict
        if self.cadence == 'Plagal':
            self.prog = [4,1]
            self.inv = ['4/6',None]
        if self.cadence == 'Deceptive':
            self.prog = [5,6]
            self.inv = [None, None]
        if self.cadence == 'Simple':
            self.prog = [1,4,5,1]
            self.inv = [None,'3','3',None]
        if self.cadence == 'NewSong':
            self.prog = [6,1,5,4,6,1,5,4]
            self.inv = [None,None,None,None,None,None,None,None]
        if self.cadence == 'Canon':
            self.prog = [1,5,6,3,4,1,4,5,1]
            self.inv = [None,None,None,None,None,None,None,None,None]
        if self.cadence == 'CanonX2':
            self.prog = [1,5,6,3,4,1,4,5,1,5,6,3,4,1,4,5,1]
            self.inv = []
            for i in range(len(self.prog)):
                self.inv.append(None)
        if self.cadence == 'IfIAintGotYou':
            self.prog = [1,1,6,6,2,2,5,5,1,1,6,6,2,2,5,5,1,2,3,2,1,2,3,2,1,2,3,2,1,2,3,3,4,4,3,3,2,2,1,1,4,4,3,3,2,2,1,1]
            self.inv = []
            for i in range(len(self.prog)):
                self.inv.append(None)
        if self.cadence == 'Radioactive':
            self.prog = [4,6,3,7]
            self.prog = 8*self.prog
            self.prog.append(4)
            self.inv = []
            for i in range(len(self.prog)):
                self.inv.append(None)
                
    def loopDiatonic(self,i):
        if i > 7:
            return i - 7
        else:
            return i
    
    def inversionPicker(self, diatList, inversion = '4/6' ):
        if inversion == '4/6':
            order = [2,0,1]
        elif inversion == '3':
            order = [1,2,0]
        elif inversion == None:
            order = [0,1,2]
        
        diatList = [diatList[i] for i in order]
        return diatList
        
    def findInstLowestBass(self,bass):
        iLowestBassVal = 128
        iLowestBassKey = ''
        iLowestBassNum = bass
        for instKey in self.instDict:
            for i,val in enumerate(self.instDict[instKey].diatonicListVal):
                if self.instDict[instKey].diatonicListNum[i] == bass:
                    if val < iLowestBassVal:
                        iLowestBassVal = val 
                        iLowestBassKey = instKey
        #FIX IF BASS AND SECOND LOWEST HAVE SAME DIATONIC BASE VAL
        #import pdb
        #pdb.set_trace()
        return iLowestBassVal, iLowestBassKey, iLowestBassNum

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

    def resolveDuplicates(self, dupleDictValues,progNum,progVal,diatListInv, iChord):
        dupUse = False
        iDuplicate = 0
        while dupUse == False:
            for j in reversed(range(len(self.orderOfRange))):
                instKey = self.orderOfRange[j]
                progIdx = self.instDict[instKey].diatonicListVal.index(progVal[instKey])
                
                for i,dup in enumerate(dupleDictValues):
                    if j == dup and dupUse == False:
                        for iDiat,diat in enumerate(diatListInv):
                            if diat == progNum[instKey]:
                                idxDiat = diatListInv.index(diat)
                                if idxDiat == len(diatListInv) - 1:
                                    newDiat = diatListInv[idxDiat + 1 - len(diatListInv)]
                                else:
                                    newDiat = diatListInv[idxDiat + 1]
                                dNum = newDiat - progNum[instKey]
                                if dNum < -self.diatTol:
                                    dNum = 7 + dNum 
                                elif dNum > self.diatTol:
                                    dNum = dNum - 7
                                    
                                if iChord == 0:
                                    progNum[instKey] = self.instDict[instKey].diatonicListNum[progIdx + dNum]
                                    progVal[instKey] = self.instDict[instKey].diatonicListVal[progIdx + dNum]
                                    dupUse = True
                                else:
                                    tempNewVal = self.instDict[instKey].diatonicListVal[progIdx + dNum]
                                    dValFirst = tempNewVal - self.instPartsVal[instKey][0]
                                    if abs(dValFirst) <= self.valTol:
                                        progNum[instKey] = self.instDict[instKey].diatonicListNum[progIdx + dNum]
                                        progVal[instKey] = self.instDict[instKey].diatonicListVal[progIdx + dNum]
                                        dupUse = True   
            iDuplicate += 1
            if iDuplicate > 30:
                print('The previous chord was:')
                for inst in self.instDict:
                    print(inst + ': ' + str(self.instPartsNum[inst][iChord-1]))
                print('The active chord is:')
                print(diatListInv)
                print('So far we have:')
                for inst in progNum:
                    print(inst + ': ' + str(progNum[inst]))
                raise ValueError('ERROR: Could not resolve duplicates in: ' + str(diatListInv))
                
        return progNum, progVal

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
            previousPartNum = self.instPartsNum[instKey][iChord-1]
            previousPartIdx = self.instDict[instKey].diatonicListVal.index(previousPartVal)
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
        #print(instDiatList)
        #print(diatUse)
        diatUseList = list(diatUse.values())
        #print(diatUseList)
        #print('Checking for duplicates...')
        hasDuplicates, dupleDict = self.checkForDuplicates(list(progVal.values()))
        for inst,instKey in enumerate(self.orderOfRangeMB):
            if not all(diatUseList) == True:
                dChordNum[inst] = 99
            if hasDuplicates:
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
            instDiatList.append(0)
        iD = 0
        iI = 0
        while all(diatUse) is False:
            for inst,instKey in enumerate(self.orderOfRangeMB):
                previousPartVal = self.instPartsVal[instKey][iChord-1]
                previousPartNum = self.instPartsNum[instKey][iChord-1]
                previousPartIdx = self.instDict[instKey].diatonicListVal.index(previousPartVal)
                
                while instUse[inst] is False:
                    randDiatIdx = random.randint(0,len(diatListInv)-1)
                    diat = diatListInv[randDiatIdx]
                    #print('For instrument: ' + instKey + ', arriving at diatonic: ' + str(diat))
                    dChordNum = diat - previousPartNum  
                    if dChordNum < -self.diatTol:
                        dChordNum = 7 + dChordNum
                    elif dChordNum > self.diatTol:
                        dChordNum = dChordNum - 7
                    tempNewVal = self.instDict[instKey].diatonicListVal[previousPartIdx + dChordNum]
                    tempNewIdx = self.instDict[instKey].diatonicListVal.index(tempNewVal)
                    if tempNewIdx + self.rangeTol >= len(self.instDict[instKey].diatonicListNum) or tempNewIdx - self.diatTol < 0:
                        #print('Approaching range limit in instrument: ' + instKey + '! Try another diatonic.')
                        pass
                    elif diatUse[randDiatIdx] == False:
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
        
    def resolveProgression(self, iChord, iLowestBassVal, iLowestBassKey, iLowestBassNum, diatListInv):
        #Find halfway diatonic note
        print('\nNEW CHORD\n')
        print('Currently on chord: ' + str(diatListInv))
        print('iChord: ' + str(iChord))
        progVal = {}
        progNum = {}
        hasDuplicates = True
        
        maxDiatonicListVal = {}
        for instKey in self.instDict:
            maxDiatonicListVal[instKey] = self.instDict[instKey].maxDiatonicListVal
        self.orderOfRange = sorted(maxDiatonicListVal,key=maxDiatonicListVal.get)
        self.orderOfRangeMB = []
        for inst,instKey in enumerate(self.orderOfRange):
            if not self.instDict[instKey].bass:
                self.orderOfRangeMB.append(instKey)
        
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
            sizePopulation = math.factorial(len(self.orderOfRangeMB)*2)
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
            print('Final parts are: ' + str(instDiatList))

        #import pdb
        #pdb.set_trace()
        breakCtr = 0
        chordUseSwitch = 0
        print('Populating chord....')
        #if iChord == 34:
        #    import pdb
        #    pdb.set_trace()
        for inst,instKey in enumerate(self.orderOfRange):
            if iChord == 0:
                if instKey == iLowestBassKey:
                    progVal[instKey] = iLowestBassVal
                    progNum[instKey] = iLowestBassNum
                    chordUse[0] = True
                    instUse[inst] = True
                elif self.orderOfRange[-1] == instKey:
                    totalRange = len(self.instDict[instKey].diatonicListVal)
                    halfRange = int(totalRange/2)
                    halfNum = self.instDict[instKey].diatonicListNum[halfRange]
                    halfVal = self.instDict[instKey].diatonicListVal[halfRange]
                    chordNum = diatListInv[-1]
                    dNum = chordNum - halfNum
                    if dNum < -self.diatTol:
                        dNum = 7 + dNum 
                    elif dNum > self.diatTol:
                        dNum = dNum - 7
                    progNum[instKey] = self.instDict[instKey].diatonicListNum[halfRange + dNum]
                    progVal[instKey] = self.instDict[instKey].diatonicListVal[halfRange + dNum]
                    chordUse[-1] = True
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
                if instKey == iLowestBassKey:
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
                        previousPartNum = self.instPartsNum[instKey][iChord-1]
                        previousPartIdx = self.instDict[instKey].diatonicListVal.index(previousPartVal)
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
        print('Checking for duplicates...')
        hasDuplicates, dupleDict = self.checkForDuplicates(list(progVal.values()))
        if hasDuplicates == False:
            print('No duplicates found.')
        elif iChord > 0:
            raise ValueError('Duplicate should not exist!')
        else:
            print('Resolving duplicates')
            dupleDictValues = list(dupleDict.values())[0]
            progNum, progVal = self.resolveDuplicates(dupleDictValues,progNum,progVal,diatListInv, iChord)
                
        for inst in progNum:
            diatKey = findKey(self.instDict[inst].grandStaff,progVal[inst])
            print('Instrument: ' + inst + ' Diatonic: ' + str(progNum[inst]) + ' Value: ' + str(progVal[inst]) + ' Key: ' + str(diatKey))
        return progNum, progVal
            
        
        
    def harmonizeTriadParts(self):
        self.instPartsVal = {}
        self.instPartsNum = {}
        self.instPartsKey = {}
        for instKey in self.instDict:
            self.instPartsVal[instKey] = []
            self.instPartsNum[instKey] = []
            self.instPartsKey[instKey] = []
            
        for iChord, chord in enumerate(self.prog):
            
            self.root = []
            self.third = []
            self.fifth = []
            self.diatList = []
            
            root = chord
            third = self.loopDiatonic(root + 2)
            fifth = self.loopDiatonic(root + 4)
            
            self.root.append(root)
            self.third.append(third)
            self.fifth.append(fifth)

            self.diatList.append([root,third,fifth])
            diatList = [root,third,fifth]
            diatListInv = self.inversionPicker(diatList, self.inv[iChord])
            [iLowestBassVal, iLowestBassKey, iLowestBassNum] = self.findInstLowestBass(diatListInv[0])
            
            progNum, progVal = self.resolveProgression(iChord, iLowestBassVal, iLowestBassKey, iLowestBassNum, diatListInv)
            
            for instKey in self.instDict:
                self.instPartsVal[instKey].append(progVal[instKey])
                self.instPartsNum[instKey].append(progNum[instKey])
                self.instPartsKey[instKey].append(findKey(self.instDict[instKey].grandStaff,progVal[instKey]))
            
                
                
            
        
        
        