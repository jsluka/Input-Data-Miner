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
space = []
left = []
prevX = 0
prevY = 0
prevW = 0
prevA = 0
prevS = 0
prevD = 0
prevLeft = 0
prevSpace = 0
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
def listAppender(pX,pY,delX,delY,m,pW,pA,pS,pD,pSp,pL):
    posX.append(pX)
    posY.append(pY)
    deltaX.append(delX)
    deltaY.append(delY)
    magnitude.append(m)
    Ws.append(pW)
    As.append(pA)
    Ss.append(pS)
    Ds.append(pD)
    space.append(pSp)
    left.append(pL)

# Commands for individual keypresses
def OnKeyDown(event):
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
    elif event.KeyID == 32:
        global prevSpace
        prevSpace = 1
    return True

# Commands for key release
def OnKeyUp(event):
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
    elif event.KeyID == 32:
        global prevSpace
        prevSpace = 0
    return True

def OnLeftDown(event):
    global prevLeft
    prevLeft = 1
    return True

def OnLeftUp(event):
    global prevLeft
    prevLeft = 0
    return True

# Primary code
tX,tY = queryMousePosition()
prevX = tX
prevY = tY
prevTime = int(round(time.time()*1000))
cTime = 0

hm = pyHook.HookManager()
hm.KeyDown = OnKeyDown
hm.KeyUp = OnKeyUp
hm.MouseLeftDown = OnLeftDown
hm.MouseLeftUp = OnLeftUp
hm.HookKeyboard()
hm.HookMouse()

try:
    while(True): # Logging loop!
        pythoncom.PumpWaitingMessages()
        if capture == 1: # Only logs when F9 was hit
            step = step + 1
            pX,pY = queryMousePosition()
            dX = abs(prevX - pX)
            dY = abs(prevY - pY)
            prevX = pX
            prevY = pY
            mag = math.sqrt((dX*dX)+(dY*dY))
            cTime = int(round(time.time()*1000))
            if(cTime-10 >= prevTime): # Once per 10 milliseconds
                listAppender(pX,pY,dX,dY,mag,prevW,prevA,prevS,prevD,prevSpace,prevLeft)
                prevTime = cTime
        #time.sleep(0.1)
except KeyboardInterrupt:
    pass

# CSV writer
zipped = zip(posX,posY,deltaX,deltaY,magnitude,Ws,As,Ss,Ds,space,left)
timestamp = strftime("%Y-%m-%d-%H-%M-%S",gmtime())
with open("Raw Outputs/%s.csv"%timestamp,"w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(zipped)
