## this is a main module to run main loop
from steplogic import *
from Enum import *
import time
from timer import updateTimers
from Test_I2C import GetTemperature

EXIT = False




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

    BrewConfig["StartDelayMinutes"] = 0
    BrewConfig["MASH_TEMP"] = [0,0,0,0,0,0]
    BrewConfig["StrikeWaterTemp"] = 70 

##
## Start of main section

LoadProgram()
while not (EXIT):
    print stepProgram
    
    updateTimers()

    temp[VS_MASH] = GetTemperature()

    stepCore()
    
    time.sleep(2)
    
