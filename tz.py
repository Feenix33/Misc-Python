# tz.py
# Simple way to input a time and see the times in other zones
# zones are hardcoded
#
# Sets the DFW time and then calculates everything else from there
#

import sys
from datetime import datetime, timedelta
zoneOff = [('dfw', 0, 0), ('blr', 10, 30), ('krk', 7, 0)]
dfwTime = datetime.now()

def printUsage():
    print("Incorrect usage")

def validZone(zone):
    global zoneOff
    if len([item for item in zoneOff if item[0] == zone]) >= 1:
        return True
    return False

def setDFW(inZone, inTime):
    global dfwTime
    for zn, offH, offM in zoneOff:
        if zn == inZone:
            dfwTime = inTime - timedelta(hours=offH, minutes=offM)

def printList():
    global dfwTime
    for zn, offH, offM in zoneOff:
        localTime = dfwTime + timedelta(hours=offH, minutes=offM) 
        print (zn.upper(), localTime.strftime("%H:%M"), "  |  ", localTime.strftime("%I:%M"))

def main():
    if len(sys.argv) == 1: #no arguments
        inZone = 'dfw'
        inTime = datetime.now()
    elif len(sys.argv) == 2: #one argument, assume a local time
        inZone = 'dfw'
        try:
            inTime = datetime.strptime(sys.argv[1], '%H:%M')
        except ValueError:
            printUsage()
            exit()
    else:
        inZone = sys.argv[1].lower()
        try:
            inTime = datetime.strptime(sys.argv[2], '%H:%M')
        except ValueError:
            printUsage()
            exit()

    if not validZone(inZone):
        inZone = 'dfw'
        print ("ERROR: Changing zone to DFW")

    setDFW(inZone, inTime)
    printList()


if __name__ == '__main__':
    main()
