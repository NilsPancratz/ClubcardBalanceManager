import requests
import json


apiip = "localhost"
cardID = "34:67:88"
amount = "-15.0"


# Transaktionen abrufen
# r = requests.get('http://'+apiip+':5000/balances/clubcardID/'+cardID)
# print("Aktueller Kontostand: " + r.text)



# # Transaktion durchfuehren
# requests.put('http://'+apiip+':5000/clubcardID/'+cardID+"/"+amount)


# JSON mit Clubcards abrufen und Umlaufsumme ausgeben
r = requests.get('http://'+apiip+':5000/clubcards')
returnjson = r.text
clubcards = json.loads(returnjson)
# print(json.dumps(y, indent=1, sort_keys=True))
# print(type(clubcards))
totalbalances = 0.0
for clubcard in clubcards:
	totalbalances += float(clubcard["balance"])
print(totalbalances)