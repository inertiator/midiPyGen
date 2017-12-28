from Utilities.BasicFunctions import findKey
from BaseClasses.Tonality import Tonality
from BaseClasses.Ensemble import Ensemble
from BaseClasses.Instruments import *
from BaseClasses.TimeMeter import *
from BaseClasses.ChordProgression import ChordProgression
from BaseClasses.Form import Form

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
            self.instDict[instKey].chordProg = []
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
        
    
    def addSingleCadenceAcc(self, cadence, start = 0, velocity = 70):
        chordProg = ChordProgression(cadence)
        measures = len(chordProg.prog)
        chordProg.harmonizeTriadParts(self.instDict)
        for instKey in self.instDict:
            for part in chordProg.instPartsVal[instKey]:
                self.instDict[instKey].chordProg.append(part)
        
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
        
        

        
        
    
        

            
        