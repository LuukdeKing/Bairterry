import RPi.GPIO as GPIO
VRelayPin = 21
def ON():
    GPIO.output(VRelayPin, 0)

def OFF():
    GPIO.output(VRelayPin, 1)