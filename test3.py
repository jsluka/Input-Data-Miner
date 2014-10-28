import pyHook, pythoncom
from time import gmtime,strftime
import time, csv

prev = 0
p = []

def OnDown(event):
    print("Down")
    return True

def OnUp(event):
    print("Up")
    return True

hm = pyHook.HookManager()
hm.MouseLeftDown = OnDown
hm.MouseLeftUp = OnUp
hm.HookMouse()

it = 0
while(True):
    pythoncom.PumpWaitingMessages()

#timestamp = strftime("INPUT2-%Y-%m-%d-%H-%M-%S",gmtime())
#with open("Raw Outputs/%s.csv"%timestamp,"w",newline='') as f:
#    writer = csv.writer(f)
#    writer.writerows(p)
