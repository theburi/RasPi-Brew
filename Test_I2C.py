import smbus
import time
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

# commands list
SetPinCommand = 0X1
GetTemparatureCommand = 0X02
SetHeatPowerCommand = 0x03
ShowModeCommand = 0X04

t = 0
heat=False

def HeatPower (val):
    global heat
    ##bus.write_i2c_block_data(address, SetHeatPowerCommand, val)
    if val>0 : heat = True
    else: heat = False

def GetTemperature():
    global t
    if heat : t += 5
    else:
        if t>0 : t = t - 1
    
    return t

def showMode(value):
    # bus.write_byte(address, value)    
    bValues = StringToBytes(value)    
    bus.write_i2c_block_data(address, ShowModeCommand, bValues)
    time.sleep(1)
    return -1

def readCommand():
    # number = bus.read_byte(address)
    cmd = 0x01
    
    res = bus.read_i2c_block_data(address, cmd)
    return res

def StringToBytes(val):
    retVal = []
    for c in val:
        retVal.append(ord(c))
        print ord(c)
    return retVal

def resetHeatOutput(vessel):
    #send command to turn of heating
    heat =False
    #HeatPower(0)

##    
##var = "mash 3"
##
##showMode(var)
##print "RPI: Hi Arduino, I sent you ", var
### sleep one second
##time.sleep(2)
##
##number = readCommand()
##print "Arduino: Hey RPI, I received a digit ", number
##print


