# http://stackoverflow.com/questions/3698635/getting-cursor-position-in-python

# imports
from ctypes import windll, Structure, c_ulong, byref
import time, math, csv

# Retrieve point
class POINT(Structure):
    _fields_ = [("x",c_ulong),("y",c_ulong)]
def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x,pt.y

# Utility definitions
def listAppender(pX,pY,delX,delY,m):
    posX.append(pX)
    posY.append(pY)
    deltaX.append(delX)
    deltaY.append(delY)
    magnitude.append(m)

# Storage
posX = []
posY = []
deltaX = []
deltaY = []
magnitude = []
prevX = 0
prevY = 0

# Primary code
step = 0
tX,tY = queryMousePosition()
prevX = tX
prevY = tY
while(step < 100):
    step = step + 1
    pX,pY = queryMousePosition()
    dX = abs(prevX - pX)
    dY = abs(prevY - pY)
    prevX = pX
    prevY = pY
    mag = math.sqrt((dX*dX)+(dY*dY))
    print("%5d... POS:(%4d,%4d), DELTA:(%4d,%4d), MAG:(%4.2f)"%(step,pX,pY,dX,dY,mag))
    listAppender(pX,pY,dX,dY,mag)
    time.sleep(0.1)

zipped = zip(posX,posY,deltaX,deltaY,magnitude)
with open("output.csv","w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(zipped)
