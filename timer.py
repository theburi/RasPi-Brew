from Enum import *
import datetime
from time import mktime

timerValue = [0]*2
lastTime = [0]*2
timerStatus = [0]*2

def setTimer(timer, minutes):
    if (not(minutes == -1)):
#    //A cancel action as not been selected!
        timerValue[timer] = datetime.timedelta( minutes=minutes);
        lastTime[timer] = datetime.datetime.now()
        timerStatus[timer] = 1;
        setTimerStatus(timer, 1);
        setTimerRecovery(timer, minutes);

def pauseTimer(timer):
    if (timerStatus[timer]):
#    //Pause
        timerStatus[timer] = 0;
    else:
    #    //Unpause
        timerStatus[timer] = 1;
        lastTime[timer] = datetime.datetime.now()
 
    setTimerStatus(timer, timerStatus[timer]);


def clearTimer(timer):
    timerValue[timer] = 0;
    timerStatus[timer] = 0;
    setTimerStatus(timer, 0);
    setTimerRecovery(timer, 0);


def updateTimers():
    dt = datetime.datetime.now()
    for timer in range (TIMER_MASH, TIMER_BOIL+1) :
        if (timerStatus[timer]):
            now = dt
        
            if (timerValue[timer] > now - lastTime[timer]):
                timerValue[timer] = timerValue[timer]- (now - lastTime[timer]);

            else :
                timerValue[timer] = 0;
                timerStatus[timer] = 0;
                setTimerStatus(timer, 0);
                setTimerRecovery(timer, 0); #// KM - Moved this from below to be event driven
                # TODO setAlarm(1);

            lastTime[timer] = now;
       
        timerHours = timerValue[timer] / 3600000;
        timerMins = (timerValue[timer] - timerHours * 3600000) / 60000;

##
###//This function allows modulation of buzzer when the alarm is on.
##def updateBuzzer():
###  //Retreive the status of the alarm. (Removed by Matt. This value is always in memory)
###  //byte alarmStatus = bitRead(EEPROM.read(306), 2);
###  //Set the buzzer according the user custom buzzer modulation 
##    setBuzzer(alarmStatus); 
##
##
##def setAlarm(alarmON):
##    setAlarmStatus(alarmON);
##    setBuzzer(alarmON);
##
###//This function allow to modulate the sound of the buzzer when the alarm is ON. 
###//The modulation varies according the custom parameters.
###//The modulation occurs when the buzzerCycleTime value is larger than the buzzerOnDuration
##def setBuzzer(alarmON):
##  if (alarmON) {
##    #ifdef BUZZER_CYCLE_TIME
##      //Alarm status is ON, Buzzer will go ON or OFF based on modulation.
##      //The buzzer go OFF for every moment passed in the OFF window (low duty cycle). 
##      unsigned long now = millis(); //What time is it? :-))      
##      
##      //Now, by elimation, identify scenarios where the buzzer will go off. 
##      if (now < buzzerCycleStart + BUZZER_CYCLE_TIME) {
##        //At this moment ("now"), the buzzer is in the OFF window (low duty cycle). 
##        if (now > buzzerCycleStart + BUZZER_ON_TIME) {
##          //At this moment ("now"), the buzzer is NOT within the ON window (duty cycle) allowed inside the buzzer cycle window.
##          //Set or keep the buzzer off
##          alarmPin.set(0); 
##        }
##      } else {
##        //The buzzer go ON for every moment where buzzerCycleStart < "now" < buzzerCycleStart + buzzerOnDuration
##        alarmPin.set(1); //Set the buzzer On 
##        buzzerCycleStart = now; //Set a new reference time for the begining of the buzzer cycle.
##      }
##    #else
##      alarmPin.set(1); //Set the buzzer On 
##    #endif
##  } else {
##    //Alarm status is OFF, Buzzer goes Off
##    alarmPin.set(0);
##  }
##}

def setTimerStatus( timer, value):
    timerStatus[timer] = value;

def setTimerRecovery(timer, newMins):
    if not (newMins == -1):
        newMins=0
