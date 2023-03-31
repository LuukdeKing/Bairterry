import RPi.GPIO as GPIO
CRelayPin = 16
def ON():
    GPIO.output(CRelayPin, 0)

def OFF():
    GPIO.output(CRelayPin, 1)
