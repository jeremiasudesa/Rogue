from pygame import mixer
import os
import vars
import random

#Instantiate mixer
mixer.init()
music_channel = mixer.Channel(0)
#Set preferred volume
music_channel.set_volume(0.1)

def play_song(path):
    #Load audio file
    song = mixer.Sound(os.path.join('resources', path))
    #song length in miliseconds
    songlen = int(song.get_length()*1000)+1
    #Play the music
    mixer.Channel(0).play(song, 0, songlen, 2000)

def rand_music(path):
    num = random.randint(0, vars.SONGFREQ)
    if(num == 0 and music_channel.get_busy() == False):
        play_song(path)