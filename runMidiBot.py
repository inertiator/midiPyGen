from BaseClasses.Tonality import Tonality
from BaseClasses.TimeMeter import TimeMeter
from BaseClasses.Song import Song
from BaseClasses.MidiBot import MidiBot
from BaseClasses.Ensemble import Ensemble


keySig = 'C'
tonalMode = 'Major'
tonal = Tonality(keySig,tonalMode)
numBeats = 4
beat = 4
tempo = 100
timeMeter = TimeMeter(numBeatsPerMeasure = numBeats, beat = beat, tempo = tempo)

ensemble = Ensemble('Test')

song = Song(ensemble,timeMeter,tonal)

#cadence = 'NewSong'
#Fix this!
title = cadence + '_' + keySig + '_' + tonalMode
song.addSingleCadenceAcc(cadence)

import pdb
pdb.set_trace()
botMidi = MidiBot(song,title)
botMidi.runCode()
botMidi.writeMidiFile()
