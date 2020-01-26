import pyodbc
import config
import secrets

class SessionService:
    def __init__(self, CONNSTRING=config.CONNSTRING):
        self.conn = pyodbc.connect(CONNSTRING)

    def setSession(self, userId):
        sessId = secrets.token_urlsafe(16)
        cursor = self.conn.cursor()
        query = "INSERT INTO Sessions (UserId, SessId) VALUES ('" + str(userId) + "','" + str(sessId) + "');"
        cursor.execute(query)
        self.conn.commit()
        return sessId

    def isActive(self, sessId):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT IsActive FROM Sessions WHERE SessId = '" + str(sessId) + "'")
        row = cursor.fetchone()
        if not row:
            return 0
        return row[0]

    def __del__(self):
        self.conn.close()