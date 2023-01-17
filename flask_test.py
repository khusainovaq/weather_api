# flask_test.py
from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/flasktest'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)
class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    count = db.Column(db.Integer, nullable=True)

    def __init__(self, name, count):
        self.name = name
        self.count = count
@app.route('/weather', methods=['POST'])
def weather():
    name = request.form['city_name']

    query = db.session.execute(f"""SELECT EXISTS (SELECT * FROM cities WHERE name = '{name}');""")
    result = query.fetchone()
    print(result)
    if result is None:
        db.engine.execute(f"""INSERT INTO cities (name, count) VALUES ('{name}', 1);""")
    else:
        db.engine.execute(f"""UPDATE cities SET count = count + 1 WHERE name = '{name}';""")
    db.session.commit()

    url = 'http://api.weatherapi.com/v1/current.json?key=5edf2f4998ab4944bf8135340222612&q=' + name
    response = requests.get(url)
    data_dir = response.json()

    country = data_dir["location"]["country"]
    timezone = data_dir["location"]["tz_id"]
    local_time = data_dir["location"]["localtime"]
    tempc = data_dir["current"]["temp_c"]
    tempf = data_dir["current"]["temp_f"]
    cond = data_dir["current"]["condition"]["text"]
    return render_template('weather.html', city=name, country=country,timezone=timezone, local_time=local_time, tempc=tempc, tempf=tempf, cond=cond)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)