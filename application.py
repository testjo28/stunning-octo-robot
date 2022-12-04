from flask import render_template
from flask import Flask

import psycopg2

import subprocess
import random
import os
import datetime as dt
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

conn = None

def get_cursor():
    global conn
    conn = psycopg2.connect(os.getenv("DB_CONNECTION"))
    return conn.cursor()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/db/')
def with_db():
    try:
        cur = get_cursor()
        cur.execute("INSERT INTO tick (tick_time) VALUES (%s)", (dt.datetime.now(),))
        conn.commit()

        cur.execute("SELECT id, tick_time FROM tick")
        ticks = cur.fetchall()
        logger.error(f"ticks : {ticks}")
        return render_template('ticks.html', ticks=ticks)

    except Exception as e:
        conn.rollback()
        return f"<p>An error was encoutered, did you call init_db route first ?</p><br>{e}"

@app.route('/init_db/')
def init_db():
    try:
        cur = get_cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tick (id SERIAL PRIMARY KEY, tick_time TIMESTAMP)")
        conn.commit()
        return "<p>Init db done !</p>"
    except Exception as e:
        conn.rollback()
        return f"<p>An error was encoutered</p><br>{e}"

@app.route('/image/')
def with_image():
    new_size = random.randint(50, 200)
    subprocess.check_call(['convert', 'static/VanGogh.jpg', '-resize', f'{new_size}%', 'static/VanGogh_resized.jpg'])
    return render_template('image.html')
