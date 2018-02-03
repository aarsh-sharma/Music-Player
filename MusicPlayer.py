from tkinter import *
import pyglet
from tkinter import filedialog as fd
from pathlib import Path
import googlesearch
from bs4 import BeautifulSoup
import urllib2
import threading

window= Tk()
player=pyglet.media.Player()
pyglet.options['audio'] = ('pulse', 'openal', 'silent')
filename = []
song = []
k = 0

T=Text(window,height=30,width=50)
def playSong(): 
	#pyglet.media.load()
	player.play()	

def pauseSong():
	player.pause()


def openSong():
	# player.queue("/home/sunidhi/Music/temp.mp3")
	global filename, k
	filename.append(fd.askopenfilename(parent=window))
	print filename[k]
	
	song.append(pyglet.media.load(filename[k]))
	player.queue(song[k])	
	#print filename
	p = Path(filename[k])
	songName = p.name
	print songName 
	lyrics=ssearch(songName)
	T.insert(INSERT, lyrics)
	k = k+1

def ssearch(songName):
	query = songName +" az lyrics"
	#print query
	songLink = ''
	for link in googlesearch.search(query,tld="com",lang='en',num=10,stop=1,pause=2.0):
		print(link)
		# temp = link.find("https://www.azlyrics.com/lyrics")
		# if temp != -1:
		# 	songLink = temp
		# 	print songLink
		# 	break
		if "https://www.azlyrics.com/lyrics" in link:
			songLink = link
			break
	print songLink

	page=urllib2.urlopen(songLink)
	soup = BeautifulSoup(page, 'html.parser')
	# print soup
	content=soup.find('div',class_="col-xs-12 col-lg-8 text-center")
	# print content
	# print list(content.children)
	return list(content.children)[12].get_text()
	
#A=Button(window, text="Play",command=t1.start())
#B=Button(window, text="Pause",command=t2.start())
A=Button(window, text="Play",command=playSong)
B=Button(window, text="Pause",command=pauseSong)
C=Button(window, text="OpenSong",command=openSong)

A.pack(padx=15, pady=5, side=LEFT)
B.pack(padx=20, pady=10, side=LEFT)
C.pack(padx=30,pady=45,side=LEFT)
T.pack()

window.mainloop()
#t1.join();t2.join()
