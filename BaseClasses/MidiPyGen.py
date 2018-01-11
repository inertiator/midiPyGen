from Utilities.BasicFunctions import findKey
from BaseClasses.Song import Song
from Utilities.MIDIUtil.MidiFile import MIDIFile

class MidiPyGen(MIDIFile):
    '''
    A class that links together MIDIFile and the Song class.
    This class needs a Song object to function
    The song input encapsulates all data needed for tracks, pitch, key, tempo, tonality, and instruments.
    '''
    def __init__(self,song,title):
        '''
        Initialize MidiPyGen
        ------------------------------------------------
        INPUT       TYPE    DESCRIPTION
        ------------------------------------------------
        song        object  Song input. Song object must be developed before starting MidiPyGen
        title       string  Title of song. Will determine title of midi file
        '''
        self.title = title
        self.outputLocation = 'OutputMIDI' + '\\' + title + '.mid'
        self.song = song
        self.initializteMIDIFile()
        self.setTracks()
        self.setInitialTempo()
        self.setProgramChanges()
        
    def initializteMIDIFile(self):
        numTracks = len(self.song.ensemble.instrumentList)
        super(MidiPyGen,self).__init__(numTracks=numTracks, adjust_origin=True, file_format=2)
        
    def setTracks(self, time=0):
        for track,inst in enumerate(self.song.ensemble.instrumentList):
            super(MidiPyGen,self).addTrackName(track,time,inst)
    
    def setInitialTempo(self, time=0):
        for track,inst in enumerate(self.song.ensemble.instrumentList):
            super(MidiPyGen,self).addTempo(track,time,self.song.timeMeter.tempo)
    
    def setProgramChanges(self, time=0):
        for track,instKey in enumerate(self.song.instDict):
            program = self.song.instDict[instKey].program
            #TO DO: IMPLEMENT DIFFERENT CHANNELS
            channel = 0
            super(MidiPyGen,self).addProgramChange(track,channel,time,program)
    
    def runCode(self):
        for track,instKey in enumerate(self.song.instDict):
            for iT,time in enumerate(self.song.instDict[instKey].timeArr):
                print(instKey)
                print(iT)
                print(time)
                pitch = self.song.instDict[instKey].pitchArr[iT]
                duration = self.song.instDict[instKey].durArr[iT]
                velocity = self.song.instDict[instKey].velArr[iT]
                channel = self.song.instDict[instKey].chArr[iT]
                program = self.song.instDict[instKey].program
                super(MidiPyGen,self).addProgramChange(track,channel,time,program)
                super(MidiPyGen,self).addNote(track,channel,pitch,time,duration,velocity)
        
    def writeMidiFile(self):
        midiBinFile = open(self.outputLocation,'wb')
        super(MidiPyGen,self).writeFile(midiBinFile)
        midiBinFile.close()
            
            
        

        
        
    
        

            
        