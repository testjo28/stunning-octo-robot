from flask import render_template
from flask import Flask

import psycopg2

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/db/')
def with_db():
    conn = psycopg2.connect("dbname=test user=postgres")
    cur = conn.cursor()
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))


@app.route('/image/')
def with_image():
    return render_template('image.html')
