import os
from random import random

a_id = 0
pipeName = '/tmp/brewState.xml'
ActionPipeName = '/tmp/ActionPipeName'


def SetUserAction(text, action):
    try:
        a_id = int(random() * 100)
        output_file = open(ActionPipeName, "w")
        output_file.write('%s;%s;%s\n' % (text, action, a_id))
    except:
        print 'Error'


def WaitForUserAction():

    if not (os.path.exists(ActionPipeName)):
        file = open(ActionPipeName, 'w')
        file.close()


    output_file = open(ActionPipeName, "r")
    for line in output_file:
        if a_id in line:
            return False

    return True
