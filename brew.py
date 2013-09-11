## this is a main module to run main loop
from steplogic import *
from Enum import *
import time
from timer import updateTimers
from Test_I2C import GetTemperature
from Outputs import UpdateOutputs

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
    BrewConfig["MASH_TEMP"] = [30,40,50,60,70,80]
    BrewConfig["MASH_MINUTES"] = [1,1,1,1,2,1]
    BrewConfig["StrikeWaterTemp"] = 70

    ## TODO understand how mashVol and tgtVol[VS_MASH] works
    
    ## Initialize system

    setpoint[VS_MASH]=0

##
## Start of main section

LoadProgram()
while not (EXIT):    
    
    updateTimers()

    temp[VS_MASH] = GetTemperature()

    UpdateOutputs ()

    ##processUserCommands()

    ##WriteState()

    stepCore()
    
    time.sleep(2)
    
