
class TimeMeter(object):
    def __init__(self, numBeatsPerMeasure = 4, beat = 4, tempo = 100, totalTime = None, numMeasures = None):
        
        self.numBeatsPerMeasure = numBeatsPerMeasure
        self.beat = beat
        self.tempo = tempo
        self.totalTime = totalTime
        self.numMeasures = numMeasures
        
        if self.totalTime is None and self.numMeasures is None:
            self.numMeasures = 2
            self.totalTime = 1/self.tempo*self.numBeatsPerMeasure*self.numMeasures*60 #Time in seconds
        elif self.totalTime is None and self.numMeasures is not None:
            #Beats/Minute, Total Time = Minute/Beats*Beats/Measure*numMeasures*60
            self.totalTime = 1/self.tempo*self.numBeatsPerMeasure*self.numMeasures*60 #Time in seconds
        elif self.numMeasures is None and self.totalTime is not None:
            self.numMeasures = self.totalTime*self.tempo/self.numBeatsPerMeasure/60
        self.setMainStaffArray()
        
    def setMainStaffArray(self):
        self.mainStaff = {}
        for i in range(self.numMeasures):
            self.mainStaff[i] = []
            for j in range(self.numBeatsPerMeasure):
                self.mainStaff[i].append(j)
    

class InstrumentTimeMeter(TimeMeter):
    def __init__(self, masterTime = None):
        self.masterTime = masterTime
        if masterTime == None:
            masterTime = TimeMeter()
        self.pitchArray = []
        self.volumeArray = []
        self.setInstStaffArray()
        
    def setInstStaffArray(self):
        self.instStaff = {}
        for i in range(self.masterTime.numMeasures):
            self.instStaff[i] = []
            for j in range(self.masterTime.numBeatsPerMeasure):
                self.instStaff[i].append(j)
                
    def timePart(self, startMeasure, startBeat, duration):
        pass
        
class ProgressionTime(object):
    def __init__(self,start,measures,duration,velocity,timeMeter):
        self.start = start
        self.measures = measures
        self.duration = duration
        self.timeMeter = timeMeter
        self.velocity = velocity
        self.createTimeArray()
        self.createDurationArray()
        self.createVelocityArray()
        
    def createTimeArray(self):
        self.progTimeArray = []
        for i in range(self.measures):
            self.progTimeArray.append(self.start + self.duration*i)
        
    def createDurationArray(self):
        self.progDurArray = []
        for i in range(self.measures):
            self.progDurArray.append(self.duration)
    
    def createVelocityArray(self):
        self.progVelArray = []
        for i in range(self.measures):
            self.progVelArray.append(self.velocity)