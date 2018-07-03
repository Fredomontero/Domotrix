import RPi.GPIO as GPIO #Libreria Python GPIO
import time #Libreria Time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

GPIO.setmode(GPIO.BCM) #Establecemos el sisetma de numeracion de pins BCM
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT) #Ponemos el Pin GPIO4 como salida
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Ponemos el Pin GPIO17 como como entrada y pull up
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Ponemos el Pin GPIO17 como como entrada y pull up
global led_state
global sensor_state
cred = credentials.Certificate('/home/pi/Desktop/Practicas/ProyectoFinal/cred.json')

def getLedData():
	led_ref = db.reference('led/state').get()
	led_db = (True, False)[led_ref == "off"]
	return led_db

def loadLedData():
	led_state = getLedData()
	toogleLed(led_state)
	return led_state

def compareState(led_state):
	led_temp = getLedData()
	result = (False, True)[led_state == led_temp]
	return result


def loadResources():
	firebase_admin.initialize_app(cred, {
    	'databaseURL': 'https://domotrix-6534a.firebaseio.com/'
	})

def changeState(led_state):
	print "The state of the led is: ", led_state
	led_value = ("off", "on")[led_state == True]
	db.reference('led/state').set(led_value)

def toogleLed(led_state):
	if led_state == True:
		GPIO.output(4, GPIO.LOW)
	else:
		GPIO.output(4, GPIO.HIGH)
	changeState(led_state)
	
def toogleSensor():
	if GPIO.input(27) == False:
		while(GPIO.input(27) == 0):
			pass
		time.sleep(0.02)
		print "The sensor state has change to: ", True
	db.reference('sensor/state').set("off")
			

#main function 
def main():
	print "Welcome to Domotrix"
	loadResources()
	led_state = loadLedData()
	sensor_state = False
	while True:
		if GPIO.input(17) == False:
			while(GPIO.input(17) == 0):
				pass
			time.sleep(0.05)
			led_state = not led_state
			toogleLed(led_state)
		elif GPIO.input(27) == False:
			db.reference('sensor/state').set("on")
			print "The sensor state has change to: ", False
			toogleSensor()
		elif compareState(led_state) == False:
			led_state = getLedData()
			toogleLed(led_state)

try:
	main()
except:
	print "Finishing program"
finally:
	GPIO.cleanup()
#python app.py
