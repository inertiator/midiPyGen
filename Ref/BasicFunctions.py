import datetime, time, os
#Import pygame for midi playback
import pygame

# Simple countdown timer if we need to break
def count_down(n,statement):
    for i in reversed( range(n) ):
        print('Starting in: ',i)
        time.sleep(1)
    print(statement)

    
#Simple function in OS that opens mid file (using application name fed in) and closes the process after the length of the file
def start_file(filename,length,application):
    
    os.startfile(filename)
    time.sleep(length)


def play_music(music_file,loops,start):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play(loops,start)
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)
