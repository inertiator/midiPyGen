import datetime, time, os
#Import pygame for midi playback
import pygame


##########################################################################
#Develop the grand staff
##########################################################################


#Function to create grand staff that returns table lookup for notes and octaves for all 127 tones
def create_grand_staff():

    grand_staff = {};
    stf_ctr = 0
    note_letters = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    note_octaves = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    note_diatonics = [1, 2, 3, 4, 5, 6, 7]

    for octaves in note_octaves:
        for letters in note_letters:
            grand_staff[str(letters)+str(octaves)] = stf_ctr
            stf_ctr += 1
            if stf_ctr >= 128:
                break
    return grand_staff
    
    
#Function to find keys from values            
def find_key(mydict,value):
    return str([ key for key,val in mydict.items() if val==value ])
  
#Function to create useful arrays of diatonics in our key
def create_diatonic_map(grand_staff,LowestTonic,Chromatics):
    
    LowestTonicValue = grand_staff[LowestTonic]
    DiatonicRange = {}
    DiatonicList = []
    DiatonicScale = []
    OctaveList = []
    NoteValue = LowestTonicValue
    NoteCtr = 0
    OctCtr = 0
    
    while NoteValue < 128:
        TonalNote = Chromatics[0] + 12*OctCtr + LowestTonicValue
        DiatonicRange[(find_key(grand_staff,TonalNote))] = []
        OctaveList.append(TonalNote)
        for diatonics, item in enumerate(Chromatics):
            NoteValue = Chromatics[diatonics] + 12*OctCtr + LowestTonicValue
            if NoteValue >= 128:
                break
            DiatonicList.append(NoteValue)
            DiatonicRange[(find_key(grand_staff,TonalNote))].append(NoteValue)
            NoteCtr += 1
        DiatonicScale = []
        OctCtr += 1
    return DiatonicList, OctaveList, DiatonicRange

        
    