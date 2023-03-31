import RPi.GPIO as GPIO
import serial
import time

import VRelay
import CRelay

#Config
max_temp = 30
max_pressure = 107


#Sensors
PSensor = 0 #Pressure sensor
TSensor = 20 #Temperature sensor
sensorlist = [PSensor, TSensor]


#Relays 
VRelayPin = 21 #Valve relay
CRelayPin = 16 #Compressor relay
relaylist = [VRelayPin, CRelayPin]


GPIO.setmode(GPIO.BCM)

for item in sensorlist:
    GPIO.setup(item, GPIO.IN)

for item in relaylist:
    GPIO.setup(item, GPIO.OUT)

ser = serial.Serial('/dev/ttyACM0', 9600) # Maak verbinding met de seriële poort van de Arduino

while True:
    ArduinoData = ser.readline().decode('utf-8').rstrip() # this reads the data from the Arduino and decodes it
    temperature, pressure = map(float, ArduinoData.split(',')) # this splits the data and turns it into two varibles
    print("| Temperature: ", temperature, end="  |  ") # Prints the temurer and pressure in the compersor
    print("Pressure: ", pressure, " |")
    
    if temperature < max_temp and pressure < max_pressure: # Zet de compressor aan als de temperatuur en druk onder de maximale waarde zitten
        CRelay.ON()
    
    if temperature >= max_temp: # Zet de compressor uit als de maximale temperatuur overschreden is
        CRelay.OFF()
        print("The compressor is overheated, it will turn on in 10 minutes.")
        
        countdown = 10
        while countdown: # Start een timer van 10 minuten waarna de compressor weer aan kan
            mins, secs = divmod(countdown, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(timer, end="\r")
            time.sleep(1)
            countdown -= 1
        print("The compressor will turn on again.")
        
    if pressure >= max_pressure: # Zet de compressor uit als de maximale druk is overschreden
        CRelay.OFF()
        print("Battery is charged.")
        while True:
            try:
                start = str(input("Do you want to release the charge? Y / N")) # Vraag of de stroom moet worden opgewekt
                break
            except ValueError:
                continue
        if start == "Y": # Open de klep om de stroom op te wekken tot de druk onder de 105 zit
            while pressure > 105:
                VRelay.ON()
            VRelay.OFF()
        else:
            print("Program closed")
            break
    
        
        