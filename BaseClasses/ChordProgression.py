from Utilities.BasicFunctions import findKey
from collections import Counter
from collections import defaultdict
class ChordProgression(object):
    def __init__(self, cadence):
        self.cadence = cadence
        self.diatTol = 3
        self.valTol = 7
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
        
    def findInstLowestBass(self,instDict,bass):
        iLowestBassVal = 128
        iLowestBassKey = ''
        iLowestBassNum = bass
        for instKey in instDict:
            for i,val in enumerate(instDict[instKey].diatonicListVal):
                if instDict[instKey].diatonicListNum[i] == bass:
                    if val < iLowestBassVal:
                        iLowestBassVal = val 
                        iLowestBassKey = instKey
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

    def resolveDuplicates(self,instDict,orderOfRange, dupleDictValues,progNum,progVal,diatListInv, iChord):
        dupUse = False
        while dupUse == False:
            for j in reversed(range(len(orderOfRange))):
                instKey = orderOfRange[j]
                progIdx = instDict[instKey].diatonicListVal.index(progVal[instKey])
                
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
                                    progNum[instKey] = instDict[instKey].diatonicListNum[progIdx + dNum]
                                    progVal[instKey] = instDict[instKey].diatonicListVal[progIdx + dNum]
                                    dupUse = True
                                else:
                                    tempNewVal = instDict[instKey].diatonicListVal[progIdx + dNum]
                                    dValFirst = tempNewVal - self.instPartsVal[instKey][0]
                                    if abs(dValFirst) <= self.valTol:
                                        progNum[instKey] = instDict[instKey].diatonicListNum[progIdx + dNum]
                                        progVal[instKey] = instDict[instKey].diatonicListVal[progIdx + dNum]
                                        dupUse = True   
                        
        return progNum, progVal

    def resolveProgression(self, instDict, iChord, iLowestBassVal, iLowestBassKey, iLowestBassNum, diatListInv):
        #Find halfway diatonic note
        
        print('Currently on chord: ' + str(diatListInv))
        
        progVal = {}
        progNum = {}
        hasDuplicates = True
        
        maxDiatonicListVal = {}
        for instKey in instDict:
            maxDiatonicListVal[instKey] = instDict[instKey].maxDiatonicListVal
        orderOfRange = sorted(maxDiatonicListVal,key=maxDiatonicListVal.get)
        
        chordUse = []
        for i,diat in enumerate(diatListInv):
            chordUse.append(False)
        
        
        diatDict = {}
        if iChord > 0:
            for iDiat, diat in enumerate(diatListInv):
                dChordNumMin = 10
                for inst, instKey in enumerate(orderOfRange):                    
                    previousPartVal = self.instPartsVal[instKey][iChord-1]
                    previousPartNum = self.instPartsNum[instKey][iChord-1]
                    previousPartIdx = instDict[instKey].diatonicListVal.index(previousPartVal)   
                    dChordNum = diat - previousPartNum
                    if abs(dChordNum) < abs(dChordNumMin) and instKey is not iLowestBassKey:
                        dChordNumMin = dChordNum
                        dChordNumMinIdx = iDiat
                        dChordNumMinNum = diat
                        diatDict[diat] = instKey
        #import pdb
        #pdb.set_trace()
        breakCtr = 0
        while all(chordUse) is False:
            for inst,instKey in enumerate(orderOfRange):
                if iChord == 0:
                    if instKey == iLowestBassKey:
                        progVal[instKey] = iLowestBassVal
                        progNum[instKey] = iLowestBassNum
                        chordUse[0] = True
                    elif orderOfRange[-1] == instKey:
                        totalRange = len(instDict[instKey].diatonicListVal)
                        halfRange = int(totalRange/2)
                        halfNum = instDict[instKey].diatonicListNum[halfRange]
                        halfVal = instDict[instKey].diatonicListVal[halfRange]
                        chordNum = diatListInv[-1]
                        dNum = chordNum - halfNum
                        if dNum < -self.diatTol:
                            dNum = 7 + dNum 
                        elif dNum > self.diatTol:
                            dNum = dNum - 7
                        progNum[instKey] = instDict[instKey].diatonicListNum[halfRange + dNum]
                        progVal[instKey] = instDict[instKey].diatonicListVal[halfRange + dNum]
                        chordUse[-1] = True
                    elif all(chordUse) is False:
                        switch = 0
                        for iDiat,diat in enumerate(diatListInv):
                            if chordUse[iDiat] == False and switch == 0:
                                totalRange = len(instDict[instKey].diatonicListVal)
                                halfRange = int(totalRange/2)
                                halfNum = instDict[instKey].diatonicListNum[halfRange]
                                halfVal = instDict[instKey].diatonicListVal[halfRange]
                                chordNum = diatListInv[iDiat]
                                dNum = chordNum - halfNum
                                if dNum < -self.diatTol:
                                    dNum = 7 + dNum
                                elif dNum > self.diatTol:
                                    dNum = dNum - 7
                                progNum[instKey] = instDict[instKey].diatonicListNum[halfRange + dNum]
                                progVal[instKey] = instDict[instKey].diatonicListVal[halfRange + dNum]
                                chordUse[iDiat] = True
                                switch = 1
                    else: 
                        totalRange = len(instDict[instKey].diatonicListVal)
                        halfRange = int(totalRange/2)
                        halfNum = instDict[instKey].diatonicListNum[halfRange]
                        halfVal = instDict[instKey].diatonicListVal[halfRange]
                        chordNum = diatListInv[-1]
                        dNum = chordNum - halfNum
                        if dNum < -self.diatTol:
                            dNum = 7 + dNum
                        elif dNum > self.diatTol:
                            dNum = 7 - dNum
                        progNum[instKey] = instDict[instKey].diatonicListNum[halfRange + dNum]
                        progVal[instKey] = instDict[instKey].diatonicListVal[halfRange + dNum]
                else:
                    #self.instPartsVal and self.instPartsNum should exist now
                    previousPartVal = self.instPartsVal[instKey][iChord-1]
                    previousPartNum = self.instPartsNum[instKey][iChord-1]
                    previousPartIdx = instDict[instKey].diatonicListVal.index(previousPartVal)
                    if instKey == iLowestBassKey:
                        progVal[instKey] = iLowestBassVal
                        progNum[instKey] = iLowestBassNum
                        chordUse[0] = True
                    elif all(chordUse) is False:
                        switch = 0
                        dChordNumMin = 10
                        for iDiat,diat in enumerate(diatListInv):
                            if chordUse[iDiat] == False or diatDict[diat] == instKey:
                                #import pdb
                                #pdb.set_trace()
                                
                                #if chordUse[iDiat] == False and switch == 0 and diatDict[diat] == instKey:                       
                                if switch == 0:
                                    dChordNum = diat - previousPartNum
                                    dChordValFirst = instDict[instKey].diatonicListVal[previousPartIdx + dChordNum] - self.instPartsVal[instKey][0]
                                    if dChordNum < -self.diatTol or dChordValFirst < -self.valTol:
                                        dChordNum = 7 + dChordNum
                                    elif dChordNum > self.diatTol or dChordValFirst > self.valTol:
                                        dChordNum = dChordNum - 7
                                    if abs(dChordNum) < abs(dChordNumMin):
                                        dChordNumMin = dChordNum
                                        dChordNumMinIdx = iDiat
                                        dChordNumMinNum = diat
                                    #if dChordNumMin < -self.diatTol:
                                    #    dChordNumMin = 7 + dChordNumMin
                                    #elif dChordNumMin > self.diatTol:
                                    #    dChordNumMin = 7 - dChordNumMin
                                    tempNewVal = instDict[instKey].diatonicListVal[previousPartIdx + dChordNumMin]
                                    dChordValFirstCorrected = tempNewVal - self.instPartsVal[instKey][0]
                                    progNum[instKey] = instDict[instKey].diatonicListNum[previousPartIdx + dChordNumMin]
                                    progVal[instKey] = instDict[instKey].diatonicListVal[previousPartIdx + dChordNumMin]
                                    chordUse[iDiat] = True
                                    #import pdb
                                    #pdb.set_trace()
                                        
                                        
                                    switch = 1
                    else:
                        dChordNumMin = 10
                        for iDiat, diat in enumerate(diatListInv):
                            dChordNum = diat - previousPartNum
                            if dChordNum < -self.diatTol:
                                dChordNum = 7 + dChordNum
                            if dChordNum > self.diatTol:
                                dChordNum = dChordNum - 7
                            if abs(dChordNum) < abs(dChordNumMin):
                                dChordNumMin = dChordNum
                                dChordNumMinIdx = iDiat
                                dChordNumMinNum = diat
                            tempNewVal = instDict[instKey].diatonicListVal[previousPartIdx + dChordNumMin]
                            dChordValFirst = tempNewVal - self.instPartsVal[instKey][0]
                        if abs(dChordValFirst) <= self.valTol:
                            progNum[instKey] = instDict[instKey].diatonicListNum[previousPartIdx + dChordNumMin]
                            progVal[instKey] = instDict[instKey].diatonicListVal[previousPartIdx + dChordNumMin]
                #import pdb
                #pdb.set_trace()
            while hasDuplicates == True:
                print('Resolving duplicates')
                hasDuplicates, dupleDict = self.checkForDuplicates(list(progVal.values()))
                if hasDuplicates == False:
                    break
                dupleDictValues = list(dupleDict.values())[0]
                progNum, progVal = self.resolveDuplicates(instDict,orderOfRange,dupleDictValues,progNum,progVal,diatListInv, iChord)
            #checkForDuplicates(progVal.values)
            if all(chordUse) == False:
                print('Doing another iteration')
                for iDiat,diat in enumerate(diatListInv):
                    if chordUse[iDiat] == False:
                        print('There is no home for diatonic: ' + str(diat))
                for instKey in instDict:
                    if not instKey in progNum:
                        print('There is no value for instrument: ' + instKey)
            print('Most optimum diatonics for each instrument are: ' + str(diatDict))
            #import pdb
            #pdb.set_trace()
            breakCtr += 1
            if breakCtr > 30:
                print('The last chord was:')
                for inst in instDict:
                    print(inst + ': ' + str(self.instPartsNum[inst][iChord-1]))
                    
                print('So far we have:')
                for inst in progNum:
                    print(inst + ': ' + str(progNum[inst]))
                raise ValueError('ERROR: Could not resolve chord: ' + str(diatListInv))
                
        for inst in progNum:
            diatKey = findKey(instDict[inst].grandStaff,progVal[inst])
            print('Instrument: ' + inst + ' Diatonic: ' + str(progNum[inst]) + ' Value: ' + str(progVal[inst]) + ' Key: ' + str(diatKey))
        return progNum, progVal
            
        
        
    def harmonizeTriadParts(self,instDict):
        self.instPartsVal = {}
        self.instPartsNum = {}
        self.instPartsKey = {}
        for instKey in instDict:
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
            [iLowestBassVal, iLowestBassKey, iLowestBassNum] = self.findInstLowestBass(instDict, diatListInv[0])
            
            progNum, progVal = self.resolveProgression(instDict, iChord, iLowestBassVal, iLowestBassKey, iLowestBassNum, diatListInv)
            
            for instKey in instDict:
                self.instPartsVal[instKey].append(progVal[instKey])
                self.instPartsNum[instKey].append(progNum[instKey])
                self.instPartsKey[instKey].append(findKey(instDict[instKey].grandStaff,progVal[instKey]))
            
            #for instKey in instDict:
            #    iLowestRoot,key = self.findInstLowestRoot(instDict,self.chord.root)
            #    instKey = 1
    
                
                
            
        
        
        