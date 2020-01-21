import pyodbc
import config


class TemperatureService:

    def __init__(self):
        self.conn = pyodbc.connect(config.CONNSTRING)

    def getActualTempreture(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT top 1 Value FROM EventLog where EventType = "TEMP" order by 1 desc;')
        temperature = ""
        for row in cursor:
            temperature = temperature + " " + row[1]
        return temperature

    def getActualHigr(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT top 1 Value FROM EventLog where EventType = "HIGR" order by 1 desc;')
        higr = ""
        for row in cursor:
            higr = higr + " " + row[1]
        return higr

    def getActualHigr(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT top 1 Value FROM EventLog where EventType = "VIBR" order by 1 desc;')
        vibr =  ""
        for row in cursor:
            vibr = vibr + " " + row[1]
        return vibr

    def __del__(self):
        self.conn.close()