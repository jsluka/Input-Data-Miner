# https://www.daniweb.com/software-development/python/threads/115282/get-key-press

from tkinter import *
from time import gmtime,strftime
import time, csv

prevW = 0
prevA = 0
prevS = 0
prevD = 0

Ws = []
As = []
Ss = []
Ds = []

def keypress(event):
    if event.keysym == "Escape":
        print("exiting...")
        root.destroy()
    elif event.char == "a":
        global prevA
        prevA = 1
    elif event.char == "s":
        global prevS
        prevS = 1
    elif event.char == "w":
        global prevW
        prevW = 1
    elif event.char == "d":
        global prevD
        prevD = 1

def keyrelease(event):
    if event.char == "a":
        global prevA
        prevA = 0
    if event.char == "s":
        global prevS
        prevS = 0
    if event.char == "w":
        global prevW
        prevW = 0
    if event.char == "d":
        global prevD
        prevD = 0

def logic():
    it = 0
    while(it < 100):
        it = it + 1
        Ws.append(prevW)
        As.append(prevA)
        Ss.append(prevS)
        Ds.append(prevD)
        print(it)
        time.sleep(0.1)
        root.update()

root = Tk()
print("Press ESC to exit")
root.bind_all('<KeyPress>',keypress)
root.bind_all('<KeyRelease>',keyrelease)
root.withdraw()

logic()

zipped = zip(Ws,As,Ss,Ds)
timestamp = strftime("INPUT-%Y-%m-%d-%H-%M-%S",gmtime())
with open("Raw Outputs/%s.csv"%timestamp,"w",newline='') as f:
    writer = csv.writer(f)
    writer.writerows(zipped)
