from Utilities.BasicFunctions import findKey
from collections import Counter
from collections import defaultdict
class ChordProgression(object):
    def __init__(self, cadence):
        self.cadence = cadence
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
        import pdb
        pdb.set_trace()
        return hasDuplicates, dict

    def resolveDuplicates(self,instDict,orderOfRange, dupleDictValues,progNum,progVal,diatListInv):
        dupUse = False
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
                            
                            if dNum < -4:
                                dNum = 7 + dNum 

                            progNum[instKey] = instDict[instKey].diatonicListNum[progIdx + dNum]
                            progVal[instKey] = instDict[instKey].diatonicListVal[progIdx + dNum]
                            dupUse = True
                    
        return progNum, progVal

    def resolveProgression(self, instDict, iChord, iLowestBassVal, iLowestBassKey, iLowestBassNum, diatListInv):
        #Find halfway diatonic note
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
            
        
        while all(chordUse) is False and hasDuplicates:
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
                        if dNum < -4:
                            dNum = 7 + dNum 
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
                                if dNum < -4:
                                    dNum = 7 + dNum
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
                        if dNum < -4:
                            dNum = 7 + dNum
                        progNum[instKey] = instDict[instKey].diatonicListNum[halfRange + dNum]
                        progVal[instKey] = instDict[instKey].diatonicListVal[halfRange + dNum]
                        chordUse[-1] = True
                else:
                    if instKey == iLowestBassKey:
                    #Take current note and try to stay there!
                        progVal[instKey] = iLowestBassVal
                        progNum[instKey] = iLowestBassNum
                        chordUse[0] = True

                    else:
                        #self.instPartsVal and self.instPartsNum should exist now
                        previousPartVal = self.instPartsVal[instKey][iChord-1]
                        previousPartNum = self.instPartsNum[instKey][iChord-1]
                        previousPartIdx = instDict[instKey].diatonicListVal.index(previousPartVal)
                        dChordNumMin = 10
                        for iDiat, diat in enumerate(diatListInv):
                            dChordNum = diat - previousPartNum
                            if abs(dChordNum) < abs(dChordNumMin):
                                dChordNumMin = dChordNum
                                dChordNumMinIdx = iDiat
                                dChordNumMinNum = diat
                        if dChordNumMin < -4:
                            dChordNumMin = 7 + dChordNumMin
                        progNum[instKey] = instDict[instKey].diatonicListNum[previousPartIdx + dChordNumMin]
                        progVal[instKey] = instDict[instKey].diatonicListVal[previousPartIdx + dChordNumMin]
                        chordUse[iDiat] = True


            hasDuplicates, dupleDict = self.checkForDuplicates(list(progVal.values()))
            if hasDuplicates == True:
                dupleDictValues = list(dupleDict.values())[0]
                progNum, progVal = self.resolveDuplicates(instDict,orderOfRange,dupleDictValues,progNum,progVal,diatListInv)

            #checkForDuplicates(progVal.values)
            
            
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
    
                
                
            
        
        
        