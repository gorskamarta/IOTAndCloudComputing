#Żydoskop do bramy
#Libraries
import RPi.GPIO as GPIO
import time
#ADXL
import board
import busio
import adafruit_adxl34x
import Adafruit_DHT

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

def antypodpierdol(oldacc):
    pctacc = [oldacc[0] / accelerometer.acceleration[0],
              oldacc[1] / accelerometer.acceleration[1],
              oldacc[2] / accelerometer.acceleration[2]]
    if \
       pctacc[0]>calibmax or pctacc[0]<calibmin or \
       pctacc[1]>calibmax or pctacc[1]<calibmin or \
       pctacc[2]>calibmax or pctacc[2]<calibmin:
        print("Żyd chce zajebać czujnik")
    time.sleep(1)
    oldacc = [accelerometer.acceleration[0],accelerometer.acceleration[1],accelerometer.acceleration[2]]


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
            ##humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(0.100)
            if dist<20:
                GPIO.output(LED1_OUT, GPIO.HIGH)
                GPIO.output(LED2_OUT, GPIO.LOW)
                if ZYD==True:
                    print ("Żyd ciągle przy bramie")
                else:
                    print ("Żyd przy bramie")
                    ZYD_start = time.time()
                ZYD = True;
                oldacc = [accelerometer.acceleration[0],accelerometer.acceleration[1],accelerometer.acceleration[2]]
                for x in range(5): #sleep5
                    antypodpierdol(oldacc)
                
            else:
                if ZYD==True:
                    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
                    ##if humidity is not None and temperature is not None:
                        
                    print ("Żyd zniknął")
                    ZYD_stop = time.time() - ZYD_start
                    print ("Żyd wypalał się około " + str(int(ZYD_stop)) + " sekund")
                    print ("W temperaturze " + str(round(temperature,1)) + " oC")
                    print ("Przy wilgodności powietrza " + str(round(humidity,1)) + " %")
                    # debounce jakby żyd się kręcił przez 10 sekund
                    time.sleep(10) 
                ZYD = False;
                GPIO.output(LED1_OUT, GPIO.LOW)
                GPIO.output(LED2_OUT, GPIO.HIGH)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
