from flask import Flask, render_template, request
import mariadb

app = Flask(__name__)

config = {
    'host': '127.0.0.1',
    'port': 3308,
    'user': 'root',
    'password': 'Password123!',
    'database': 'example-database'
}

conn = mariadb.connect(**config)
cur = conn.cursor()

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

if __name__ == "__main__":
    cur.execute("CREATE TABLE IF NOT EXISTS TestTable (Id int AUTO_INCREMENT PRIMARY KEY, Content VARCHAR(50));")
    conn.commit()
    app.run(host="0.0.0.0", debug=True)
