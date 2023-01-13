# flask_test.py
from flask import Flask, render_template, request
import requests
import sqlite3

app = Flask(__name__)

@app.route('/weather', methods=['POST'])
def weather():
    db = sqlite3.connect('db/cities.db')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS search_queries (id INTEGER PRIMARY KEY, name TEXT, count INTEGER) """)
    city_name = request.form['zip']
    db.commit()
    cursor.close()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM search_queries WHERE name = ?;', (city_name,))

    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO search_queries (id, name, count) VALUES (?, 1);', (city_name,))
        print("inserted")
    else:
        cursor.execute('UPDATE search_queries SET count = count + 1 WHERE name = ?;', (city_name,))
        print("updated")
    db.commit()
    cursor.close()
    cursor = db.cursor()
    url = 'http://api.weatherapi.com/v1/current.json?key=5edf2f4998ab4944bf8135340222612&q=' + city_name
    response = requests.get(url)
    data_dir = response.json()

    country = data_dir["location"]["country"]
    timezone = data_dir["location"]["tz_id"]
    local_time = data_dir["location"]["localtime"]
    tempc = data_dir["current"]["temp_c"]
    tempf = data_dir["current"]["temp_f"]
    cond = data_dir["current"]["condition"]["text"]
    return render_template('weather.html', city=city_name, country=country,timezone=timezone, local_time=local_time, tempc=tempc, tempf=tempf, cond=cond)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
