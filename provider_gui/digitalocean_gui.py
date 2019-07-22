from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import os

from util.tf_util import *
from util.gui_util import *

import util.provider_utils.digitalocean_tf as tf
from tf_generation.terra import *

from resource_gui import Resource_GUI

class digitalocean_gui:

	def __init__(self, master):             
		self.master = master
		self.master.title("Terraform Generator")

	def implement(self, working_directory):
		#self.master.clearScreen()
		print("Performing DigitalOcean")

		os.chdir(working_directory)
		print(os.getcwd())

		width = self.master.winfo_width()
		height = self.master.winfo_height()

		title = placeView(self.master, Label, x=0, y=0, w=width, h=height*0.1)
		title["text"] = "Terraform Infrastructure Generator:   Digital Ocean"
		title["font"] = "Helvetica 25 bold"
		title["bg"] = "#5C4EE5"
		title["fg"] = "white"

		token_label = placeView(self.master, Label, x=width*0.05, y=height*0.125, w=width*0.35, h=height*0.05)
		token_label["anchor"] = 'w'
		token_label["justify"] = 'left'
		token_label["font"] = "fixedsys 18 bold"
		token_label["fg"] = "black"
		token_label["text"] = "Digital Ocean Token:   (required)"
		token = StringVar()
		token_field = placeView(self.master, Entry, x=width*0.05, y=height*0.175, w=width*0.4, h=height*0.05)
		token_field["textvariable"] = token
		token_field["borderwidth"] = 0
		token_field["bg"] = "#dddddd"
		
		fingerprint_label = placeView(self.master, Label, x=width*0.5, y=height*0.125, w=width*0.35, h=height*0.05)
		fingerprint_label["anchor"] = 'w'
		fingerprint_label["justify"] = 'left'
		fingerprint_label["font"] = "fixedsys 18 bold"
		fingerprint_label["fg"] = "black"
		fingerprint_label["text"] = "Secret Key:   (required)"
		fingerprint = StringVar()
		fingerprint_field = placeView(self.master, Entry, x=width*0.5, y=height*0.175, w=width*0.4, h=height*0.05)
		fingerprint_field["textvariable"] = fingerprint
		fingerprint_field["borderwidth"] = 0
		fingerprint_field["bg"] = "#dddddd"

		resources = placeView(self.master, Label, x=width*0.05, y=height*0.375, w=width*0.25, h=height*0.05)
		resources["anchor"] = 'w'
		resources["justify"] = 'left'
		resources["font"] = "fixedsys 18 bold"
		resources["fg"] = "black"
		resources["text"] = "List of Resources:"

		addResourceButtonFrame = createFrame(self.master, x=width*0.05, y=height*0.45, w=width*0.15, h=height*0.05)
		addResourceButton = Button(addResourceButtonFrame, text="Add Resource")
		addResourceButton["command"] = lambda: print("hi")
		addResourceButton["font"] = "fixedsys 15 bold"
		addResourceButton.pack(fill=BOTH, expand=1)

		newResourceLabel = placeView(self.master, Label, x=width*0.225, y=height*0.4, w=width*0.25, h=height*0.05)
		newResourceLabel["anchor"] = 'sw'
		newResourceLabel["justify"] = 'left'
		newResourceLabel["font"] = "fixedsys 15 italic"
		newResourceLabel["fg"] = "#4e4e4e"
		newResourceLabel["text"] = "New Resource Name"
		newResourceName = StringVar()
		newResource = placeView(self.master, Entry, x=width*0.225, y=height*0.45, w=width*0.25, h=height*0.05)
		newResource["textvariable"] = newResourceName
		newResource["borderwidth"] = 0
		newResource["bg"] = "#dddddd"

		resourceListFrame = createFrame(self.master, x=width*0.05, y=height*0.525, w=width*0.425, h=height*0.2)
		resourceListFrame["bg"] = "#eeeeee"
		scrollBar = Scrollbar(resourceListFrame)
		scrollBar.pack(side=RIGHT, fill=Y)

		applyButtonFrame = createFrame(self.master, x=width*0.75, y=height*0.85, w=width*0.2, h=height*0.1)
		applyButton = Button(applyButtonFrame, text="Apply")
		applyButton["command"] = lambda: None
		applyButton["fg"] = "#999999"
		applyButton["font"] = "fixedsys 20 bold"
		applyButton.pack(fill=BOTH, expand=1)

		planButtonFrame = createFrame(self.master, x=width*0.05, y=height*0.85, w=width*0.2, h=height*0.1)
		planFunc = lambda: self.plan(applyButton, token.get())
		planButton = Button(planButtonFrame, command=planFunc , text="Plan")
		planButton["font"] = "fixedsys 20 bold"
		planButton.pack(fill=BOTH, expand=1)

	def plan(self, ab, token):
		tf.createProvider()
		tf.generateKeys()
		tf.storeToken(token)
		tf.init()
		tf.plan()
		if tf.checkValidPlan():
			ab["command"] = self.apply
			ab["fg"] = "#000000"
		else:
			ab["command"] = lambda: None
			ab["fg"] = "#999999"
		print("# Planning complete")

	def apply(self):
		MsgBox = messagebox.askquestion('Apply the current infrastructure plan', 'Are you sure?')
		if MsgBox == "yes":
			tf.apply()















