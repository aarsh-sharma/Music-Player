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
#import pygame

fileName = []
k = 0

window = Tk()
window.wm_title("Media Player")
T = Text(window, height=30, width=60)
T.pack()

pyglet.options['audio'] = ('pulse','openal','silent')
player = pyglet.media.Player()

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
	return list(parentDiv.children)[12].get_text()

def playMusic():
	# music = pyglet.media.load(fileName)
	# music.play()
	# pyglet.app.run()
	# pygame.mixer.music.play()
	player.play()

def pauseMusic():
	# pygame.mixer.music.stop()
	player.pause()

def nextMusic():
	player.next()

def browsefunc():
	global fileName
	global player
	global k
	global songName
	filePath = askopenfilename(parent=window)
	fileName.append(filePath)
	music = pyglet.media.load(fileName[k])
	player.queue(music)

	# pygame.mixer.music.load(filename[k])
	p = Path(fileName[k])
	songName = p.name
	lyrics = lyricsScratch(songName)
	#print type(lyrics)
	indexLyricsNotReq = lyrics.find('if  (')
	if indexLyricsNotReq != -1:
		lyrics = lyrics[0:indexLyricsNotReq]	
	T.insert(END, lyrics)
	k = k+1
	#print filename
	
openSong = Button(window, text ="open", command = browsefunc)
play = Button(window, text ="play", command = playMusic)
pause = Button(window, text ="pause", command = pauseMusic)
next = Button(window, text ="next", command = nextMusic)
#pyglet.app.run()


next.pack()
play.pack()
pause.pack()
openSong.pack()
window.mainloop()