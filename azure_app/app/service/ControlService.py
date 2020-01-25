import pyodbc
import config

class ControlService:
    def __init__(self, CONNSTRING=config.CONNSTRING):
        self.conn = pyodbc.connect(CONNSTRING)

    def getDeviceState(self, DeviceName):
        cursor = self.conn.cursor()
        cursor.execute("SELECT RTRIM(DeviceName) AS DeviceName, RTRIM(DeviceValue) AS DeviceValue FROM DeviceState WHERE DeviceName='" + DeviceName + "' ORDER BY 1 DESC;")
        row = cursor.fetchone()
        if not row:
            DeviceName  = 'No data!'
            DeviceValue = 'No data!'
        else:
            DeviceName  = row[0]
            DeviceValue = row[1]
        return DeviceName, DeviceValue

    def setDeviceState(self, DeviceName, DeviceValue):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE DeviceState SET DeviceValue='" + DeviceValue + "' WHERE DeviceName='" + DeviceName + "';")
        self.conn.commit()
        return "Updated"
    
    def getDeviceLedRed(self):
        DeviceName, DeviceValue = self.getDeviceState('LedRed')
        return DeviceValue
    
    def getDeviceLedBlue(self):
        DeviceName, DeviceValue = self.getDeviceState('LedBlue')
        return DeviceValue    
    
    def setDeviceLedRedON(self):
        result = self.setDeviceState('LedRed', 'ON')
        return result
    
    def setDeviceLedBlueON(self):
        result = self.setDeviceState('LedBlue', 'ON')
        return result

    def setDeviceLedRedOFF(self):
        result = self.setDeviceState('LedRed', 'OFF')
        return result
    
    def setDeviceLedBlueOFF(self):
        result = self.setDeviceState('LedBlue', 'OFF')
        return result
    
    def __del__(self):
        self.conn.close()