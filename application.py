import pyodbc
import config
from flask import Flask, request
app = Flask(__name__)

webkey = config.WEBKEY
connstring = config.CONNSTRING

@app.route("/")
def hello():
    conn = pyodbc.connect(connstring)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Test;')
    result = ""
    for row in cursor:
        result = result + " " + row[1]
    conn.close()
    return result

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
