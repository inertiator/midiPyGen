from BaseClasses.Tonality import Tonality
from BaseClasses.TimeMeter import TimeMeter
from BaseClasses.Song import Song
from BaseClasses.MidiPyGen import MidiPyGen
from BaseClasses.Ensemble import Ensemble

date = '12_28_17'
keySig = 'G'
tonalMode = 'Major'
tonal = Tonality(keySig,tonalMode)
numBeats = 3
beat = 4
tempo = 120
timeMeter = TimeMeter(numBeatsPerMeasure = numBeats, beat = beat, tempo = tempo)

#Canon in D works for JoJoQuartet but not JoJoTrio

ensem = 'JoJoQuartet'
ensemble = Ensemble(ensem)

song = Song(ensemble,timeMeter,tonal)

cadence = 'Canon'
#cadence = 'NewSong'
#Fix this!
title = date + '_' + ensem + '_' + cadence + '_' + keySig + '_' + tonalMode
song.addSingleCadenceAcc(cadence)
botMidi = MidiPyGen(song,title)
botMidi.runCode()
botMidi.writeMidiFile()
