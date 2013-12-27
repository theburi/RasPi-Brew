# coding=utf-8
## This is a brewtroller port to Python
##All credits goes to brewtroller
## TODO need to put better diclamer

from Enum import *
from timer import *
from hardwarecontrol import resetHeatOutput


# unsigned long lastHop, grainInStart;
# unsigned int boilAdds, triggered;


# Used to determine if the given step is the active step in the program.

def stepIsActive(brewStep):
    if (stepProgram[brewStep] == PROGRAM_IDLE):
        return False
    else:
        return True


# Usd to determine if the given ZONE is the active ZONE in the program.
# Returns true is any step in the given ZONE is the active step, false otherwise.

def zoneIsActive(brewZone):
    if (brewZone == ZONE_MASH):
        if stepIsActive(STEP_FILL): return 1
        if stepIsActive(STEP_DELAY): return 1
        if stepIsActive(STEP_PREHEAT): return 1
        if stepIsActive(STEP_ADDGRAIN): return 1
        if stepIsActive(STEP_REFILL): return 1
        if stepIsActive(STEP_DOUGHIN): return 1
        if stepIsActive(STEP_ACID): return 1
        if stepIsActive(STEP_PROTEIN): return 1
        if stepIsActive(STEP_SACCH): return 1
        if stepIsActive(STEP_SACCH2): return 1
        if stepIsActive(STEP_MASHOUT): return 1
        if stepIsActive(STEP_MASHHOLD): return 1
        if stepIsActive(STEP_SPARGE):
            return 1
        else:
            return 0
    elif (brewZone == ZONE_BOIL):
        if (stepIsActive(STEP_BOIL) or stepIsActive(STEP_CHILL) ):
            return 1
        else:
            return 0;


# Returns 0 if start was successful or 1 if unable to start due to conflict with other step
# Performs any logic required at start of step
# TO DO: Power Loss Recovery Handling
def stepInit(pgm, brewStep):
    print pgm, brewStep

    # Nothing more to do if starting 'Idle' program
    if (pgm == PROGRAM_IDLE): return 1

    # Abort Fill/Mash step init if mash Zone is not free
    if (brewStep >= STEP_FILL and brewStep <= STEP_MASHHOLD and zoneIsActive(ZONE_MASH)):
        return 1
    # Abort sparge init if either zone is currently active
    elif (brewStep == STEP_SPARGE and (zoneIsActive(ZONE_MASH) or zoneIsActive(ZONE_BOIL))):
        return 1
    # Allow Boil step init while sparge is still going

    # If we made it without an abort, save the program number for stepCore
    setProgramStep(brewStep, pgm)

    #    if (brewStep == STEP_FILL):
    #   Step Init: Fill
    #   REMOVED Section   

    if (brewStep == STEP_DELAY):
        # Step Init: Delay
        # Load delay minutes from EEPROM if timer is not already populated via Power Loss Recovery
        if ( timerValue[TIMER_MASH] == 0 ): setTimer(TIMER_MASH, BrewConfig['StartDelayMinutes'])
        print "Step Delay Initialized with time: " + str(timerValue[TIMER_MASH])

    elif (brewStep == STEP_PREHEAT):
        #  //Step Init: Preheat

        setpoint[VS_MASH] = calcStrikeTemp(pgm)

        preheated[VS_MASH] = 0
        #   No timer used for preheat
        clearTimer(TIMER_MASH)

    elif (brewStep == STEP_ADDGRAIN):
        # Step Init: Add Grain
        # Disable HLT and Mash heat output during 'Add Grain' to avoid
        # dry running heat elements and burns from HERMS recirc
        resetHeatOutput(VS_MASH)
        # In manual volume mode show the target mash volume as a guide to the user
        ## TODO tgtVol[VS_MASH] = mashVol





    elif brewStep == STEP_DOUGHIN:
    # Step Init: Dough In

        setpoint[VS_MASH] = getProgMashTemp(pgm, MASH_DOUGHIN);
        preheated[VS_MASH] = 0;

        #    //Set timer only if empty (for purposed of power loss recovery)
        if (not (timerValue[TIMER_MASH])):
            setTimer(TIMER_MASH, getProgMashMins(pgm, MASH_DOUGHIN));
        #    //Leave timer paused until preheated
        pauseTimer(TIMER_MASH)
        print "Initializing Dough In..."

    elif (brewStep == STEP_ACID):
    #  //Step Init: Acid Rest

        setpoint[TS_MASH] = getProgMashTemp(pgm, MASH_ACID);
        preheated[VS_MASH] = 0;
        #    //Set timer only if empty (for purposed of power loss recovery)
        if (not (timerValue[TIMER_MASH])):
            setTimer(TIMER_MASH, getProgMashMins(pgm, MASH_ACID));
            #    //Leave timer paused until preheated
        timerStatus[TIMER_MASH] = 0;

    elif (brewStep == STEP_PROTEIN):
        # Step Init: Protein        
        setpoint[TS_MASH] = getProgMashTemp(pgm, MASH_PROTEIN);
        preheated[VS_MASH] = 0;

        # Set timer only if empty (for purposed of power loss recovery)
        if (not (timerValue[TIMER_MASH])):
            setTimer(TIMER_MASH, getProgMashMins(pgm, MASH_PROTEIN));
            # Leave timer paused until preheated
        timerStatus[TIMER_MASH] = 0;

    elif (brewStep == STEP_SACCH):
        #  //Step Init: Sacch
        print "Initializing SACCH ..."
        setpoint[TS_MASH] = getProgMashTemp(pgm, MASH_SACCH);
        preheated[VS_MASH] = 0;
        #    //Set timer only if empty (for purposed of power loss recovery)
        if (not (timerValue[TIMER_MASH])):
            setTimer(TIMER_MASH, getProgMashMins(pgm, MASH_SACCH));
            #    //Leave timer paused until preheated
        timerStatus[TIMER_MASH] = 0;

    elif (brewStep == STEP_SACCH2):
        #  //Step Init: Sacch2
        print "Initializing SACH2 ..."
        setpoint[TS_MASH] = getProgMashTemp(pgm, MASH_SACCH2);
        preheated[VS_MASH] = 0;
        #    //Set timer only if empty (for purposed of power loss recovery)
        if (not (timerValue[TIMER_MASH])):
            setTimer(TIMER_MASH, getProgMashMins(pgm, MASH_SACCH2));
            #    //Leave timer paused until preheated
        timerStatus[TIMER_MASH] = 0;

    elif (brewStep == STEP_MASHOUT):
        #  //Step Init: Mash Out
        print "Initializing MashOut ..."
        setpoint[TS_MASH] = getProgMashTemp(pgm, MASH_MASHOUT);
        preheated[VS_MASH] = 0;
        #    //Set timer only if empty (for purposed of power loss recovery)
        if (not (timerValue[TIMER_MASH])):
            setTimer(TIMER_MASH, getProgMashMins(pgm, MASH_MASHOUT));
            #    //Leave timer paused until preheated
        timerStatus[TIMER_MASH] = 0;
        print "Exit Initialization MashOut ..."

    elif (brewStep == STEP_MASHHOLD):
        print "Initializing MASH HOLD step ", setpoint[TS_MASH]
        #    //Set HLT to Sparge Temp
        #    //Cycle through steps and use last non-zero step for mash setpoint
        if (not (setpoint[TS_MASH])):
            i = MASH_MASHOUT;
        while (setpoint[TS_MASH] == 0 and i >= MASH_DOUGHIN and i <= MASH_MASHOUT):
            i = i - 1
            setSetpoint[TS_MASH] = getProgMashTemp(pgm, i)

    elif (brewStep == STEP_BOIL):
        #  //Step Init: Boil
        print "Initializing BOIL step ", setpoint[TS_MASH]
        ## TODO Pump
        ## resetHeatOutput(VS_PUMP); # turn off the pump if we are moving to boil. 
        setpoint[VS_KETTLE] = getBoilTemp();
        preheated[VS_KETTLE] = 0;
        ##boilAdds = getProgAdds(pgm);

        #    //Set timer only if empty (for purposes of power loss recovery)
        if (not (timerValue[TIMER_BOIL])):
        #      //Clean start of Boil
            setTimer(TIMER_BOIL, getProgBoil(pgm));
            triggered = 0;
            ##setBoilAddsTrig(triggered);
            ##else :
        #      //Assuming power loss recovery
        ##triggered = getBoilAddsTrig();

        #    //Leave timer paused until preheated
        timerStatus[TIMER_BOIL] = 0;
        lastHop = 0;
        ##boilControlState = CONTROLSTATE_AUTO;

    elif (brewStep == STEP_CHILL):
    #  //Step Init: Chill
        pitchTemp = getProgPitch(pgm);


    #  //Call event handler
    ##  TODO replace event with writing to file so that webserver can pick up
    #eventHandler(EVENT_STEPINIT, brewStep)


def stepCore():
    global stepProgram
    if (stepIsActive(STEP_FILL)):
        print "Running Active Step fill"
        stepFill(STEP_FILL);

    if (stepIsActive(STEP_PREHEAT)):
        print "Running Active step Preheat", temp[VS_MASH], "; target ", setpoint[VS_MASH]
        if (setpoint[VS_MASH] and temp[VS_MASH] >= setpoint[VS_MASH]):
            stepAdvance(STEP_PREHEAT);

    if (stepIsActive(STEP_DELAY)):
        print "Running Active Delay Step"
        if (timerValue[TIMER_MASH] == 0):
            stepAdvance(STEP_DELAY);

    if (stepIsActive(STEP_ADDGRAIN)):
        ## TODO understand how input would work here
        stepAdvance(STEP_ADDGRAIN)

    if (stepIsActive(STEP_REFILL)):
        stepFill(STEP_REFILL);

    for brewStep in range(STEP_DOUGHIN, STEP_MASHOUT + 1):
        if (stepIsActive(brewStep)):
            stepMash(brewStep);

    if (stepIsActive(STEP_MASHHOLD)):
        print "Running MASH HOLD. Boil ZONE is ", zoneIsActive(ZONE_BOIL)
        if ( not (zoneIsActive(ZONE_BOIL))):
            stepAdvance(STEP_MASHHOLD);

    if (stepIsActive(STEP_SPARGE)):
        stepAdvance(STEP_SPARGE);

    if (stepIsActive(STEP_BOIL)):
        print "BOILING ", timerValue[TIMER_BOIL]
        #    PREBOIL_ALARM
        ## TODO figure this out
        ##        if not((triggered & 32768) and temp[TS_KETTLE] >= PREBOIL_ALARM) :
        ##            setAlarm(1);
        ##            triggered |= 32768;
        ##            setBoilAddsTrig(triggered);

        if not (preheated[VS_KETTLE] and temp[TS_KETTLE] >= setpoint[VS_KETTLE] and setpoint[VS_KETTLE] > 0):
            preheated[VS_KETTLE] = 1;
            #         //Unpause Timer
            if not (timerStatus[TIMER_BOIL]): pauseTimer(TIMER_BOIL);

        ## TODO need to figure out boil addition logic at some stage
        ##    if (preheated[VS_KETTLE]) :
        ###      //Boil Addition
        ##        if ((boilAdds <> triggered) and 1):
        ##            lastHop = millis();
        ##            setAlarm(1);
        ##            triggered |= 1;
        ##            setBoilAddsTrig(triggered);
        ##
        ###      //Timed additions (See hoptimes[] array at top of AutoBrew.pde)
        ##        for i in range(0,9):
        ##            if (((boilAdds <> triggered) and (1<<(i + 1))) and timerValue[TIMER_BOIL] <= hoptimes[i] * 60000):
        ##                lastHop = millis();
        ##                setAlarm(1);
        ##                triggered |= (1<<(i + 1));
        ##                setBoilAddsTrig(triggered);

        #    //Exit Condition  
        if (preheated[VS_KETTLE] and timerValue[TIMER_BOIL] == 0):
            stepAdvance(STEP_BOIL);

    if (stepIsActive(STEP_CHILL)):
        stepAdvance(STEP_CHILL);

    if (stepIsActive(STEP_DONE)):
        global EXIT
        print "Exiting"
        EXIT = True

#//stepCore logic for Fill and Refill
def stepFill(brewStep):
    # TODO add loginc to wait to start for fill stage aka Manual fill
    stepAdvance(brewStep)


#//stepCore Logic for all mash steps
def stepMash(brewStep):
#    smartHERMSHLT();

    if not (preheated[VS_MASH] and temp[VS_MASH] >= setpoint[VS_MASH]):
        preheated[VS_MASH] = 1;
    #    //Unpause Timer
    if not (timerStatus[TIMER_MASH]): pauseTimer(TIMER_MASH)

    #  //Exit Condition (and skip unused mash steps)
    print "DEBUG: Exit Conditions ", setpoint[VS_MASH] == 0, preheated[VS_MASH], timerValue[TIMER_MASH] == 0

    if (setpoint[VS_MASH] == 0 or (preheated[VS_MASH] and timerValue[TIMER_MASH] == 0)):
        stepAdvance(brewStep);


#//Advances program to next brew step
#//Returns 0 if successful or 1 if unable to advance due to conflict with another step
def stepAdvance(brewStep):
#  //Save program for next step/rollback
    program = stepProgram[brewStep];
    stepExit(brewStep);
    #  //Advance step (if applicable)
    if (brewStep + 1 < NUM_BREW_STEPS):
        if (stepInit(program, brewStep + 1)):
        #          //Init Failed: Rollback
            stepExit(brewStep + 1); #//Just to make sure we clean up a partial start
            setProgramStep(program, brewStep); #//Show the step we started with as active
            print "Step Advance ->" + str(brewStep)
            return 1;

        #  //Init Successful
    return 0;


#//Performs exit logic specific to each step
#//Note: If called directly (as opposed through stepAdvance) acts as a program abort
def stepExit(brewStep):
#  //Mark step idle
    setProgramStep(brewStep, PROGRAM_IDLE);

    #  //Perform step closeout functions

    if (brewStep == STEP_DELAY):
    #  //Step Exit: Delay
        clearTimer(TIMER_MASH);

    elif (brewStep == STEP_ADDGRAIN):
    #  //Step Exit: Add Grain
        print "Exit Add Grain"

    elif (brewStep == STEP_PREHEAT or (brewStep >= STEP_DOUGHIN and brewStep <= STEP_MASHHOLD)):
    #  //Step Exit: Preheat/Mash
        clearTimer(TIMER_MASH);

        resetHeatOutput(VS_MASH);

    #    elif (brewStep == STEP_SPARGE):
    #  //Step Exit: Sparge

    elif (brewStep == STEP_BOIL):
    #  //Step Exit: Boil
    #    TODO 0 Min Addition
    ##    if ((boilAdds ^ triggered) & 2048):
    ##        setAlarm(1);
    ##        triggered |= 2048;
    ##        setBoilAddsTrig(triggered);
    ##        delay(HOPADD_DELAY);

        resetHeatOutput(VS_KETTLE);
        clearTimer(TIMER_BOIL);

#    elif (brewStep == STEP_CHILL):
#  //Step Exit: Chill

##  TODO replace event with writing to file so that webserver can pick up
##    eventHandler(EVENT_STEPEXIT, brewStep);


#def resetSpargeValves():

#ifdef SMART_HERMS_HLT
#void smartHERMSHLT() {
#  if (setpoint[VS_MASH] != 0) setpoint[VS_HLT] = constrain(setpoint[VS_MASH] * 2 - temp[TS_MASH], setpoint[VS_MASH] + MASH_HEAT_LOSS * SETPOINT_DIV * 100, HLT_MAX_TEMP *  SETPOINT_DIV * 100);
#}
#endif
##  
##unsigned long calcStrikeVol(byte pgm) {
##  unsigned int mashRatio = getProgRatio(pgm);
##  unsigned long retValue;
##  if (mashRatio) {
##    retValue = round(getProgGrain(pgm) * mashRatio / 100.0);
##
##    //Convert qts to gal for US
##    #ifndef USEMETRIC
##      retValue = round(retValue / 4.0);
##    #endif
##    retValue += getVolLoss(TS_MASH);
##  }
##  else {
##    //No Sparge Logic (Matio Ratio = 0)
##    retValue = calcPreboilVol(pgm);
##  
##    //Add Water Lost in Spent Grain
##    retValue += calcGrainLoss(pgm);
##    
##    //Add Loss from other Vessels
##    retValue += (getVolLoss(TS_HLT) + getVolLoss(TS_MASH));
##  }
##  
##  #ifdef DEBUG_PROG_CALC_VOLS
##    logStart_P(LOGDEBUG);
##    logField_P(PSTR(StrikeVol:));
##    logFieldI( retValue);
##    logEnd();
##  #endif
##  
##  return retValue;
##}

##
##
##def calcGrainLoss(byte pgm) {
##  unsigned long retValue;
##  retValue = round(getProgGrain(pgm) * GRAIN_VOL_LOSS);
##  
##  #ifdef DEBUG_PROG_CALC_VOLS
##    logStart_P(LOGDEBUG);
##    logField_P(PSTR(GrainLoss));
##    logFieldI(retValue);
##    logEnd();
##  #endif
##  
##  return retValue;
##}
##
##unsigned long calcGrainVolume(byte pgm) {
##  return round (getProgGrain(pgm) * GRAIN2VOL);
##}

##
## Calculates the strike temperature for the mash.
##
def calcStrikeTemp(pgm):
    strikeTemp = getFirstStepTemp(pgm);
    ## TODO Calculate
    ##return (strikeTemp + round(.4 * (strikeTemp - getGrainTemp()) / (calcStrikeVol(pgm) / getProgGrain(pgm))) + 1.7 + STRIKE_TEMP_OFFSET) * SETPOINT_DIV;
    return BrewConfig["StrikeWaterTemp"]


def getFirstStepTemp(pgm):
    firstStep = 0;
    i = MASH_DOUGHIN;
    while (firstStep == 0 and i <= MASH_MASHOUT):
        firstStep = BrewConfig["MASH_TEMP"][i];
        i = i + 1
    return firstStep;


def setProgramStep(brewStep, actPgm):
    global stepProgram

    stepProgram[brewStep] = actPgm


def getProgPitch(pgm):
    ##TODO calc pitch temp
    return 70


def getProgMashTemp(actStep, mashstep):
    return BrewConfig["MASH_TEMP"][mashstep]


def getProgMashMins(actStep, mashstep):
    return BrewConfig["MASH_MINUTES"][mashstep]


def getBoilTemp():
    return BrewConfig["BOIL_TEMP"]


def getProgBoil(pgm):
    return BrewConfig["BOIL_TIME"]
