# midiPyGen
midiPyGen is intended to be a Python-MIDI interface and songwriter with capability of expansion.
Currently development is being made in the "Backbone" branch.

## Libraries Needed
MidiBot links Python and MIDI together with the help of the library MIDIUtil 1.1.3 (2017-03-06). With that capability, all that's left to do is to program the inputs to the MIDI environment, including: tracks, channels, and time signature.

## Subcomponents of a Song
A song can be decomposed into various parts, such as:
1) Tonality
2) Time Signature and Rhythm
3) Instruments and Ensemble
4) Chord Progression, Accompaniment, and Form
5) Motif and Melody

Different genres of music use different flavors of these parts. A 16th century classical piece would vary widely from a 1960s rock ballad, but they all contain elements of these subcomponents.

## Current Status
For this first pass, only a single method is completed. This method takes in a cadence or chord progression from the user and applies it to an indicated instrumentation.
1) Variation of Cadence (Currently using Plagal and Deceptive)
2) Variation of Chord Progression (Currently have Canon in D set up)
3) Variation of Key, Time Signature, and Mode (Major or Minor)

## How to Run
runMidiPyGen.py should be the only input needed to run.

## Plans
MidiBot aims to be a constantly growing system of different capabilities.
1) Addition of Forms
2) Melody generation from an accompinament
3) Accompinament generation from melody  

Here's to see if something cool comes out of this!
