# getestet mit USB-Lesegeraet "KKmoon 14443A", dabei auszuwaehlendes Format: "8h{sz}e" (Nr. 3), dann byteweise tauschen


import tkinter as tk
from tkinter import messagebox

from resources.dbaccess_local import transferamount
from resources.dbaccess_local import getbalance


windowwidth = 350
windowheight = 700


currentTransaction=0.0
amount_euros_string="0"
amount_cents_string="00"	
amount_string = amount_euros_string + "." + amount_cents_string
in_cents = 0 	# Hilfsvariable zur Bestimmung der Cursor-Position (bei 3 erfolgt keine weitere Eingabe)



class LocalBalanceManager:
	currentUID=""

	def __init__(self, master):
		self.canvas = tk.Canvas(master, width=windowwidth, height=windowheight)
		self.canvas.pack()

		self.topframe = tk.Frame(master, bg='#ff9d00')
		self.topframe.place(x=0, y=0, relwidth=1, height=200)

		self.centerframe = tk.Frame(master, bg = 'black')
		self.centerframe.place(x=0, y=200, relwidth=1, height=100)

		self.bottomframe = tk.Frame(master, bg = '#555555')
		self.bottomframe.place(x=0, y=290, relwidth=1, height=400)


		self.clubcardInputField = tk.Text(self.topframe, wrap='none', font=("Arial", 22))
		self.clubcardInputField.place(x=10, y=10, width=290, height = 50)
		
		self.clubcardInputFieldReset = tk.Button(self.topframe, anchor='c', text='\u2327', bg='#ff9d00', fg='black', font=("Arial", 20), highlightthickness = 0, bd = 0, command=lambda: self.clubcardfieldreset())
		self.clubcardInputFieldReset.place(x=310, y=10, width=30, height=50)

		self.clubcardInputField.bind("<Key>", self.check_key)
		# self.clubcardInputField.bind("<KeyRelease>", self.update_width)
		self.clubcardInputField.focus_set()


		self.descriptionLabel = tk.Label(self.topframe, anchor='sw', text="Guthaben:", bg='#ff9d00', fg='black', font=("Arial", 10))
		self.descriptionLabel.place(x=10, y=64, width=80, height=60)

		self.guthabenLabel = tk.Label(self.topframe, anchor='se', text="keine ID", bg='#ff9d00', fg='black', font=("Arial bold", 44))
		self.guthabenLabel.place(x=90, y=70, width=250, height=60)


		self.button_aufladen = tk.Button(self.topframe, anchor='w', text='aufladen (+)', bg='#ff9d00', fg='#3d9a40', font=("Arial", 20), highlightthickness = 0, bd = 0, command=lambda: aufladen(self.currentUID, float(amount_string)))
		self.button_aufladen.place(x=10, y=130, width=150)

		self.button_belasten = tk.Button(self.topframe, anchor='e', text='belasten (-)', bg='#ff9d00', fg='#b43300', font=("Arial", 20), highlightthickness = 0, bd = 0, command=lambda: belasten(self.currentUID, -float(amount_string)))
		self.button_belasten.place(x=190,y=130, width=150)


		self.transaktionLabel = tk.Label(self.centerframe, anchor='se', text="0.00", bg='black', fg='white', font=("Arial bold", 44))
		self.transaktionLabel.place(x=90, y=20, width=250, height=60)

		self.cleartransactionbutton = tk.Button(self.centerframe, anchor='c', text="AC", bg='black', fg='white', font=("Arial", 20), highlightthickness = 0, bd = 0, command=lambda: self.numpad_click_ac())
		self.cleartransactionbutton.place(x=0, y=0, relwidth=1/3, height=100)




		self.button_9 = tk.Button(self.bottomframe, anchor='c', text="9", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(9))
		self.button_9.place(x=2*350/3, y=0*400/4, relwidth=1/3, relheight=1/4)

		self.button_8 = tk.Button(self.bottomframe, anchor='c', text="8", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(8))
		self.button_8.place(x=1*350/3, y=0*400/4, relwidth=1/3, relheight=1/4)

		self.button_7 = tk.Button(self.bottomframe, anchor='c', text="7", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(7))
		self.button_7.place(x=0*350/3, y=0*400/4, relwidth=1/3, relheight=1/4)

		self.button_6 = tk.Button(self.bottomframe, anchor='c', text="6", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(6))
		self.button_6.place(x=2*350/3, y=1*400/4, relwidth=1/3, relheight=1/4)

		self.button_5 = tk.Button(self.bottomframe, anchor='c', text="5", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(5))
		self.button_5.place(x=1*350/3, y=1*400/4, relwidth=1/3, relheight=1/4)

		self.button_4 = tk.Button(self.bottomframe, anchor='c', text="4", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(4))
		self.button_4.place(x=0*350/3, y=1*400/4, relwidth=1/3, relheight=1/4)

		self.button_3 = tk.Button(self.bottomframe, anchor='c', text="3", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(3))
		self.button_3.place(x=2*350/3, y=2*400/4, relwidth=1/3, relheight=1/4)

		self.button_2 = tk.Button(self.bottomframe, anchor='c', text="2", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(2))
		self.button_2.place(x=1*350/3, y=2*400/4, relwidth=1/3, relheight=1/4)

		self.button_1 = tk.Button(self.bottomframe, anchor='c', text="1", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(1))
		self.button_1.place(x=0*350/3, y=2*400/4, relwidth=1/3, relheight=1/4)

		self.button_delete = tk.Button(self.bottomframe, anchor='c', text="\u232b", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: self.numpad_click_delete())
		self.button_delete.place(x=2*350/3, y=3*400/4, relwidth=1/3, relheight=1/4)

		self.button_dot = tk.Button(self.bottomframe, anchor='c', text=".", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: self.numpad_click_comma())
		self.button_dot.place(x=1*350/3, y=3*400/4, relwidth=1/3, relheight=1/4)

		self.button_0 = tk.Button(self.bottomframe, anchor='c', text="0", bg = '#555555', fg='white', font=("Arial", 30), highlightthickness = 0, bd = 0, command=lambda: numpad_click_number(0))
		self.button_0.place(x=0*350/3, y=3*400/4, relwidth=1/3, relheight=1/4)


	# Event nach 'Return' key -> Guthaben abfragen
	def check_key(self, event):
		if event.keysym == "Return":
			text = self.clubcardInputField.get(1.0, tk.END)[:-1]
			# print(UIDbyteweisetauschen(text))
			print(len(text))
			if ":" not in text and len(text)==14: #wenn kein : im String ist und Laenge = 14 Wahrscheinlichkeit gross, dass Eingabe ueber RFID Reader erfolgt ist und Umrechnung erfolgen muss
				self.clubcardInputField.delete("1.0", "end") #"1.0" und "end" beziehen sich auf das erste Zeichen und das letzte Zeichen des Inhalts 
				self.clubcardInputField.insert("end", UIDbyteweisetauschen(text))
				self.currentUID=UIDbyteweisetauschen(text)
			else:
				self.currentUID=text
			# print(self.currentUID)
			root.focus_set()
			aktuellesGuthaben=getbalance(self.currentUID)
			aktuellesGuthaben_float=float(aktuellesGuthaben)
			aktuellesGuthaben = "{:.2f}".format(aktuellesGuthaben_float) #string auf zwei Nachkommastellen
			# print(aktuellesGuthaben)
			self.guthabenLabel.config(text=aktuellesGuthaben)
			return "break"

	def numpad_click_comma(self):
		global in_cents
		# print("Numpad_Button comma clicked!")
		in_cents = 1
		# print("in_cents: "+str(in_cents))

	def numpad_click_delete(self):
		# print("Numpad_Button del clicked!")
		global amount_euros_string
		global amount_cents_string
		global amount_string
		global in_cents
		if in_cents == 3:
			amount_cents_string = amount_cents_string[:1]
			amount_string = amount_euros_string + "." + amount_cents_string + "0"
			in_cents = 2
			# print("in_cents: "+str(in_cents))
		elif in_cents == 2:
			amount_cents_string = amount_cents_string[:0]
			amount_string = amount_euros_string + "." + amount_cents_string + "00"
			in_cents = 1
			# print("in_cents: "+str(in_cents))
		elif in_cents == 1:
			amount_cents_string = "00"
			amount_string = amount_euros_string + "." + amount_cents_string
			in_cents = 0
			# print("in_cents: "+str(in_cents))
		elif in_cents == 0:
			amount_euros_string = amount_euros_string[:-1]
			if amount_euros_string == "":
				amount_euros_string = "0"
			amount_string = amount_euros_string + "." + amount_cents_string
		m.transaktionLabel.config(text=amount_string)
		currentTransaction=float(amount_string)
		# print(currentTransaction)

	def numpad_click_ac(self):
		# print("Numpad_Button AC clicked!")
		global amount_euros_string
		global amount_cents_string
		global amount_string
		global in_cents
		amount_euros_string = "0"
		amount_cents_string = "00"
		amount_string = amount_euros_string + "." + amount_cents_string
		in_cents = False
		m.transaktionLabel.config(text=amount_string)
		currentTransaction=float(amount_string)
		# print(currentTransaction)

	def clubcardfieldreset(self):
		self.clubcardInputField.delete("1.0", "end") #"1.0" und "end" beziehen sich auf das erste Zeichen und das letzte Zeichen des Inhalts 
		self.guthabenLabel.config(text="keine ID")
		self.clubcardInputField.focus_set()

		
def numpad_click_number(number_clicked):
	global amount_euros_string
	global amount_cents_string
	global amount_string
	global in_cents
	if in_cents == 0:
		if amount_euros_string == "0":
			amount_euros_string = ""
		amount_euros_string+=str(number_clicked)
		amount_string = amount_euros_string + ".00"
	elif in_cents == 1:
		amount_cents_string = str(number_clicked)
		amount_string = amount_euros_string + "." + amount_cents_string + "0"
		in_cents = 2
	elif in_cents == 2:
		amount_cents_string += str(number_clicked)
		amount_string = amount_euros_string + "." + amount_cents_string
		in_cents = 3
	m.transaktionLabel.config(text=amount_string)
	currentTransaction=float(amount_string)
	# print(currentTransaction)


def UIDbyteweisetauschen(data):
	UID=""
	UID=UID+data[12:14]+":"+data[10:12]+":"+data[8:10]+":"+data[6:8]+":"+data[4:6]+":"+data[2:4]+":"+data[0:2]
	UID=UID.upper()
	return(UID)

def on_closing():
	# if messagebox.askokcancel("Beenden?", "Soll der 'Clubcard Balance Manager' wirklich beendet werden?"):
		# try:
		# 	r = requests.get('http://localhost:5000/shutdown')
		# except:
		# 	print("")
		root.destroy()

def on_keypress(event):
	if "!frame.!text" not in str(event.widget): #nur wenn kein Textfeld ausgewaehlt ist
		# print(event.char) #welche Taste wurde geklickt?
		if (event.char in ["0","1","2","3","4","5","6","7","8","9"]): #wenn geklickte Taste eine Nummer ist
			numpad_click_number(int(event.char))
		elif event.char in [",","."]:
			m.numpad_click_comma()
		elif event.char in ["c","a"]:
			m.numpad_click_ac()
		elif event.char == "x":
			m.clubcardfieldreset()
		elif event.char == "-":
			belasten(m.currentUID, -float(amount_string))
		elif event.char == "+":
			aufladen(m.currentUID, float(amount_string))

def on_backspace(event): # analog zu on_keypress
	if "!frame.!text" not in str(event.widget): #nur wenn kein Textfeld ausgewaehlt ist
		m.numpad_click_delete()


def aufladen(UID, amount):
	if m.guthabenLabel.cget("text") != "keine ID" and m.transaktionLabel.cget("text") != "0.00":
		if messagebox.askokcancel("Clubkarte aufladen?", "Soll der Clubkarte "+UID+" wirklich " + str(amount)+ " gutgeschrieben werden?"):
			transferamount(UID, amount)
			m.guthabenLabel.config(text="keine ID")
			m.clubcardInputField.delete("1.0", "end") #"1.0" und "end" beziehen sich auf das erste Zeichen und das letzte Zeichen des Inhalts 
			m.clubcardInputField.focus_set()
			numpadzuruecksetzen()


def belasten(UID, amount):
	if m.guthabenLabel.cget("text") != "keine ID" and m.transaktionLabel.cget("text") != "0.00":
		if messagebox.askokcancel("Clubkarte aufladen?", "Soll die Clubkarte "+UID+" wirklich mit "+ str(-amount) +" Euro belastet werden?"):
			transferamount(UID, amount)
			m.guthabenLabel.config(text="keine ID")
			m.clubcardInputField.delete("1.0", "end") #"1.0" und "end" beziehen sich auf das erste Zeichen und das letzte Zeichen des Inhalts 
			m.clubcardInputField.focus_set()
			numpadzuruecksetzen()

def numpadzuruecksetzen():
	global amount_euros_string
	global amount_cents_string
	global amount_string
	global in_cents
	globalcurrentTransaction=0.0
	amount_euros_string="0"
	amount_cents_string="00"	
	amount_string = amount_euros_string + "." + amount_cents_string
	in_cents = 0
	m.transaktionLabel.config(text="0.00")
 

# Start der GUI:
root = tk.Tk()
root.title("Clubcard Balance Manager: Local Access")
root.minsize(windowwidth,windowheight)
root.maxsize(windowwidth,windowheight)
m = LocalBalanceManager(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind('<KeyPress>', on_keypress)
root.bind("<BackSpace>", on_backspace)
root.mainloop()
