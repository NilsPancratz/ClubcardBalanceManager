import sqlite3
import json

databasefile = 'db.db'
conn = sqlite3.connect(databasefile)

# Anlegen der Tabellen und ggf. der Datenbank (wenn nicht vorhanden):
def create_table():
	c = conn.cursor()
	c.execute("""
		CREATE TABLE transactions (
			clubcardID char(20),
			amount real,
			transactiontimestamp timestamp DEFAULT CURRENT_TIMESTAMP
			)""")
	conn.commit()
	c.execute("""
		CREATE TABLE clubcards (
			clubcardID int,
			balance real
			)""")
	conn.commit()
	conn.close()

# gibt einen JSON mit Clubkarten IDs, Guthaben und Transaktionen zurueck
def returnclubcardjson():
	c = conn.cursor()
	c.execute("SELECT * FROM clubcards NATURAL JOIN transactions ORDER BY clubcardid ASC, transactiontimestamp DESC;")
	# c.execute("SELECT * FROM clubcards NATURAL JOIN transactions ORDER BY clubcardid ASC, transactiontimestamp DESC")
	# Spalte 0: clubcardID, Spalte 1: amount, Spalte: transactiontimestamp
	db_data = c.fetchall()

	# Wenn keine Werte vorhanden, leeres Array zurueckgeben
	if len(db_data) == 0:
		return "[]"
	else:
		bufferstring = ""
		lastUID = ""
		for i in db_data:
			if i[0] != lastUID:
				lastUID = i[0]
				# loesche zunaechst das letzte Komma
				bufferstring = bufferstring[:-1]
				bufferstring += ']},'
				bufferstring += '{"clubcardID": "'
				bufferstring += i[0]
				bufferstring += '", "balance": "'
				bufferstring += str(i[1])
				bufferstring += '", "transactions": ['
			bufferstring += '{"amount": '
			bufferstring += str(i[2])
			bufferstring += ', "timestamp": "'
			bufferstring += str(i[3])
			bufferstring += '"},'
	# letzter Durchlauf:
	# loesche zunaechst das letzte Komma
	bufferstring = bufferstring[:-1]
	bufferstring += ']}]'
	# loesche die ersten drei Zeichen (']},' -> zu Schleifenbeginn angelegt)
	bufferstring2 = bufferstring[3:]
	bufferstring = '[' + bufferstring2
	return bufferstring




def getbalance(key):
	print("Frage Guthaben für Karte Nr. "+key+" ab.")
	# return 14.23
	cur = conn.cursor()
	cur.execute("SELECT balance FROM clubcards WHERE clubcardID= (?)", (key,))
	# Spalte 0: clubcardID, Spalte 1: amount, Spalte: transactiontimestamp
	db_data = cur.fetchall()

	# Wenn keine Werte vorhanden, Clubkarte anlegen
	if len(db_data) == 0:
		print("kein Eintrag, lege an ...")

		# return "{}"
		cur.execute("INSERT INTO clubcards (clubcardID, balance) VALUES (? , 0.0)", (key,))
		conn.commit()
		cur.execute("SELECT balance FROM clubcards WHERE clubcardID= (?)", (key,))
		db_data = cur.fetchall()
		
	# bufferstring = '{"clubcardID": '+str(key) + ', balance: '+str(db_data)
	bufferstring = str(db_data)
	# String zurechtschneiden? -> vorne zwei weg, hinteren 3 weg
	payload = bufferstring[2:-3]
	print(payload)
	return payload



def transferamount(key, amount):
	print("Transaction: UID "+key+" Amount: "+str(amount))
	# Transaktion in transactions einfuegen:
	cur = conn.cursor()
	cur.execute("INSERT INTO transactions (clubcardID, amount) VALUES (? , ? )",(key, amount))
	conn.commit()
	# Guthaben abfragen und in Buffer speichern:
	guthabenbuffer = 0.0
	cur.execute("SELECT balance FROM clubcards WHERE clubcardID= (?)", (key,))
	# Spalte 0: clubcardID, Spalte 1: amount, Spalte: transactiontimestamp
	db_data = cur.fetchall()

	# Wenn keine Werte vorhanden, Clubkarte anlegen
	if len(db_data) == 0:
		print("kein Eintrag, lege an ...")

		# return "{}"
		cur.execute("INSERT INTO clubcards (clubcardID, balance) VALUES (? , 0.0)", (key,))
		get_db().commit()
		cur.execute("SELECT balance FROM clubcards WHERE clubcardID= (?)", (key,))
		db_data = cur.fetchall()
	
	bufferstring = str(db_data)
	# String zurechtschneiden? -> vorne zwei weg, hinteren 3 weg, siehe oben
	bufferstring = bufferstring[2:-3]
	# ggf. auf zwei Nachkommastellen runden (Konvertierungsfehler abfedern):
	guthabenbuffer = float(bufferstring)
	guthabenbuffer = round(guthabenbuffer, 2)
	# neues Guthaben berechnen:
	transactionbuffer = amount
	transactionbuffer = round(transactionbuffer, 2)
	guthabenbuffer = guthabenbuffer + transactionbuffer
	# sicherheitshalber nochmal runden
	guthabenbuffer = round(guthabenbuffer, 2)
	# Guthaben in Tabelle clubcards updaten
	cur.execute("UPDATE clubcards SET balance = (?) WHERE clubcardID = (?)",(guthabenbuffer, key))
	conn.commit()
	return "Erfolgreich"







# UNTEREN FUNKTIONEN MUESSEN GEUPDATED WERDEN : NOCH NICHT AUF ZWEITE TABELLE CLUBCARDS ANGEPASST!!!!

# # Transaktion vornehmen
# def transaction(identifier, amount):
# 	# Eintragung in transactions
# 	c = conn.cursor()
# 	c.execute("INSERT INTO transactions VALUES ("+str(identifier)+","+str(amount)+", CURRENT_TIMESTAMP)")
# 	conn.commit()
# 	# Abrufen des bisherigen Kontostands
# 	previousbalance = 0.0
# 	c = conn.cursor()
# 	c.execute("SELECT balance FROM clubcards WHERE clubcardID="+str(identifier))
# 	previousbalance = c.fetchall()
# 	print("previousbalance: ")
# 	print(previousbalance)
# 	conn.close()

# # Transaktionen abrufen
# def gettransactions(identifier):
# 	c = conn.cursor()
# 	c.execute("SELECT amount, transactiontimestamp FROM transactions WHERE clubcardID="+str(identifier))
# 	dbselection = c.fetchall()
# 	return dbselection


# # Transaktionen abrufen
# def getbalance(identifier):
# 	c = conn.cursor()
# 	c.execute("SELECT balance FROM clubcards WHERE clubcardID="+str(identifier))
# 	dbselection = c.fetchall()
# 	if not dbselection:
# 		print("kein Eintrag vorhanden, lege Clubkarte an...")
# 		c = conn.cursor()
# 		c.execute("INSERT INTO clubcards VALUES ("+str(identifier)+",0.00)")
# 		conn.commit()
# 	return dbselection


# Testing:




# create_table()



# transaction("123456", "-5.80")
# print(gettransactions(12345))
# print(getbalance(123456))
# print(returnclubcardjson())

# print(getbalance("123456"))

# transferamount("123456",-10.83)
