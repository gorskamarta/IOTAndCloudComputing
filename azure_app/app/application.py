import pyodbc
import config
import azure_app.app.service.TemperatureService
from flask import Flask, request, render_template
app = Flask(__name__)

webkey = config.WEBKEY
connstring = config.CONNSTRING

@app.route('/')
@app.route('/index')
def index():
    tempServ = azure_app.TemperatureService()
    temp = tempServ.getActualTemp
    higr = tempServ.getActualHigr
    return render_template('index.html', temperature=temp, higr=higr)

@app.route('/newevent', methods=['POST','GET'])
def newevent():
    result = "No method"
    if request.method == 'POST':
        Token     = request.form.get('Token')
        EventType = request.form.get('EventType')
        Value     = request.form.get('Value')
        result = "Invalid token"
        if Token==webkey:
            conn = pyodbc.connect(connstring)
            cursor = conn.cursor()
            query = "INSERT INTO EventLog (EventType, Value, DateTime) VALUES ('" + EventType + "','" + Value + "', GETDATE() );"
            cursor.execute(query)
            conn.commit()
            conn.close()
            result = "New entry registred"
    return result