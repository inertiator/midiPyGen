###################################################################################
# A hopefully successful code that combines elements of randomness and music theory
# Date: 5/2016
# Version: As many zeros as possible
###################################################################################

#Import the libraries. We're taking in our Midi generator (MIDIUtil), and our MIDI player ()
from MIDIUtil_Base.midiutil.MidiFile3 import MIDIFile
from Functions.BasicFunctions import * 

#Import pygame for midi playback
import pygame

#Import time and system libraries
import datetime, time, os, sys

#Some version checkers
print("You are running Python", sys.version)
print("Python is located in: ", sys.path[1])

#Initialize Pygame
pygame.init()

# Create the MIDIFile Object
MyMIDI = MIDIFile(1)

# Add track name and tempo. The first argument to addTrackName and
# addTempo is the time to write the event.
midi_track = 0
midi_time = 0
MyMIDI.addTrackName(midi_track,midi_time,"Sample Track")
MyMIDI.addTempo(midi_track,midi_time, 160)

# Add a note. addNote expects the following information:
midi_channel = 0
midi_pitch = 60
midi_duration = 1
midi_volume = 100

# Now add the note.
MyMIDI.addNote(midi_track,midi_channel,midi_pitch,midi_time,midi_duration,midi_volume)

# And write it to disk.
midi_binfile = open("Output_MIDI\output.mid", 'wb')
MyMIDI.writeFile(midi_binfile)
midi_binfile.close()

count_down(5,'Opening file using default player')
music_file = "Output_MIDI\output.mid"
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