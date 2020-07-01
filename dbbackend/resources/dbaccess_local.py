import sqlite3

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




create_table()
# transaction("12346", "-5.80")
# print(gettransactions(12345))
# print(getbalance(12345))
# print(returnclubcardjson())
