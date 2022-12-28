#!/usr/bin/env python3

import cgi
import requests
import json
import html

our_form = cgi.FieldStorage()
in_name = our_form.getfirst("in_name", "not found")
in_name = html.escape(in_name)
url = 'http://api.weatherapi.com/v1/current.json?key=5edf2f4998ab4944bf8135340222612&q=' + in_name
response = requests.get(url)

data_dir = response.json()
country = data_dir["location"]["country"]
timezone = data_dir["location"]["tz_id"]
local_time = data_dir["location"]["localtime"]
tempc = data_dir["current"]["temp_c"]
tempf = data_dir["current"]["temp_f"]
cond = data_dir["current"]["condition"]["text"]
print("Content-type: text/html")
print()
# print('Weather in ', in_name)
# print('Located in ', country)
# print('In ', timezone)
# print('Time: ', local_time)
# print('Celsius ', tempc)
# print('Fahrenheit ', tempf)
# print('Condition: ', cond)
print("""<!DOCTYPE HTML>
        <html>
        <head>
        <style>
        h1 {
            text-align: center;
        }

        p {
            text-align: center;
        }
    </style>
            <meta charset="utf-8">
            <title> weather </title>
        </head>
        <body style="background-color: lightskyblue">""")

print("<h1> Weather in city today </h1>")
print("<p> City: {}</p>".format(in_name))
print("<p> Country: {}</p>".format(country))
print("<p> Timezone: {}</p>".format(timezone))
print("<p> Local time: {}</p>".format(local_time))
print("<p> Temp Celsius: {}</p>".format(tempc))
print("<p> Temp Fahrenheit: {}</p>".format(tempf))
print("<p> Condition: {}</p>".format(cond))

print("""</body>
        </html>""")