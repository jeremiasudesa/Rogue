from pygame import mixer
import os

#Instantiate mixer
mixer.init()
music_channel = mixer.Channel(0)
#Set preferred volume
mixer.music.set_volume(0.01)

def play_song(path):
    #Load audio file
    song = mixer.Sound(os.path.join('resources', path))
    #song length in miliseconds
    songlen = int(song.get_length()*1000)+1
    #Play the music
    mixer.Channel(0).play(song, 0, songlen, 5000)