# http://stackoverflow.com/questions/3698635/getting-cursor-position-in-python

# imports
from ctypes import windll, Structure, c_ulong, byref
from time import gmtime,strftime
import time, math, csv, pyHook, pythoncom

# Storage
posX = []
posY = []
deltaX = []
deltaY = []
magnitude = []
Ws = []
As = []
Ss = []
Ds = []
prevX = 0
prevY = 0
prevW = 0
prevA = 0
prevS = 0
prevD = 0
capture = 0
step = 0

# Mouse Position
class POINT(Structure):
    _fields_ = [("x",c_ulong),("y",c_ulong)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x,pt.y

# Appends all of the lists
def listAppender(pX,pY,delX,delY,m,pW,pA,pS,pD):
    posX.append(pX)
    posY.append(pY)
    deltaX.append(delX)
    deltaY.append(delY)
    magnitude.append(m)
    Ws.append(pW)
    As.append(pA)
    Ss.append(pS)
    Ds.append(pD)

# Commands for individual keypresses
def onDown(event):
    if event.KeyID == 120:
        print("Toggle logging...")
        global capture
        capture = 1 - capture
    elif event.KeyID == 65:
        global prevA
        prevA = 1
    elif event.KeyID == 83:
        global prevS
        prevS = 1
    elif event.KeyID == 87:
        global prevW
        prevW = 1
    elif event.KeyID == 68:
        global prevD
        prevD = 1
    return True

# Commands for key release
def onUp(event):
    if event.KeyID == 65:
        global prevA
        prevA = 0
    if event.KeyID == 83:
        global prevS
        prevS = 0
    if event.KeyID == 87:
        global prevW
        prevW = 0
    if event.KeyID == 68:
        global prevD
        prevD = 0
    return True

# Primary code
tX,tY = queryMousePosition()
prevX = tX
prevY = tY

hm = pyHook.HookManager()
hm.KeyDown = onDown
hm.KeyUp = onUp
hm.HookKeyboard()

try:
    while(True): # Logging loop!
        pythoncom.PumpWaitingMessages()
        step = step + 1
        pX,pY = queryMousePosition()
        dX = abs(prevX - pX)
        dY = abs(prevY - pY)
        prevX = pX
        prevY = pY
        mag = math.sqrt((dX*dX)+(dY*dY))
        if capture == 1: # Only logs when F9 was hit
            listAppender(pX,pY,dX,dY,mag,prevW,prevA,prevS,prevD)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

# CSV writer
zipped = zip(posX,posY,deltaX,deltaY,magnitude,Ws,As,Ss,Ds)
timestamp = strftime("%Y-%m-%d-%H-%M-%S",gmtime())
with open("Raw Outputs/%s.csv"%timestamp,"w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(zipped)
