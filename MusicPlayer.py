#import tkinter
from Tkinter import *
from tkFileDialog import *
import pyglet
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import urllib2
import googlesearch
import time  
from time import sleep  
import player
#import pygame

fileName = []
songName = []
k = 0
player = pyglet.media.Player()
FORWARD_REWIND_JUMP_TIME = 10

def playMusic():
	player.play()
	# if source: #lyrics
	# 	if player.time == source.duration-1:
	# 		showLyrics()

def pauseMusic():
	player.pause()

def nextMusic():
	player.next()
	if source: # if player.queue not empty
		showLyrics()
	
def add_to_queue(audio_file):
	global source
	source = pyglet.media.load(audio_file)
	player.queue(source)
	print(source)

def reset_player():
	player.pause()
	player.delete()

def is_playing():
	try:
		elapsed_time = int(player.time)
		is_playing = elapsed_time < int(track_length)
	except:
		is_playing = False
	return is_playing

def seek(time):
	try:
		player.seek(time)
	except AttributeError:
		pass

@property
def track_length():
	try:
		return source.duration
	except AttributeError:
		return 0

@property
def volume():
	return player.volume

@property
def elapsed_play_duration():
	return player.time

# @volume.setter
# def volume(volume):
# 	player.volume = volume

def stop():
	reset_player()

def mute():
	player.volume = 0.0

def unmute(newvolume_level):
	player.volume = newvolume_level

def fast_forward():
	time = player.time + FORWARD_REWIND_JUMP_TIME
	try:
		if source.duration > time:
			seek(time)
		else:
			seek(source.duration)
	except AttributeError:
		pass

def rewind():
	time = player.time - FORWARD_REWIND_JUMP_TIME
	try:
		seek(time)
	except:
		seek(0)

def lyricsScratch(songName):
	query = songName + ' az lyrics'
	for j in googlesearch.search(query, tld='com', lang='en', num=10, stop=1, pause=2.0):
		print(j)
		if 'https://www.azlyrics.com/lyrics/' in j:
				link = j
				print j+' hi'
				break
	
	#manager = urllib3.PoolManager()
	#page = manager.request('GET',link)
	# page = requests.get('https://www.azlyrics.com/lyrics/shayneward/nopromises.html')
	page=urllib2.urlopen(link)
	soup = BeautifulSoup(page, 'html.parser')

	parentDiv = soup.find('div',class_ = 'col-xs-12 col-lg-8 text-center')
	#print parentDiv
	lyrics = list(parentDiv.children)[12].get_text()
	indexLyricsNotReq = lyrics.find('if  (')
	if indexLyricsNotReq != -1:
		lyrics = lyrics[0:indexLyricsNotReq]
	return lyrics

def browsefunc():
	global fileName
	global player
	global songName,k
	filePath = askopenfilename(parent=window)
	fileName.append(filePath)
	add_to_queue(filePath)
	if k==0:
		showLyrics()

	# pygame.mixer.music.load(filename[k])
def showLyrics():
	global k
	p = Path(fileName[k])
	songName.append(p.name)
	lyrics = lyricsScratch(songName[k])
	#print type(lyrics)
	T.configure(state='normal')	
	T.delete('1.0',END)
	T.insert(END, lyrics)
	T.configure(state='disabled')
	k = k+1
	#print filename
	
if __name__ == '__main__':
	window = Tk()
	window.resizable(width=False, height=False)
	pyglet.options['audio'] = ('pulse','openal','silent')
	
	openSong = Button(window, text ="open", command = browsefunc)
	play_button=PhotoImage(file='play-button.png')
	play = Button(window, image = play_button, command = playMusic)
	pause = Button(window, text ="pause", command = pauseMusic)
	next = Button(window, text ="next", command = nextMusic)

	T = Text(window,state = 'disabled', height=30, width=60)
	window.wm_title("Media Player")
	T.pack()
	
	next.pack()
	play.pack()
	pause.pack()
	openSong.pack()
	window.mainloop()

#pyglet.app.run()
