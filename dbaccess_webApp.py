from flask import Flask, request, jsonify, g

import sqlite3
import json

app = Flask(__name__)
#api = Api(app)

databasefile = 'testdatabase.db'
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
    return "Hallo Clubcard Payment User :)"



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
def get_resource(key, resource):
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
		# Guthaben in Tabelle clubcards updaten
		cur.execute("UPDATE clubcards SET balance = (?) WHERE clubcardID = (?)",(guthabenbuffer, key))
		get_db().commit()
		return "Erfolgreich"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
