import json, urllib.request as urlread
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/check_city', methods=['POST'])
def check_city():
    if request.method == 'POST':
        country = request.form['country']
        city = request.form['city']
        appid = "0373f9cf76566a7ffc49a8a2a5a898cd"
        #city = "London"
        #country = "uk"

        urlGet = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country\
        + "&appid=" + appid\
        + "&units=metric" 
    
        with urlread.urlopen(urlGet) as url:
            parsed_json = json.loads(url.read().decode())
    
    return \
    "Miasto: "     + parsed_json['name'] + "<br>"\
    "Państwo: "    + parsed_json['sys']['country'] + "<br>"\
    "Temperatura : " + str(parsed_json['main']['temp']) + " oC<br>"\
    "Temperatura (min): " + str(parsed_json['main']['temp_min']) + " oC<br>"\
    "Temperatura (max): " + str(parsed_json['main']['temp_max']) + " oC<br>"\
    "<a href='/'>Formularz</a>"



