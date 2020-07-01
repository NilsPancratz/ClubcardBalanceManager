from flask import Flask, request, jsonify, g

import sqlite3
import json

app = Flask(__name__)
#api = Api(app)

databasefile = 'db.db'
conn = sqlite3.connect(databasefile)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(databasefile)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return "Hello Clubcard Payment User :)"



# # Gibt Guthaben mit clubcardID und Guthaben zurueck:
# @app.route('/balances/clubcardID/<key>', methods = ['GET', 'POST', 'DELETE'])
# erlaubt nur GET
@app.route('/balances/clubcardID/<key>', methods = ['GET'])
def gettransactions(key):
	if request.method == 'GET':
		cur = get_db().cursor()
		cur.execute("SELECT balance FROM clubcards WHERE clubcardID= (?)", (key,))
		# Spalte 0: clubcardID, Spalte 1: amount, Spalte: transactiontimestamp
		db_data = cur.fetchall()

		# Wenn keine Werte vorhanden, Clubkarte anlegen
		if len(db_data) == 0:
			# return "{}"
			cur.execute("INSERT INTO clubcards (clubcardID, balance) VALUES (? , 0.0)", (key,))
			get_db().commit()
			cur.execute("SELECT balance FROM clubcards WHERE clubcardID= (?)", (key,))
			db_data = cur.fetchall()
			
		# bufferstring = '{"clubcardID": '+str(key) + ', balance: '+str(db_data)
		bufferstring = str(db_data)
		# String zurechtschneiden? -> vorne zwei weg, hinteren 3 weg
		payload = bufferstring[2:-3]
		return payload

# Fuegt die Transaktion in transactions ein, fragt letztes Guthaben ab und updated Guthaben
# @app.route('/clubcardID/<key>/<resource>', methods=['GET', 'PUT', 'POST', 'DELETE'])
# erlaubt nur PUT oder POST
@app.route('/clubcardID/<key>/<resource>', methods=['PUT', 'POST'])
def posttransaction(key, resource):
	if request.method == 'PUT' or request.method == 'POST':
		# Transaktion in transactions einfuegen:
		cur = get_db().cursor()
		cur.execute("INSERT INTO transactions (clubcardID, amount) VALUES (? , ? )",(key, resource))
		get_db().commit()
		# Guthaben abfragen und in Buffer speichern:
		guthabenbuffer = 0.0
		cur.execute("SELECT balance FROM clubcards WHERE clubcardID= (?)", (key,))
		# Spalte 0: clubcardID, Spalte 1: amount, Spalte: transactiontimestamp
		db_data = cur.fetchall()
		bufferstring = str(db_data)
		# String zurechtschneiden? -> vorne zwei weg, hinteren 3 weg, siehe oben
		bufferstring = bufferstring[2:-3]
		# ggf. auf zwei Nachkommastellen runden (Konvertierungsfehler abfedern):
		guthabenbuffer = float(bufferstring)
		guthabenbuffer = round(guthabenbuffer, 2)
		# neues Guthaben berechnen:
		transactionbuffer = float(resource)
		transactionbuffer = round(transactionbuffer, 2)
		guthabenbuffer = guthabenbuffer + transactionbuffer
		# sicherheitshalber nochmal runden
		guthabenbuffer = round(guthabenbuffer, 2)
		# Guthaben in Tabelle clubcards updaten
		cur.execute("UPDATE clubcards SET balance = (?) WHERE clubcardID = (?)",(guthabenbuffer, key))
		get_db().commit()
		return "Erfolgreich"

# Gibt JSON mit ClubkartenID, Guthaben und Transaktionen zurück
# erlaubt nur GET
@app.route('/clubcards/')
def getclubcards():
	cur = get_db().cursor()
	cur.execute("SELECT * FROM clubcards NATURAL JOIN transactions ORDER BY clubcardid ASC, transactiontimestamp DESC;")
	# Spalte 0: clubcardID, Spalte 1: amount, Spalte: transactiontimestamp
	db_data = cur.fetchall()

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
				bufferstring += '", "balance": '
				bufferstring += str(i[1])
				bufferstring += ', "transactions": ['
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

# Faehrt den Server herunter
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

# ermoeglicht es externen Skripten den Server hochzufahren
def webApp_start_externscript(webAppstatus):
	if webAppstatus == True:
		try:
			app.run(host='0.0.0.0')
		except:
			print("konnte nicht hochgefahren werden, vielleicht bereits up?")

# ermoeglicht es intern, den Server hochzufahren
def webApp_start():
	if __name__ == '__main__':
		app.run(host='0.0.0.0')



webApp_start()
