from Enum import *
from Test_I2C import GetTemperature
from Test_I2C import HeatPower


def UpdateOutputs():
    global heatstatus
    
    if ESTOP:
        heatstatus[VS_MASH] = 0
        HeatPower(0)
        return
        
    
    if temp[VS_MASH] < setpoint[VS_MASH] :
        heatstatus[VS_MASH] = 1
        HeatPower(255)
    else:
        heatstatus[VS_MASH] = 0
        HeatPower(0)
