## this is a main module to run main loop
from random import random
from steplogic import *
from Enum import *
import time
from timer import updateTimers
from hardwarecontrol import GetTemperature
from Outputs import UpdateOutputs
import os
import errno
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement


EXIT = False
pipeName = '/tmp/brewState.xml'
ActionPipeName = '/tmp/ActionPipeName'


def LoadProgram():
    global stepProgram
    global BrewConfig

    stepProgram[STEP_FILL] = PROGRAM_IDLE
    stepProgram[STEP_DELAY] = PROGRAM_IDLE
    stepProgram[STEP_PREHEAT] = PROGRAM_IDLE
    stepProgram[STEP_ADDGRAIN] = PROGRAM_IDLE
    stepProgram[STEP_REFILL] = PROGRAM_IDLE
    stepProgram[STEP_DOUGHIN] = PROGRAM_IDLE
    stepProgram[STEP_ACID] = PROGRAM_IDLE
    stepProgram[STEP_PROTEIN] = PROGRAM_IDLE
    stepProgram[STEP_SACCH] = PROGRAM_IDLE
    stepProgram[STEP_SACCH2] = PROGRAM_IDLE
    stepProgram[STEP_MASHOUT] = PROGRAM_IDLE
    stepProgram[STEP_MASHHOLD] = PROGRAM_IDLE
    stepProgram[STEP_SPARGE] = PROGRAM_IDLE
    stepProgram[STEP_BOIL] = PROGRAM_IDLE
    stepProgram[STEP_CHILL] = PROGRAM_IDLE
    stepProgram[STEP_DONE] = PROGRAM_IDLE

    BrewConfig["StartDelayMinutes"] = 0
    BrewConfig["MASH_TEMP"] = [30, 40, 50, 60, 70, 80]
    BrewConfig["MASH_MINUTES"] = [0, 0, 0, 0, 1, 1]
    BrewConfig["StrikeWaterTemp"] = 70
    BrewConfig["BOIL_TEMP"] = 100
    BrewConfig["BOIL_TIME"] = 5

    ## TODO understand how mashVol and tgtVol[VS_MASH] works

    ## Initialize system

    setpoint[VS_MASH] = 0


def WriteState():
# <membership/>
    membership = Element('state')

    # <membership><users/>
    temperature = SubElement(membership, 'temperature')
    temperature.text = str(temp[VS_MASH])
    heaterStatus = SubElement(membership, 'heater')
    heaterStatus.text = str(HeatStatus[VS_MASH])

    try:
        output_file = open(pipeName, 'w')
        output_file.write('<?xml version="1.0"?>')
        output_file.write(ElementTree.tostring(membership))
        output_file.close()
    except:
        print 'Error'


a_id = 0


def SetUserAction(text, action):
    try:
        a_id = int(random() * 100)
        output_file = open(ActionPipeName, "w")
        output_file.write('%s;%s;%s\n' % (text, action, a_id))
    except:
        print 'Error'


def WaitForUserAction():
    output_file = open(ActionPipeName, "r")
    for line in output_file:
        if a_id in line:
            return False

    return True

##
## Start of main section

LoadProgram()

while not (EXIT):
    updateTimers()

    temp[VS_MASH] = GetTemperature()

    UpdateOutputs()

    ##processUserCommands()

    WriteState()

    EXIT = stepCore()

    time.sleep(2)
    
