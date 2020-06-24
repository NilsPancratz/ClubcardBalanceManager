import requests
import json

cardID = "34:67:99"

# Transaktionen abrufen
r = requests.get('http://192.168.2.108:5000/balances/clubcardID/'+cardID)
print("Aktueller Kontostand: " + r.text)



# # Transaktion durchfuehren
amount = "-89.60"
# r = requests.put('http://192.168.0.3:5000/clubcardID/'+cardID+"/"+amount)
