import pyodbc
import config
import hashlib

class LoginService:
    def __init__(self, CONNSTRING=config.CONNSTRING):
        self.conn = pyodbc.connect(CONNSTRING)

    def login(self, login, passwd):
        passwd_hash = self.hashPasswd(passwd)
        cursor = self.conn.cursor()
        cursor.execute("SELECT Id AS Granted FROM UserAccess WHERE UserLogin = '" + login + "' AND UserPassword = '" + passwd_hash + "';")
        row = cursor.fetchone()
        if not row:
            return 0
        return row[0]

    def hashPasswd(self, passwd):
        salt = '!@#qazxsw'
        return hashlib.md5(bytes(passwd, 'utf-8') + bytes(salt, 'utf-8')).hexdigest()

    def __del__(self):
        self.conn.close()
