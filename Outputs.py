from Enum import *
from hardwarecontrol import GetTemperature
from hardwarecontrol import HeatPower


def UpdateOutputs():
    global HeatStatus

    if ESTOP:
        HeatStatus[VS_MASH] = 0
        HeatPower(0)
        return

    if temp[VS_MASH] < setpoint[VS_MASH]:
        HeatStatus[VS_MASH] = 1
        HeatPower(255)
    else:
        HeatStatus[VS_MASH] = 0
        HeatPower(0)
