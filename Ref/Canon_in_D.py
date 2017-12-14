###################################################################################
# A hopefully successful code that creates a Canon in D midi file
# Date: 5/2016
# Version: As many zeros as possible
# Python version used: 
###################################################################################

#Import the libraries. We're taking in our Midi generator (MIDIUtil), and our MIDI player ()
from MIDIUtil_Base.midiutil.MidiFile3 import MIDIFile
from Utilities.BasicFunctions import * 
from Utilities.GrandStaffFunctions import * 

#Import pygame for midi playback
import pygame

#Import time and system libraries
import datetime, time, os, sys

#Some version checkers
print("You are running Python", sys.version)
print("Python is located in: ", sys.path[1])

#Initialize Pygame
pygame.init()

##########################################################################
#Develop the grand staff
##########################################################################


#General format for note properties to be used when making songs
# note_properties = {"Letter":"C", "Octave":7, "Diatonic":3,"midi_pitch","midi_time","midi_duration","midi_volume"}




#Defining some functions here:


#Now we shall try sweeping through the song
Song_Key = "D"
Song_LowestTonic = "D-2"
Song_Tonality = "Major"
Song_Diatonic_Chromatics = [0,2,4,5,7,9,11] #In chromatic indices, this is the Major Scale sequence
Song_Diatonic_Degrees = [0,1,2,3,4,5,6] #Seven degrees in standard music
grand_staff = create_grand_staff();
[Song_Diatonic_List,Song_Octave_List,Song_Diatonic_Range,Song_Diatonic_List_Indices] = create_diatonic_map(grand_staff,Song_LowestTonic,Song_Diatonic_Chromatics)

import pdb
pdb.set_trace()

class MotifBasics(object):

    def __init__(self, MotifName):
        self.MotifName = MotifName
        return None
    
    def add_motif_lick(self):
        return None
        #Random number of motif elements  



# Alrighty, just to test how this works, let's just hard code stuff in now
CanonD = MIDIFile(1) #Just one track
track = 0
time = 0
totalbeats = 1024
filename = "Output_MIDI\CanonD.mid"
CanonD.addTrackName(track,time,"Sample Track")
CanonD.addTempo(track,time, 60) #Canon in D is 60 BPM

Bass_Motif = ['D2','A1','B1','F#1','G1','D1','G1','A1']

# Add a note. addNote expects the following information:
channel = 0
duration = 2
volume = 100

for _ in range(10):
    for pitch in Bass_Motif:
        CanonD.addNote(track,channel,grand_staff[pitch],time,duration,volume)
        time = time + duration

        


#Next Voice! Let's do low trebles now!
Treble_Low = ['F#3','A2','E3','A2','D3','F#2','C#3','F#2','B2','D2','A2','D2','B2','E2','C#3','G2']
channel = 1
time = 16 # Comes in after 2 periods
duration = 1
volume = 60

for _ in range(9):
    for pitch in Treble_Low:
        CanonD.addNote(track,channel,grand_staff[pitch],time,duration,volume)
        time = time + duration

#How about some chords?
Treble_Chords = [['F#2','A2','D2'],['C#3','E3','A3'],['B2','D2','F#2'],['A2','C#3','F#3'],['G2','B2','D3'],['D2','F#2','A2'],['D2','G2','B2'],['A2','C#3','E3']]
channel = 2
time = 32
duration = 2
for _ in range(8):
    for row in Treble_Chords:
        print("Row = ",row)
        for column in row:
            print("Column = ",column)
            CanonD.addNote(track,channel,grand_staff[column],time,duration,volume)
        time = time + duration

# #Next section!
# channel = 0
# time = 64
# duration = 1
# volume = 100
# Bass_Motif = ['D2','A2','A1','E2','B1','F#2','F#1','C#2','G1','D2','D1','A1','G1','D2','A1','E2']
# for _ in range(2):
    # for pitch in Bass_Motif:
        # CanonD.addNote(track,channel,grand_staff[pitch],time,duration,volume)
        # time = time + duration
        
#Let's do the high part now
channel = 3
time = 64
duration = 0.5
volume = 100
Treble_High = ['D4','C#4','D4','D3','C#3','A3','E3','F#3','D3','D4','C#4','B3','C#4','F#4','A4','B4','G4','F#4','E4','G4','F#4','E4','D4','C#4','B3','A3','G3','F#3','E3','B3','A3','G3']
for _ in range(4):
    for pitch in Treble_High:
        CanonD.addNote(track,channel,grand_staff[pitch],time,duration,volume)
        time = time + duration  
        
# And write it to disk.
midi_binfile = open(filename, 'wb')
CanonD.writeFile(midi_binfile)
midi_binfile.close()

count_down(5,'Opening file using Pygame')
music_file = filename
freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

try:
    play_music(music_file,-1,0)
except KeyboardInterrupt:
    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit



