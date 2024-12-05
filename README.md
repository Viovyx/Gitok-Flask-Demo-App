# gitok-demo-communicatie

Deze instructies zijn geschreven om te werken op een nieuw opgezette ubuntu 24.04 server.

## download deze repository
Download deze repository (of gebruik git clone) in je home folder.

Voor verdere instructies gaan we ervan uit dat je (met cd) in deze map werkt.

## setup test mysql server
Voer docker_start_empty_testdb.sh uit om een (tijdelijke) mysql server te starten, die luistert op de niet-standaard poort 3308. Deze wordt gebruikt voor deze demo.
Gebruik in je project je eigen mysql server die je hebt opgezet, op poort 3306. Instructies om deze op te zetten staan op smartschool.
```
chmod +x docker_start_empty_testdb.sh
./docker_start_empty_testdb.sh
```


## setup python3 environment
installeer de nodige python3 packages:
```
sudo apt-get install python3-pip python3-venv
```
Maak een virtual environment aan, dit moet je enkel de eerste keer doen
```
python3 -m venv .venv
```
Start de virtual environment op
```
source .venv/bin/activate
```
Download de nodige python libraries (tip: als je voor je project nog python libraries nodig hebt voeg ze dan toe aan requirements.txt, zodat iemand anders gemakkelijk dezelfde omgeving kan opzetten:
```
pip3 install -r requirements.txt
```
Start het python bestand
```
python3 App.py
```
