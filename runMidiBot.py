from BaseClasses.Tonality import Tonality
from BaseClasses.TimeMeter import TimeMeter
from BaseClasses.Song import Song
from BaseClasses.MidiBot import MidiBot
from BaseClasses.Ensemble import Ensemble

keySigs = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
date = '12_28_2017'
for keySig in keySigs:
    keySig = keySig
    tonalMode = 'Major'
    tonal = Tonality(keySig,tonalMode)
    numBeats = 4
    beat = 4
    tempo = 100
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
    botMidi = MidiBot(song,title)
    botMidi.runCode()
    botMidi.writeMidiFile()
