from BaseClasses.Tonality import Tonality
from BaseClasses.TimeMeter import TimeMeter
from BaseClasses.Song import Song
from BaseClasses.MidiPyGen import MidiPyGen
from BaseClasses.Ensemble import Ensemble

###############################
#### midiPyGen Run File #######
###############################
#If it breaks, try running it again. The nature of the randomized genetic algorithm can yield a better result.

date = '1_15_2018'
keySig = 'A'
tonalMode = 'Minor'
tonal = Tonality(keySig,tonalMode)
#numBeats: Time signature input, number of beats per measure
numBeats = 4
#beat: Time signature beat note, 4 means quarter note
beat = 4
#Tempo in beats per minute
tempo = 120

timeMeter = TimeMeter(numBeatsPerMeasure = numBeats, beat = beat, tempo = tempo)

#Select ensemble, currently, have, JoJoQuartet, JoJoQuintet, JoJoOctet, SATB
ensem = 'JoJoOctet'
ensemble = Ensemble(ensem)


#Select cadence from ChordProgression.py
cadence = 'Funky'

#Melody Generation with accompaniment, mode = 'melody', select melody instrument
#using melodyKey. Use mode = 'acc' for chord progression only.
melodyKey = 'flute'
mode = 'melody'
complete = False
while not complete:
    try:
        song = Song(ensemble,timeMeter,tonal)
        if mode == 'melody':
        #############################################################
        #Work in progress, Works Intermittently, Still Very Buggy (Breaks often and doesn't resolve at right chord in first part of periods.
        #############################################################
            title = date + '_' + ensem + '_' + cadence + '_' + keySig + '_' + tonalMode + '_' + str(melodyKey)
            song.generateMelodyAcc(cadence, melodyKey)
            botMidi = MidiPyGen(song,title)
            botMidi.runCode()
            botMidi.writeMidiFile()
            complete = True
        elif mode == 'acc':
            title = date + '_' + ensem + '_' + cadence + '_' + keySig + '_' + tonalMode
            song.generateSimpleAcc(cadence)
            botMidi = MidiPyGen(song,title)
            botMidi.runCode()
            botMidi.writeMidiFile()
            complete = True
    except:
        print('Failed case, attempting again')

print('\nFinal chord progression:')
for instKey in song.instDict:
    print('Instrument: ' + instKey)
    print(song.instDict[instKey].pitchArr)
    print(song.instDict[instKey].pitchArrKeys)

