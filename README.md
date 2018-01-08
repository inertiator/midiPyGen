# midiPyGen
midiPyGen is intended to be a Python-MIDI interface and songwriter with capability of expansion.
Currently development is being made in the "Backbone" branch.

## Libraries Needed
midiPyGen links Python and MIDI together with the help of the library MIDIUtil 1.1.3 (2017-03-06). With that capability, all that's left to do is to program the inputs to the MIDI environment, including: tracks, channels, and time signature.

## Subcomponents of a Song
A song can be decomposed into various parts, such as:
1) Tonality
2) Time Signature and Rhythm
3) Instruments and Ensemble
4) Chord Progression, Accompaniment, and Form
5) Motif and Melody

Different genres of music use different flavors of these parts. A 16th century classical piece would vary widely from a 1960s rock ballad, but they all contain elements of these subcomponents.

## Current Features
1) Creation of a multi-part harmony (1 chord per measure) with a chosen chord progression (or 'cadence')
2) Genetic Algorithm method to minimize diatonic jumps between chords and instruments
3) Simple but very powerful method to represent chords and can represent most chord progressions.
   -  Triad Chords (e.g. Key of C, Chord '2' is D minor)
   -  Seventh Chords based on diatonics (e.g. Key of C, Chord '5S' is G7, but Chord '4S' is Fmaj7)
   -  Borrowed Chords (e.g. Key of C, Chord 5B5 is D7 [C-->key 5 = G, diatonic 5 = D7], Chord 5B4 is C7 [C-->key 4 = F, diatonic 5 = C7])
      -  Can be stacked: 4B4B4 is Eb [C-->key 4 = F-->key 4 = Bb, diatonic 4 = Eb]
      -  Borrowed chords are always sevenths, unless chord is diatonic 4
      -  Seventh chords are only used in ensembles > 3 + bass
4) Scalable harmony creation method, can be applied to different ensemble sizes (create with Ensemble.py, minimum of 3 + bass instruments)
5) Able to vary Key Signature, Tonality (Major/Minor), and Tempo

## How to Run
runMidiPyGen.py should be the only input needed to run.

## Plans
midiPyGen aims to be a constantly growing system of different capabilities.
1) Melody generation from an accompaniment
2) Rhythm implementation to accompaniment
3) Accompaniment generation from melody  
4) Percussion parts
5) Form
6) Augmented and Diminished Chords

Here's to see if something cool comes out of this!
