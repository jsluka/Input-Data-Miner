import pyHook, pythoncom
from time import gmtime,strftime
import time, csv

prev = 0
p = []

def OnDown(event):
    global prev
    prev = 1
    return True

def OnUp(event):
    global prev
    prev = 0
    return True

hm = pyHook.HookManager()
hm.KeyDown = OnDown
hm.KeyUp = OnUp
hm.HookKeyboard()

it = 0
while(it < 100):
    p.append(prev)
    pythoncom.PumpWaitingMessages()
    print(len(p))
    it = it + 1
    time.sleep(0.1)

timestamp = strftime("INPUT2-%Y-%m-%d-%H-%M-%S",gmtime())
with open("Raw Outputs/%s.csv"%timestamp,"w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(p)
