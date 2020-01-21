import pyodbc
import config

class TempretureService:

#VIBR
#HIGR
#TEMP

    def getActualTempreture(self):
        conn = pyodbc.connect(config.CONNSTRING)
        cursor = conn.cursor()
        cursor.execute('SELECT top 1 Value FROM EventLog where EventType = "TEMP" order by 1 desc;')
        temperature = ""
        for row in cursor:
            temperature = temperature + " " + row[1]
        conn.close()
        return temperature

    def getActualHigr(self):
        conn = pyodbc.connect(config.CONNSTRING)
        cursor = conn.cursor()
        cursor.execute('SELECT top 1 Value FROM EventLog where EventType = "HIGR" order by 1 desc;')
        higr = ""
        for row in cursor:
            higr = higr + " " + row[1]
        conn.close()
        return higr

    def getActualHigr(self):
        conn = pyodbc.connect(config.CONNSTRING)
        cursor = conn.cursor()
        cursor.execute('SELECT top 1 Value FROM EventLog where EventType = "VIBR" order by 1 desc;')
        vibr =  ""
        for row in cursor:
            vibr = vibr + " " + row[1]
        conn.close()
        return vibr