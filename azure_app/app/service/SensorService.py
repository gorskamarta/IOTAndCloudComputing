import pyodbc
import config

class SensorService:
    def __init__(self, CONNSTRING=config.CONNSTRING):
        self.conn = pyodbc.connect(CONNSTRING)

    def getActualVar(self, EventType):
        cursor = self.conn.cursor()
        cursor.execute("SELECT TOP 1 Value, CAST( DATEADD(hour, 1, DateTime) AS smalldatetime ) AS DateTime FROM EventLog WHERE EventType = '" + EventType + "' ORDER BY 1 DESC;")
        row = cursor.fetchone()
        if not row:
            resultVal  = 'No data!'
            resultDate = 'No data!'
        else:
            resultVal  = row[0]
            resultDate = row[1]
        return resultVal, resultDate

    def getActualTemp(self):
        resultVal, resultDate = self.getActualVar('TEMP')
        return resultVal

    def getActualHigr(self):
        resultVal, resultDate = self.getActualVar('HIGR')
        return resultVal
    
    def getActualVibr(self):
        resultVal, resultDate = self.getActualVar('VIBR')
        return resultDate
    
    def __del__(self):
        self.conn.close()
