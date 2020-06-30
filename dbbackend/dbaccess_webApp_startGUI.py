import tkinter as tk

import socket
import threading
import requests

import os

from dbaccess_webApp import webApp_start_externscript
from dbaccess_webApp import shutdown_server


windowwidth = 500
windowheight = 500

class webAppStarter:
	def __init__(self, master):
		self.canvas = tk.Canvas(master, width=windowwidth, height=windowheight)
		self.canvas.pack()

		self.topframe = tk.Frame(master, bg='#5ac8fa')
		self.topframe.place(x=0, y=0, relwidth=1, height=200)

		self.bottomframe = tk.Frame(master, bg = 'white')
		self.bottomframe.place(x=0, y=200, relwidth=1, relheight=300)

		self.iconimg = tk.PhotoImage(file="icon.gif")
		self.icon = tk.Label(self.topframe, image = self.iconimg, width = 190, height = 190)
		self.icon.place(x = 500-200-20, y = 0)

		self.iplabel = tk.Label(self.bottomframe, text=get_IP(), anchor='e')
		self.iplabel.place(x=160, y = 40, width=100)

		self.iplabel_static = tk.Label(self.bottomframe, text="Lokale IP-Adresse:")
		self.iplabel_static.place(x=20, y=40)

		self.statuslabel = tk.Label(self.bottomframe, text="", anchor='e')
		self.statuslabel.place(x=160, y = 80, width=100)

		# self.statuslabel_static = tk.Label(self.bottomframe, text="Verbindungs-Status:")
		# self.statuslabel_static.place(x=20, y=80)

		self.button_start = tk.Button(self.bottomframe, text="Web-Zugriff starten", command=self.button_start_clicked)
		self.button_start.place(x=500-220, y=40, width=200)

		self.button_stop = tk.Button(self.bottomframe, text="Web-Zugriff stoppen", command=self.button_stop_clicked)
		self.button_stop.place(x=500-220, y=80, width=200)

		self.button_check = tk.Button(self.bottomframe, text="Verbindungs-Check", command=self.button_check_clicked)
		self.button_check.place(x=20, y=80, width=150)

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


arr = os.listdir()
print(arr)
root = tk.Tk()
root.title("Clubcard Balance Manager: webAppStarter")
root.minsize(windowwidth,windowheight)
root.maxsize(windowwidth,windowheight)
m = webAppStarter(root)
root.mainloop()