#Żydoskop do bramy
#Libraries
import RPi.GPIO as GPIO
import time
#ADXL
import board
import busio
import adafruit_adxl34x
import Adafruit_DHT
#do hmóry
import requests
import json
import config

API_ENDPOINT = config.API_ENDPOINT
API_KEY = config.API_KEY

readinterval = 10 #seconds

calibmax = 1.05
calibmin = 0.95
#ADXL
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
#initial oldacc
oldacc = [accelerometer.acceleration[0],accelerometer.acceleration[1],accelerometer.acceleration[2]]

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
LED1_OUT = 20
LED2_OUT = 21
ZYD = False

#DHT settings
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
 
#set GPIO direction (IN / OUT)
GPIO.setwarnings(False) # olać warningi na GPIO
GPIO.cleanup() # czyszczenie GPIO
# Sonar
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
# LEDy
GPIO.setup(LED1_OUT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED2_OUT, GPIO.OUT, initial=GPIO.LOW)

def cloud(EventType,Value):
    data = {'Token':API_KEY, 'EventType':EventType, 'Value':Value}
    r = requests.post(url = API_ENDPOINT, data = data)
    pastebin_url = r.text
    print("EventType: [" + EventType + "], Value: [" + Value + "]")
    print("Server response: %s"%pastebin_url)
    parsed_json = json.loads(pastebin_url)
    if parsed_json['LedBlue']=='ON':
        GPIO.output(LED2_OUT, GPIO.HIGH)
    if parsed_json['LedBlue']=='OFF':
        GPIO.output(LED2_OUT, GPIO.LOW)


def vibrdetect(oldacc):
    val = 0
    pctacc = [oldacc[0] / accelerometer.acceleration[0],
              oldacc[1] / accelerometer.acceleration[1],
              oldacc[2] / accelerometer.acceleration[2]]
    if \
       pctacc[0]>calibmax or pctacc[0]<calibmin or \
       pctacc[1]>calibmax or pctacc[1]<calibmin or \
       pctacc[2]>calibmax or pctacc[2]<calibmin:
        val = 1
    #time.sleep(1)
    oldacc = [accelerometer.acceleration[0],accelerometer.acceleration[1],accelerometer.acceleration[2]]
    return val


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            try:
                DHT22_lastread
            except:
                DHT22_lastread = time.time()
                
            try:
                checkanty
            except:
                checkanty = 0
                
            try:
                vibrevent
            except:
                vibrevent = 'None'
                
            DHT22_time = time.time() - DHT22_lastread
            if DHT22_time>readinterval:
                DHT22_lastread = time.time()
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
                cloud('TEMP', str(round(temperature,1)))
                cloud('HIGR', str(round(humidity,1)))
                if vibrevent!='None':
                    cloud('VIBR',vibrevent)
                    vibrevent = 'None'
                    
            
            dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            oldacc = [accelerometer.acceleration[0],accelerometer.acceleration[1],accelerometer.acceleration[2]]
            time.sleep(0.100)
            checkanty = checkanty + vibrdetect(oldacc)
            

            
            if dist<20:
                GPIO.output(LED1_OUT, GPIO.HIGH)
                #GPIO.output(LED2_OUT, GPIO.LOW)
                print("Vandal:" + str(checkanty))
                if checkanty>5:
                    vibrevent = 'Vandal'
                    checkanty = 0
            else:
                if checkanty>1 and vibrevent != 'Vandal':
                    vibrevent = 'Ground'
                    checkanty = 0
                GPIO.output(LED1_OUT, GPIO.LOW)
                #GPIO.output(LED2_OUT, GPIO.HIGH)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
