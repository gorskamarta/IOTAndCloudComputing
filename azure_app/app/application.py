import pyodbc
import config
from flask import Flask, request, render_template, make_response, redirect
from service.SensorService import SensorService
from service.LoginService import LoginService
from service.SessionService import SessionService
app = Flask(__name__)

webkey = config.WEBKEY
connstring = config.CONNSTRING

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    tempServ = SensorService()
    temp = tempServ.getActualTemp()
    higr = tempServ.getActualHigr()
    vibr = tempServ.getActualVibr()

    sessId = request.cookies.get('session_id')
    if sessId == None:
        isActive = 0
    elif sessId != None:
        sessServ = SessionService()
        isActive = sessServ.isActive(sessId)

    return render_template('index.html', temperature=temp, higr=higr, vibr=vibr, sess=isActive)

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    login = request.form.get('uname')
    passwd = request.form.get('psw')
    loginServ = LoginService()
    loginId = loginServ.login(login, passwd)
    if loginId != 0:
        sessServ = SessionService()
        sessId = sessServ.setSession(loginId)
        if sessId != None:
            response = make_response(redirect('/index'))
            response.set_cookie('session_id', sessId)
            return response
        else:
            return "Problem z zalogowaniem"

