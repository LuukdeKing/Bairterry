import psutil
import RPi.GPIO as GPIO

import VRelay
import CRelay

GPIO.setmode(GPIO.BCM)

#Relays 
VRelayPin = 21 #Valve relay
CRelayPin = 16 #Compressor relay
relaylist = [VRelayPin, CRelayPin]

for item in relaylist:
    GPIO.setup(item, GPIO.OUT)

VRelay.OFF()
CRelay.OFF()

def stop_process(name):
    for process in psutil.process_iter():
        if process.name() == name:
            process.terminate()
            print(f"Terminating {name} process with PID {process.pid}")
            
stop_process("python")  # terminate all Python processes


