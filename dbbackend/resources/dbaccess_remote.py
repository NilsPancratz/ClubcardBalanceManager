import requests
import json

apiip = "localhost"
cardID = "5C:9F:38:3A:66:4E:10"
amount = "-15.0"

# Transaktionen abrufen
# r = requests.get('http://'+apiip+':5000/balances/clubcardID/'+cardID)
# print("Aktueller Kontostand: " + r.text)

# # Transaktion durchfuehren
# requests.put('http://'+apiip+':5000/clubcardID/'+cardID+"/"+amount)

# JSON mit Clubcards abrufen und Umlaufsumme ausgeben
def printtotalbalances():
	r = requests.get('http://'+apiip+':5000/clubcards')
	returnjson = r.text
	clubcards = json.loads(returnjson)
	# print(json.dumps(y, indent=1, sort_keys=True))
	# print(type(clubcards))
	totalbalances = 0.0
	for clubcard in clubcards:
		totalbalances += float(clubcard["balance"])
	print(totalbalances)

# alternativ mit lokalen Testdaten
def test_totalbalances():
	file = open('testdata.txt', 'r')
	r = file.read()
	file.close()
	returnjson = r
	clubcards = json.loads(returnjson)
	totalbalances = 0.0
	for clubcard in clubcards:
		totalbalances += float(clubcard["balance"])
	print(totalbalances)

# Anzahl der ausgegebenen Karten ausgeben
def test_numberofclubcards():
	file = open('testdata.txt', 'r')
	r = file.read()
	file.close()
	returnjson = r
	clubcards = json.loads(returnjson)
	print(json.dumps(clubcards, indent=4, sort_keys=True))
	numberofclubcards = 0
	for i in clubcards:
		numberofclubcards += 1
	print(numberofclubcards)

# UIDs oder Seriennummern ausgeben
def test_printserialnumbers():
	file = open('testdata.txt', 'r')
	r = file.read()
	file.close()
	returnjson = r
	clubcards = json.loads(returnjson)
	# print(json.dumps(clubcards, indent=4, sort_keys=True))
	for i in clubcards:
		currentUID=i["clubcardID"]
		print(currentUID)
		print(convertUIDtoSerialNo(currentUID))

# Mifare Ultralight EV 1 UID in Seriennummer umrechnen
def convertUIDtoSerialNo(UID):
	UID_30=UID[:11] #nur die ersten 4 Byte
	UID_0=UID_30[9:11] #byteweise tauschen
	UID_1=UID_30[6:8]
	UID_2=UID_30[3:5]
	UID_3=UID_30[0:2]
	serialNo=UID_0+UID_1+UID_2+UID_3
	serialNo_dez=int(serialNo, 16) #Hex in Dez
	return serialNo_dez

# test_totalbalances()
# test_numberofclubcards()
# test_printserialnumbers()
# test_totalbalances()
# printtotalbalances()
print(convertUIDtoSerialNo("5C:9F:38:3A:66:4E:10"))
