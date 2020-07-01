import tkinter as tk

import socket
import threading
import requests

import os
import shutil

import time
import datetime
from datetime import datetime

from resources.dbaccess_webApp import webApp_start_externscript
from resources.dbaccess_webApp import shutdown_server


windowwidth = 500
windowheight = 350

class webAppStarter:
	def __init__(self, master):
		self.canvas = tk.Canvas(master, width=windowwidth, height=windowheight)
		self.canvas.pack()

		self.topframe = tk.Frame(master, bg='#5ac8fa')
		self.topframe.place(x=0, y=0, relwidth=1, height=200)

		self.centerframe = tk.Frame(master, bg = 'white')
		self.centerframe.place(x=0, y=200, relwidth=1, height=105)

		self.bottomframe = tk.Frame(master, bg = '#5ac8fa')
		self.bottomframe.place(x=0, y=305, relwidth=1, height=45)

		self.iconimg = tk.PhotoImage(file="resources/icon.gif")
		self.icon = tk.Label(self.topframe, image = self.iconimg, width = 190, height = 190)
		self.icon.place(x = 500-200-20, y = 0)

		self.iplabel = tk.Label(self.centerframe, text=get_IP(), anchor='e', bg='white')
		self.iplabel.place(x=160, y = 25, width=100)

		self.iplabel_static = tk.Label(self.centerframe, text="Lokale IP-Adresse:", bg='white')
		self.iplabel_static.place(x=10, y=25)

		self.statuslabel = tk.Label(self.centerframe, text="", anchor='e', bg='white')
		self.statuslabel.place(x=160, y = 65, width=100)

		self.button_start = tk.Button(self.centerframe, text="Web-Zugriff starten", command=self.button_start_clicked)
		self.button_start.place(x=500-220, y=25, width=200)

		self.button_stop = tk.Button(self.centerframe, text="Web-Zugriff stoppen", command=self.button_stop_clicked)
		self.button_stop.place(x=500-220, y=65, width=200)

		self.button_check = tk.Button(self.centerframe, text="Verbindung checken", command=self.button_check_clicked)
		self.button_check.place(x=20, y=65, width=150)

		self.lastbackuplabel_static = tk.Label(self.bottomframe, text="Letzte Sicherungskopie der Datenbank:", fg='white', bg='#5ac8fa')
		self.lastbackuplabel_static.place(x=20, y=10)

		lastbackuplabeltext =  lastbackup[8:10] +"."+lastbackup[5:7] +"." + lastbackup[0:4] +", " + lastbackup[11:13] + ":" + lastbackup[14:16] + ":" +lastbackup[17:19] + " Uhr"

		self.lastbackuplabel = tk.Label(self.bottomframe, text=lastbackuplabeltext, fg='white', bg='#5ac8fa', anchor='e')
		self.lastbackuplabel.place(x=500-200-20, y=10, width=200)

	def button_start_clicked(self):
		self.statuslabel.config(text="")
		thr = threading.Thread(target=webApp_start_externscript, args=[True])
		thr.start()

	def button_stop_clicked(self):
		self.statuslabel.config(text="")
		try:
			r = requests.get('http://localhost:5000/shutdown')
		except:
			print("konnte nicht heruntergefahren werden, vielleicht bereits down?")

	def button_check_clicked(self):
		self.statuslabel.config(text="")
		try:
			r = requests.get('http://localhost:5000/')
			print(r.status_code)
			# self.statuslabel.text = "verbunden"
			self.statuslabel.config(text="verbunden", fg='green')
		except:
			# self.statuslabel.text = "getrennt"
			self.statuslabel.config(text="getrennt", fg='red')

def get_IP():
	try:
		returnvalue = ""
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		returnvalue=(s.getsockname()[0])
		s.close()
		return returnvalue
	except:
		return "offline"


def makebackupofdb(timestamp):
	newfilename = 'db-'+timestamp+'.db'
	newfilepath = r'db-backups/' + newfilename
	original = 'db.db'
	target = r'db-backups/db2.db'
	target = newfilepath
	try:
		shutil.copyfile(original, target)
	except:
		print("Backup nicht moeglich: Ordner evtl. nicht vorhanden?")


# Start des Python-Skripts:

# Zeitstempel anlegen und damit Backup der DB erzeugen
timestamp = datetime.now(tz=None)
timestampreadable = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
makebackupofdb(timestampreadable)

# letztes Backup anzeigen
arraywithbackups = os.listdir('db-backups')
arraywithbackups.sort(reverse=True)
lastbackup = str(arraywithbackups[0])
lastbackup = lastbackup[3:-3]

# Start der GUI:
root = tk.Tk()
root.title("Clubcard Balance Manager: webAppStarter")
root.minsize(windowwidth,windowheight)
root.maxsize(windowwidth,windowheight)
m = webAppStarter(root)
root.mainloop()