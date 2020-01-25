import pyodbc
import config
from flask import Flask, request, render_template, make_response, redirect
from service.SensorService import SensorService
from service.ControlService import ControlService
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
    contServ = ControlService()
    
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
            result =          "{\"LedRed\": \"" + contServ.getDeviceLedRed()  + "\","
            result = result + "\"LedBlue\": \"" + contServ.getDeviceLedBlue() + "\"}"
    return result

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        sessId = request.cookies.get('session_id')
        if sessId == None:
            isActive = 0
        sessServ = SessionService()
        isActive = sessServ.isActive(sessId)
        if isActive == 1:
            response = make_response(redirect('/index?message=AlreadyLog'))
            return response
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
    message = 'Problem z zalogowaniem'
    return render_template('exception.html', message=message)

@app.route('/setLed', methods=['POST', 'GET'])
def setLed():
    sessId = request.cookies.get('session_id')
    if sessId == None:
        isActive = 0
    sessServ = SessionService()
    isActive = sessServ.isActive(sessId)
    if isActive == 1:
        contrServ = ControlService()
        if request.method == 'GET':
            checkedOn = ''
            checkedOff = ''
            isOn = contrServ.getDeviceLedBlue()
            if isOn == 'ON':
                checkedOn = 'checked'
            else:
                checkedOff = 'checked'
            return render_template('setLed.html', checkedOn=checkedOn, checkedOff=checkedOff)
        stan = request.form.get('stan')
        if stan == 'on':
            contrServ.setDeviceLedBlueON()
        if stan == 'off':
            contrServ.setDeviceLedBlueOFF()
        response = make_response(redirect('/setLed'))
        return response

    message = 'Zaloguj sie przed proba sterowania'
    return render_template('exception.html', message=message)

