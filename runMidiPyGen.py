from BaseClasses.Tonality import Tonality
from BaseClasses.TimeMeter import TimeMeter
from BaseClasses.Song import Song
from BaseClasses.MidiPyGen import MidiPyGen
from BaseClasses.Ensemble import Ensemble

date = '1_4_2018'
keySig = 'F#'
tonalMode = 'Minor'
tonal = Tonality(keySig,tonalMode)
numBeats = 4
beat = 4
tempo = 120
timeMeter = TimeMeter(numBeatsPerMeasure = numBeats, beat = beat, tempo = tempo)


ensem = 'SATB'
ensemble = Ensemble(ensem)

song = Song(ensemble,timeMeter,tonal)

cadence = 'Radioactive'
#cadence = 'NewSong'
#Fix this!
title = date + '_' + ensem + '_' + cadence + '_' + keySig + '_' + tonalMode
song.addSingleCadenceAcc(cadence)
botMidi = MidiPyGen(song,title)
botMidi.runCode()
botMidi.writeMidiFile()

print('\nFinal chord progression:')
for instKey in song.instDict:
    print('Instrument: ' + instKey)
    print(song.instDict[instKey].chordProg)
    print(song.instDict[instKey].chordProgKeys)
