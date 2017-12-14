###################################################################################
# A hopefully successful code that creates a Canon in D midi file
# Date: 5/2016
# Version: As many zeros as possible
###################################################################################

#Import the libraries. We're taking in our Midi generator (MIDIUtil), and our MIDI player ()
from MIDIUtil_Base.midiutil.MidiFile3 import MIDIFile
from Functions.BasicFunctions import * 
from Functions.GrandStaffFunctions import * 

#Import pygame for midi playback
import pygame

#Import time and system libraries
import datetime, time, os, sys

#Import the random library
import random

#Some version checkers
print("You are running Python", sys.version)
print("Python is located in: ", sys.path[1])

#Initialize Pygame
pygame.init()

#General format for note properties to be used when making songs
# note_properties = {"Letter":"C", "Octave":7, "Diatonic":3,"midi_pitch","midi_time","midi_duration","midi_volume"}


#Now we shall try sweeping through the song
Song_Title = "Random_Song"
Song_Key = "D"
Song_LowestTonic = Song_Key + "-2"
Song_Tonality = "Major"
Song_Tempo = 90 #90 beats per minute
Song_Diatonic_Chromatics = [0,2,4,5,7,9,11] #In chromatic indices, this is the Major Scale sequence
Song_Diatonic_Degrees = [0,1,2,3,4,5,6] #Seven degrees in standard music
grand_staff = create_grand_staff();
[Song_Diatonic_List,Song_Octave_List,Song_Diatonic_Range] = create_diatonic_map(grand_staff,Song_LowestTonic,Song_Diatonic_Chromatics)







#Now let's try just making a song!
Song = MIDIFile(1) #Just one track
track = 0
time = 0
filename = "Output_MIDI\\" + Song_Title + ".mid"
Song.addTrackName(track,time,"Sample Track")
Song.addTempo(track,time, Song_Tempo)
        
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



