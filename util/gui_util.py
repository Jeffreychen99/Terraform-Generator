from tkinter import *

def createFrame(master, x, y, w, h):
	f = Frame(master, width=w, height=h)
	f.pack_propagate(0) # don't shrink
	f.place(x=x, y=y)
	return f

def placeView(master, cls, x, y, w, h, *args, **kwargs):
	f = createFrame(master, x, y, w, h)
	view = cls(f, *args, **kwargs)
	view.pack(fill=BOTH, expand=1)
	return view













