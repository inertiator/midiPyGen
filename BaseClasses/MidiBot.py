from Utilities.BasicFunctions import findKey
from BaseClasses.Song import Song
from Utilities.MIDIUtil.MidiFile import MIDIFile

class MidiBot(MIDIFile):
    def __init__(self,song,title):
        self.title = title
        self.outputLocation = 'OutputMIDI' + '\\' + title + '.mid'
        self.song = song
        self.initializteMIDIFile()
        self.setTracks()
        self.setInitialTempo()
        self.setProgramChanges()
        
    def initializteMIDIFile(self):
        numTracks = len(self.song.ensemble.instrumentList)
        super(MidiBot,self).__init__(numTracks=numTracks, adjust_origin=True, file_format=2)
        
    def setTracks(self, time=0):
        for track,inst in enumerate(self.song.ensemble.instrumentList):
            super(MidiBot,self).addTrackName(track,time,inst)
    
    def setInitialTempo(self, time=0):
        for track,inst in enumerate(self.song.ensemble.instrumentList):
            super(MidiBot,self).addTempo(track,time,self.song.timeMeter.tempo)
    
    def setProgramChanges(self, time=0):
        for track,instKey in enumerate(self.song.instDict):
            program = self.song.instDict[instKey].program
            #TO DO: IMPLEMENT DIFFERENT CHANNELS
            channel = 0
            super(MidiBot,self).addProgramChange(track,channel,time,program)
    
    def runCode(self):
        for track,instKey in enumerate(self.song.instDict):
            for iT,time in enumerate(self.song.instDict[instKey].timeArr):
                pitch = self.song.instDict[instKey].chordProg[iT]
                duration = self.song.instDict[instKey].durArr[iT]
                velocity = self.song.instDict[instKey].velArr[iT]
                channel = self.song.instDict[instKey].chArr[iT]
                super(MidiBot,self).addNote(track,channel,pitch,time,duration,velocity)
        
    def writeMidiFile(self):
        midiBinFile = open(self.outputLocation,'wb')
        super(MidiBot,self).writeFile(midiBinFile)
        midiBinFile.close()
            
            
        

        
        
    
        

            
        