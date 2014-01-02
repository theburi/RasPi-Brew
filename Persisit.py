import os, stat
from random import random

a_id = 0
pipeName = '/tmp/brewState.xml'
ActionPipeName = '/tmp/ActionPipeName'


def SetUserAction(text, action):
    try:
        a_id = int(random() * 100) + 1
        output_file = open(ActionPipeName, "w")
        output_file.write('%s;%s;%s\n' % (text, action, a_id))
        output_file.close()
        st = os.stat(ActionPipeName)
        os.chmod(ActionPipeName, stat.S_IRWXO)
    except:
        print 'Error'


def WaitForUserAction():
    if not (os.path.exists(ActionPipeName)):
        file = open(ActionPipeName, 'w')
        file.close()

    output_file = open(ActionPipeName, "r")
    for line in output_file:
        if len(line) > 3:
            [text, action, number] = line.split(';')
            if int(number) > 0:
                return False

    return True
