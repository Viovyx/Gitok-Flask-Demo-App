# gitok-demo-communicatie

Deze instructies zijn geschreven om te werken op een nieuw opgezette ubuntu 24.04 server.

## setup test mysql server
Voer docker_start_empty_testdb.sh uit om een (tijdelijke) mysql server te starten, die luistert op de niet-standaard poort 3308. Deze wordt gebruikt voor deze demo.
Gebruik in je project je eigen mysql server die je hebt opgezet, op poort 3306. Instructies om deze op te zetten staan op smartschool.


## setup python3 environment
apt-get install python3-pip
pip install -r requirements.txt
