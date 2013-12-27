import time
import RPi.GPIO as GPIO


# This is the address we setup in the Arduino Program
heatpin = 11
temperatureAddress='28-000003ca28a5'


# Use the pin numbers from the ribbon cable board.
GPIO.setmode(GPIO.BCM)
# Set up the pin you are using ("18" is an example) as output.
GPIO.setup(heatpin, GPIO.OUT)

t = 0
heat = False


def HeatPower(val):
    global heat
    ##bus.write_i2c_block_data(address, SetHeatPowerCommand, val)
    if val > 0:
        heat = True
        # Turn on the pin and see the LED light up.
        GPIO.output(heatpin, GPIO.HIGH)

    else:
        heat = False
        GPIO.output(heatpin, GPIO.LOW)


def GetTemperature():
    global t
    #if heat:
    #    t += 5
    #else:
    #    if t > 0: t -= 1

    tfile = open("/sys/bus/w1/devices/%s/w1_slave" % temperatureAddress)
    text = tfile.read()
    tfile.close()
    temperature_data = text.split()[-1]
    t = float(temperature_data[2:])
    t /= 1000

    return t


def resetHeatOutput(vessel):
    #send command to turn of heating
    HeatPower(False)
    #HeatPower(0)


