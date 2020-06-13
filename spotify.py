import spotipy
import spotipy.util as util
import time
import os
import subprocess
import psutil
import traceback
import spotipy.oauth2
import pynput
import win32gui, win32com.client
from pynput.keyboard import Key, Controller
# Add your spotify username
username = ''
#Scope to view the playing song
scope = 'user-read-currently-playing'
#Add your client ID from Spotify Dev 
client_id=''
#Add your client secret from Spotify Dev
client_secret=''
redirect_uri='http://localhost:8080/callback'




#script has a bunch of time.sleep, if it seems to take too long try changing these values


#spotify authenticator / manages tokens as well
sp=spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
	username=username, 
	client_id=client_id, 
	client_secret=client_secret,
	redirect_uri=redirect_uri,
	scope=scope))



def relaunchSpotify():

	keyboard = Controller()

	#Finds all PIDs with the name Spotify 
	for proc in psutil.process_iter():
		if any(procstr in proc.name() for procstr in ['Spotify']):
			try:
				#Kills all processes of spotify
				proc.kill
			#sometimes the process will already be gone 
			except psutil.NoSuchProcess:
				pass
	#when relaunched the window gets focused which is kinda annoying
	#gets active window before launch
	activewindow = get_active_window()
	#Wait time may not be necessary 
	time.sleep(0.5)
	#Opens spotify
	subprocess.call(["Spotify.exe"])
	#Issue with win32gui where you need to send the alt key in order for setforegroundwindow to work
	shell = win32com.client.Dispatch("WScript.Shell")
	shell.SendKeys('%')
	#sets active window to what was before spotify opening
	win32gui.SetForegroundWindow(activewindow)
	#Wait for the spotify app to load 
	time.sleep(0.5)
	#Spotify relaunches with previous song
	keyboard.press(Key.media_next)

	


def get_active_window():
	#just gets the current active window
    activewindow = None
    window = win32gui.GetForegroundWindow()
    return window


def checkAd():
	current = sp.current_user_playing_track()
	empty = ''
	if(current == None):
		print("No music playing", end="\r")
		#had to return something 
		return empty, empty
	else:
		if("ad" in current['currently_playing_type']):
			return True, current
		else:
			return False, current


def main(): 
	#Status of song, and the dictionary that the api returns
	isplaying, info = checkAd()
	#If song is ad then reluanch spotify
	if(isplaying == True):
		relaunchSpotify()
		print("Relaunching Spotify", end="\r")
		return
	if(isplaying is False):
		if(info['item'] is not None):
			song = info['item']['name']
			duration = info['item']['duration_ms']
			progress = info['progress_ms']
			status = info['is_playing']
			percent = (progress/duration)*100
			# Printing multiple times with spaces to account for CMD print overflow
			print("Playing", '"'+song+'"', "Progress:", str(round(percent, 1))+"%",
			 " Song is playing", status, end="\r", flush=True)
			print("                                                                                                            ", end="\r")
			print("Playing", '"'+song+'"', "Progress:", str(round(percent, 1))+"%",
			 " Song is playing", status, end="\r", flush=True)
			#arbitrary sleep time
			time.sleep(1)
		else:
			#arbitrary sleep time
			time.sleep(2)

	else:
		#arbitrary sleep time
		time.sleep(2)




while(True):
	try:
		main()
	#tried to do some error catching
	except RuntimeError:
		print(traceback.format_exc())
	except KeyboardInterrupt:
		exit()

