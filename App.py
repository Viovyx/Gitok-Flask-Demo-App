import eventlet
eventlet.monkey_patch()
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mqtt import Mqtt, ssl
from flask_socketio import SocketIO
import mariadb
from datetime import datetime
from random import random

app = Flask(__name__)

mariadb_config = {
    'host': '127.0.0.1',
    'port': 3308,
    'user': 'root',
    'password': 'Password123!',
    'database': 'example-database'
}

conn = mariadb.connect(**mariadb_config)
cur = conn.cursor()

load_dotenv()
mqtt_user = os.getenv('MQTT_USERNAME')
app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL')
app.config['MQTT_BROKER_PORT'] = os.getenv('MQTT_BROKER_PORT')
app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME')
app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD')
app.config['MQTT_KEEPALIVE'] = os.getenv('MQTT_KEEPALIVE')
app.config['MQTT_TLS_ENABLED'] = os.getenv('MQTT_TLS_ENABLED')
app.config['MQTT_TLS_INSECURE'] = os.getenv('MQTT_TLS_INSECURE')
app.config['MQTT_TLS_CA_CERTS'] = os.getenv('MQTT_TLS_CA_CERTS')
app.config['MQTT_TLS_VERSION'] = os.getenv('MQTT_TLS_VERSION')
app.config['MQTT_TLS_CIPHERS'] = os.getenv('MQTT_TLS_CIPHERS')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
mqtt = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins='*')

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

@app.route('/')
def homepage():
    return("Hello World")

@app.route('/template_example')
def template_example():
    name = request.args.get('naam', default = 'no name', type = str) #vraag naam in url (voeg ?naam=JeNaam toe aan de url), als er geen naam wordt meegegeven wordt "no name" gebruikt als naam.
    return render_template('template_example.html', name=name)

@app.route('/add_data')
def init_db():
    content = request.args.get('content', default = 'DEFAULT_RESPONSE', type = str)
    cur.execute("INSERT INTO TestTable SET Content=%s;", (content,))
    conn.commit()
    return (content + " inserted")

@app.route('/show_db')
def get_data():
    cur.execute("SELECT * FROM TestTable");
    rows = cur.fetchall()
    print(rows)
    return render_template('show_db.html', content=rows)

@app.route('/rm_data')
def rm_data():
    row = request.args.get('id', default = '-1', type = str)
    if (int(row) >= 0):
        cur.execute("DELETE FROM TestTable WHERE Id=%s;", (row,))
        conn.commit()
        return ("row " + row + " removed")
    return ("ERROR: Enter a number above 0!")

@app.route('/sensor')
def sensor():
    return render_template('sensor.html')

@app.route('/actuator', methods=['GET', 'POST'])
def actuator():
    if request.method == 'POST':
        value = request.form.get('value')
        mqtt.publish(f'{mqtt_user}/feeds/actuator1', value)
        return render_template('actuator.html', value=value)
        # return ("thanks for inputting " + value)
    else:
        return render_template('actuator.html')
    
@app.route('/graph')
def graph():
    return render_template('graph.html')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(f'{mqtt_user}/feeds/graph')
    mqtt.subscribe(f'{mqtt_user}/feeds/sensor1')
    mqtt.subscribe(f'{mqtt_user}/feeds/actuator1')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(message.topic, message.payload.decode())
    if (message.topic == f"{mqtt_user}/feeds/sensor1"):
        socketio.emit("updateSensor1", message.payload.decode())
    if (message.topic == f"{mqtt_user}/feeds/actuator1"):
        socketio.emit("updateActuator1", message.payload.decode())
    if (message.topic == f"{mqtt_user}/feeds/graph"):
        if (message.payload.decode() == "random"):
            random_value = round(random() * 100)
            mqtt.publish(f"{mqtt_user}/feeds/graph", random_value)
        else:
            socketio.emit('updateSensorData', {'value': message.payload.decode(), 
                                            "date": get_current_datetime()})
@socketio.on('connect')
def connect():
    print('Client connected')


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == "__main__":
    cur.execute("CREATE TABLE IF NOT EXISTS TestTable (Id int AUTO_INCREMENT PRIMARY KEY, Content VARCHAR(50));")
    conn.commit()
    socketio.run(app, host="0.0.0.0", debug=True, use_reloader=False)
