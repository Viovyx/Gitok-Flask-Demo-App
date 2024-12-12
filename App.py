import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import mariadb


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

app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['SECRET_KEY'] = 'secret!'
mqtt = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins='*')


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

@app.route('/sensor')
def sensor():
    return render_template('sensor.html')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('gitok/sensor1')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(message.topic, message.payload.decode())
    socketio.emit("updateSensor1", message.payload.decode())

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
