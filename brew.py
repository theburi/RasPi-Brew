#!/usr/bin/env python

## this is a main module to run main loop
import logging
from random import random
import traceback
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

    stepProgram[STEP_FILL] = STEP_FILL
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
    BrewConfig["MASH_MINUTES"] = [0, 0, 0, 1, 5, 5]
    BrewConfig["StrikeWaterTemp"] = 70
    BrewConfig["BOIL_TEMP"] = 100
    BrewConfig["BOIL_TIME"] = 5

    stepInit(STEP_FILL, STEP_FILL)

    ## TODO understand how mashVol and tgtVol[VS_MASH] works

    ## Initialize system

    setpoint[VS_MASH] = 0


def WriteState():
    global stepProgram
    global ProgramNames
    # <membership/>
    membership = Element('state')

    # <membership><users/>
    steps = SubElement(membership, 'steps')
    for key, step in enumerate(stepProgram):
        StepNode = SubElement(steps, 'step', attrib={'name': ProgramNames[key], 'status': str(step)})

    temperature = SubElement(membership, 'temperature')
    temperature.text = str(temp[VS_MASH])
    heaterStatus = SubElement(membership, 'heater')
    heaterStatus.text = str(HeatStatus[VS_MASH])

    try:
        output_file = open(pipeName, 'w')
        output_file.write('<?xml version="1.0"?>')
        output_file.write(ElementTree.tostring(membership))
        output_file.close()
    except Exception as e:
        print e
        traceback.print_exc()
        raise


##
## Start of main section

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('brewpi.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.info('Starting BrewPi ....')

LoadProgram()

while not EXIT:

    try:
        updateTimers()

        temp[VS_MASH] = GetTemperature()

        UpdateOutputs()

        ##processUserCommands()

        WriteState()

        EXIT = stepCore()

    except Exception as e:

        logger.critical(e.message, exc_info=True)
        time.sleep(100)

    time.sleep(2)


