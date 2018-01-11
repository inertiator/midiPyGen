from Utilities.BasicFunctions import findKey
from BaseClasses.Tonality import Tonality
from BaseClasses.Ensemble import Ensemble
from BaseClasses.Instruments import *
from BaseClasses.TimeMeter import *
from BaseClasses.ChordProgression import ChordProgression
from BaseClasses.Form import Form
from BaseClasses.Motif import Motif,Period
from copy import deepcopy

class Song(object):
    def __init__(self,ensemble=None,timeMeter=None,tonality=None):
        self.tonality = tonality
        self.ensemble = ensemble
        self.timeMeter = timeMeter
        
        if self.tonality == None:
            self.tonality = Tonality()
        if self.ensemble == None:
            self.ensemble = Ensemble('Test')
        if timeMeter == None:
            self.timeMeter = TimeMeter()
        
        
        self.numTracks = len(self.ensemble.instrumentList)
        self.createInstClasses()
        self.initializeInstTimeMeter()
        for instKey in self.instDict:
            self.instDict[instKey].pitchArr = []
            self.instDict[instKey].pitchArrKeys = []
            self.instDict[instKey].timeArr = []
            self.instDict[instKey].durArr = []
            self.instDict[instKey].velArr = []
            self.instDict[instKey].chArr = []
            
    def createInstClasses(self):
        self.instDict = {}
        for i, instKey in enumerate(self.ensemble.instrumentList):
            instClass = globals()[self.ensemble.instClassList[i]]
            track = i 
            self.instDict[instKey] = instClass(tonality = self.tonality, track = track)
    
    def initializeInstTimeMeter(self):
        for instKey in self.instDict:
            self.instDict[instKey].timeMeter = InstrumentTimeMeter(masterTime = self.timeMeter)
        
    
    def generateSimpleAcc(self, cadence, start = 0, velocity = 70):
        chordProg = ChordProgression(cadence, self.tonality, self.instDict)
        measures = len(chordProg.prog)
        chordProg.harmonizeParts()
        for instKey in self.instDict:
            for part in chordProg.instPartsVal[instKey]:
                self.instDict[instKey].pitchArr.append(part)
                chordProgKey = findKey(self.instDict[instKey].grandStaff,part)
                self.instDict[instKey].pitchArrKeys.append(chordProgKey)
        
        duration = self.timeMeter.numBeatsPerMeasure
        progTime = ProgressionTime(start, measures, duration, velocity, self.timeMeter)
         
        ch = 0
        
        for instKey in self.instDict:
            for tm in progTime.progTimeArray:
                self.instDict[instKey].timeArr.append(tm)
            for dur in progTime.progDurArray:
                self.instDict[instKey].durArr.append(dur)
            for vel in progTime.progVelArray:
                self.instDict[instKey].velArr.append(vel)
                self.instDict[instKey].chArr.append(ch)
                
    def generateMelodyAcc(self, cadence, melodyKey, start = 0, meloVel = 100, accVel = 70):
        velocity = 60
        self.melodyDict = {}
        
        self.melodyDict[melodyKey] = deepcopy(self.instDict[melodyKey])
        self.instDict.pop(melodyKey)
        
        chordProg = ChordProgression(cadence, self.tonality, self.instDict)
        measures = len(chordProg.prog)
        chordProg.harmonizeParts()
        for instKey in self.instDict:
            for part in chordProg.instPartsVal[instKey]:
                self.instDict[instKey].pitchArr.append(part)
                pitchKey = findKey(self.instDict[instKey].grandStaff,part)
                self.instDict[instKey].pitchArrKeys.append(pitchKey)
        
        duration = self.timeMeter.numBeatsPerMeasure
        progTime = ProgressionTime(start, measures, duration, velocity, self.timeMeter)
        
        ch = 0
        for instKey in self.instDict:
            for tm in progTime.progTimeArray:
                self.instDict[instKey].timeArr.append(tm)
            for dur in progTime.progDurArray:
                self.instDict[instKey].durArr.append(dur)
            for vel in progTime.progVelArray:
                self.instDict[instKey].velArr.append(vel)
                self.instDict[instKey].chArr.append(ch)
                
                
        print('\nWorking on melody part now...')
        #Split total length into 3 parts
        measuresPerForm = int((measures-1)/3)
        motifTot = {}
        formList = ['A','B','A']
        measureCtr = 0
        melTime = 0
        for iF,form in enumerate(formList):
            if form in motifTot:
                #If form has been already created
                for melodyKey in self.melodyDict:
                    for part in motifTot[form].progVal[melodyKey]:
                        self.melodyDict[melodyKey].pitchArr.append(part)
                        pitchKey = findKey(self.melodyDict[melodyKey].grandStaff,part)
                        self.melodyDict[melodyKey].pitchArrKeys.append(pitchKey)
                        
                for melodyKey in self.melodyDict:
                        for dt in motifTot[form].dTime:
                            self.melodyDict[melodyKey].timeArr.append(melTime)
                            self.melodyDict[melodyKey].durArr.append(dt)
                            melTime += dt
                            
                        for vel in progTime.progVelArray:
                            self.melodyDict[melodyKey].velArr.append(100)
                            self.melodyDict[melodyKey].chArr.append(ch)
                measureCtr  += measuresPerForm  
            else:
                print(chordProg.prog)
                periodProg = chordProg.prog[measureCtr:measuresPerForm+measureCtr]
                print(periodProg)
                print(measureCtr)
                beatsPerChord = 4
                partPeriod = Period(beatsPerChord, self.timeMeter, self.tonality, periodProg, measuresPerForm, self.melodyDict)
                partPeriod.createAntecedentConsequent()
                motifTot[form] = deepcopy(partPeriod)
                for melodyKey in self.melodyDict:
                    for part in motifTot[form].progVal[melodyKey]:
                        self.melodyDict[melodyKey].pitchArr.append(part)
                        pitchKey = findKey(self.melodyDict[melodyKey].grandStaff,part)
                        self.melodyDict[melodyKey].pitchArrKeys.append(pitchKey)
                        
                for melodyKey in self.melodyDict:
                        for dt in motifTot[form].dTime:
                            self.melodyDict[melodyKey].timeArr.append(melTime)
                            self.melodyDict[melodyKey].durArr.append(dt)
                            melTime += dt
                            
                        for vel in progTime.progVelArray:
                            self.melodyDict[melodyKey].velArr.append(100)
                            self.melodyDict[melodyKey].chArr.append(ch)
                measureCtr  += measuresPerForm
                            
        for melodyKey in self.melodyDict:
            self.instDict[melodyKey] = deepcopy(self.melodyDict[melodyKey])
            
        
        
        
        
        

        
        
    
        

            
        