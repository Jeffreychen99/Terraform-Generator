from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import os

from util.tf_util import *
from util.gui_util import *

import tf_generators.aws_tf as tf

class aws_gui:

	def __init__(self, master):             
		self.master = master

	def implement(self, working_directory):
		print("\nPerforming AWS")

		os.chdir(working_directory)
		print(os.getcwd())

		width = self.master.winfo_width()
		height = self.master.winfo_height()

		title = placeView(self.master, Label, x=0, y=0, w=width, h=height*0.1)
		title["text"] = "Terraform Infrastructure Generator:   AWS"
		title["font"] = "Helvetica 25 bold"
		title["bg"] = "#6f24e8"
		title["fg"] = "white"

		accessKey_label = placeView(self.master, Label, x=width*0.05, y=height*0.125, w=width*0.35, h=height*0.05)
		accessKey_label["anchor"] = 'w'
		accessKey_label["justify"] = 'left'
		accessKey_label["font"] = "fixedsys 18 bold"
		accessKey_label["fg"] = "black"
		accessKey_label["text"] = "Access Key:   (required)"
		self.accessKey = StringVar()
		accessKey_field = placeView(self.master, Entry, x=width*0.05, y=height*0.175, w=width*0.4, h=height*0.05)
		accessKey_field["textvariable"] = self.accessKey
		accessKey_field["borderwidth"] = 0
		accessKey_field["bg"] = "#dddddd"

		secretKey_label = placeView(self.master, Label, x=width*0.55, y=height*0.125, w=width*0.35, h=height*0.05)
		secretKey_label["anchor"] = 'w'
		secretKey_label["justify"] = 'left'
		secretKey_label["font"] = "fixedsys 18 bold"
		secretKey_label["fg"] = "black"
		secretKey_label["text"] = "Secret Key:   (required)"
		self.secretKey = StringVar()
		secretKey_field = placeView(self.master, Entry, x=width*0.55, y=height*0.175, w=width*0.4, h=height*0.05)
		secretKey_field["textvariable"] = self.secretKey
		secretKey_field["borderwidth"] = 0
		secretKey_field["bg"] = "#dddddd"

		regionLabel = placeView(self.master, Label, x=width*0.05, y=height*0.275, w=width*0.275, h=height*0.05)
		regionLabel["anchor"] = 'w'
		regionLabel["justify"] = 'left'
		regionLabel["font"] = "fixedsys 18 bold"
		regionLabel["fg"] = "black"
		regionLabel["text"] = "Selected Region   (required):"
		regionFrame = createFrame(self.master, x=width*0.35, y=height*0.275, w=width*0.175, h=height*0.05)
		regions = [ "us-east-1", "us-east-2", 
					"us-west-1", "us-west-2", 
					"ap-northeast-1", "ap-northeast-2",
					"ap-southeast-1", "ap-southeast-2",
					"ap-south-1", "ca-central-1",
					"eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "sa-east-1"]
		self.selectedRegion = StringVar(regionFrame); self.selectedRegion.set(regions[0])
		regionMenu = OptionMenu(regionFrame, self.selectedRegion, *regions)
		regionMenu.pack(fill=BOTH, expand=1)

		resources = placeView(self.master, Label, x=width*0.05, y=height*0.35, w=width*0.25, h=height*0.05)
		resources["anchor"] = 'w'
		resources["justify"] = 'left'
		resources["font"] = "fixedsys 18 bold"
		resources["fg"] = "black"
		resources["text"] = "List of Resources:"

		self.canvasFrame = createFrame(self.master, x=width*0.05, y=height*0.425, w=width*0.425, h=height*0.35)
		self.canvas = Canvas(self.canvasFrame)
		scrollBar = Scrollbar(self.canvasFrame, orient="vertical",command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=scrollBar.set)
		scrollBar.pack(side="right",fill="y")
		self.canvas.pack(side="left")
		resourceFrame = Frame(self.canvas)
		self.canvas.create_window((0,0), width=width*0.425, height=height*0.35, window=resourceFrame, anchor='nw')
		resourceFrame["bg"] = "#eeeeee"
		self.canvas.configure(scrollregion=(0, 0, width*0.425, height*0.35), width=width*0.45, height=height*0.35)

		self.resourceButtonList = []
		self.resourceDict = {}
		self.createResourceMode()

		applyButtonFrame = createFrame(self.master, x=width*0.75, y=height*0.85, w=width*0.2, h=height*0.1)
		self.applyButton = Button(applyButtonFrame, text="Apply")
		self.applyButton["command"] = lambda: None
		self.applyButton["fg"] = "#999999"
		self.applyButton["font"] = "fixedsys 20 bold"
		self.applyButton.pack(fill=BOTH, expand=1)

		planButtonFrame = createFrame(self.master, x=width*0.05, y=height*0.85, w=width*0.2, h=height*0.1)
		self.planButton = Button(planButtonFrame, command=self.plan , text="Plan")
		self.planButton["font"] = "fixedsys 20 bold"
		self.planButton.pack(fill=BOTH, expand=1)

	def plan(self):
		tf.createProvider(self.selectedRegion.get())
		tf.storeKeys(self.accessKey.get(), self.secretKey.get())
		tf.init()
		tf.plan()
		if tf.checkValidPlan():
			self.applyButton["command"] = self.apply
			self.applyButton["fg"] = "#000000"
		else:
			self.applyButton["command"] = lambda: None
			self.applyButton["fg"] = "#999999"
		print("# Planning complete")

	def apply(self):
		MsgBox = messagebox.askquestion('Apply the current infrastructure plan', 'Are you sure?')
		if MsgBox == "yes":
			tf.apply()

	def createResourceMode(self):
		width = self.master.winfo_width()
		height = self.master.winfo_height()

		self.createNewResourceLabel = placeView(self.master, Label, x=width*0.525, y=height*0.35, w=width*0.15, h=height*0.05)
		self.createNewResourceLabel["anchor"] = 'w'
		self.createNewResourceLabel["justify"] = 'left'
		self.createNewResourceLabel["font"] = "fixedsys 18 bold"
		self.createNewResourceLabel["fg"] = "black"
		self.createNewResourceLabel["text"] = "Create Resource:"

		self.newResourceLabel = placeView(self.master, Label, x=width*0.7, y=height*0.325, w=width*0.2, h=height*0.025)
		self.newResourceLabel["anchor"] = 'sw'
		self.newResourceLabel["justify"] = 'left'
		self.newResourceLabel["font"] = "fixedsys 12 italic"
		self.newResourceLabel["fg"] = "#4e4e4e"
		self.newResourceLabel["text"] = "  New Resource Name"
		self.newResourceName = StringVar()
		self.newResourceEntry = placeView(self.master, Entry, x=width*0.7, y=height*0.35, w=width*0.25, h=height*0.05)
		self.newResourceEntry["textvariable"] = self.newResourceName
		self.newResourceEntry["borderwidth"] = 0
		self.newResourceEntry["bg"] = "#dddddd"

		self.amiLabel = placeView(self.master, Label, x=width*0.525, y=height*0.4125, w=width*0.2, h=height*0.025)
		self.amiLabel["anchor"] = 'sw'
		self.amiLabel["justify"] = 'left'
		self.amiLabel["font"] = "fixedsys 12 italic"
		self.amiLabel["fg"] = "#4e4e4e"
		self.amiLabel["text"] = "  AMI"
		self.ami = StringVar()
		self.amiEntry = placeView(self.master, Entry, x=width*0.525, y=height*0.4375, w=width*0.2, h=height*0.05)
		self.amiEntry["textvariable"] = self.ami
		self.amiEntry["borderwidth"] = 0
		self.amiEntry["bg"] = "#dddddd"

		self.instanceLabel = placeView(self.master, Label, x=width*0.75, y=height*0.4125, w=width*0.2, h=height*0.025)
		self.instanceLabel["anchor"] = 'sw'
		self.instanceLabel["justify"] = 'left'
		self.instanceLabel["font"] = "fixedsys 12 italic"
		self.instanceLabel["fg"] = "#4e4e4e"
		self.instanceLabel["text"] = "  Instance Type"
		self.instanceType = StringVar()
		self.instanceTypeEntry = placeView(self.master, Entry, x=width*0.75, y=height*0.4375, w=width*0.2, h=height*0.05)
		self.instanceTypeEntry["textvariable"] = self.instanceType
		self.instanceTypeEntry["borderwidth"] = 0
		self.instanceTypeEntry["bg"] = "#dddddd"

		self.tags = placeView(self.master, Label, x=width*0.525, y=height*0.5125, w=width*0.05, h=height*0.05)
		self.tags["anchor"] = 'w'
		self.tags["justify"] = 'left'
		self.tags["font"] = "fixedsys 15 italic"
		self.tags["fg"] = "#4e4e4e"
		self.tags["text"] = "Tags:"

		self.tagNameLabel = placeView(self.master, Label, x=width*0.5875, y=height*0.4875, w=width*0.15, h=height*0.025)
		self.tagNameLabel["anchor"] = 'sw'
		self.tagNameLabel["justify"] = 'left'
		self.tagNameLabel["font"] = "fixedsys 12 italic"
		self.tagNameLabel["fg"] = "#4e4e4e"
		self.tagNameLabel["text"] = "  Tag Name"
		self.tagName = StringVar()
		self.tagNameEntry = placeView(self.master, Entry, x=width*0.5875, y=height*0.5125, w=width*0.15, h=height*0.05)
		self.tagNameEntry["textvariable"] = self.tagName
		self.tagNameEntry["borderwidth"] = 0
		self.tagNameEntry["bg"] = "#dddddd"

		self.tagValueLabel = placeView(self.master, Label, x=width*0.75, y=height*0.4875, w=width*0.15, h=height*0.025)
		self.tagValueLabel["anchor"] = 'sw'
		self.tagValueLabel["justify"] = 'left'
		self.tagValueLabel["font"] = "fixedsys 12 italic"
		self.tagValueLabel["fg"] = "#4e4e4e"
		self.tagValueLabel["text"] = "  Tag Value"
		self.tagValue = StringVar()
		self.tagValueEntry = placeView(self.master, Entry, x=width*0.75, y=height*0.5125, w=width*0.15, h=height*0.05)
		self.tagValueEntry["textvariable"] = self.tagValue
		self.tagValueEntry["borderwidth"] = 0
		self.tagValueEntry["bg"] = "#dddddd"

		addTagButtonFrame = createFrame(self.master, x=width*0.92, y=height*0.5125, w=width*0.03, h=height*0.05)
		self.addTagButton = Button(addTagButtonFrame, text="+")
		self.addTagButton["command"] = self.addTag
		self.addTagButton["font"] = "fixedsys 15"
		self.addTagButton.pack(fill=BOTH, expand=1)

		self.tagsCanvasFrame = createFrame(self.master, x=width*0.525, y=height*0.575, w=width*0.425, h=height*0.15)
		self.tagsCanvas = Canvas(self.tagsCanvasFrame)
		scrollBar = Scrollbar(self.tagsCanvasFrame, orient="vertical",command=self.tagsCanvas.yview)
		self.tagsCanvas.configure(yscrollcommand=scrollBar.set)
		scrollBar.pack(side="right",fill="y")
		self.tagsCanvas.pack(side="left")
		tagsFrame = Frame(self.tagsCanvas)
		self.tagsCanvas.create_window((0,0), width=width*0.525, height=height*0.575, window=tagsFrame, anchor='nw')
		tagsFrame["bg"] = "#eeeeee"
		self.tagsCanvas.configure(scrollregion=(0, 0, width*0.525, height*0.575), width=width*0.425, height=height*0.15)

		self.tagsList = []
		self.tagsDict = {}

		clearResourceButtonFrame = createFrame(self.master, x=width*0.525, y=height*0.75, w=width*0.15, h=height*0.05)
		self.clearResourceButton = Button(clearResourceButtonFrame, text="Clear")
		self.clearResourceButton["command"] = self.clearNewResource
		self.clearResourceButton["font"] = "fixedsys 15"
		self.clearResourceButton.pack(fill=BOTH, expand=1)

		addResourceButtonFrame = createFrame(self.master, x=width*0.7, y=height*0.75, w=width*0.25, h=height*0.05)
		self.addResourceButton = Button(addResourceButtonFrame, text="Add Resource")
		self.addResourceButton["command"] = lambda: print("hi")
		self.addResourceButton["font"] = "fixedsys 15 bold"
		self.addResourceButton.pack(fill=BOTH, expand=1)
		self.addResourceButton["command"] = self.addResource

	def addTag(self):
		if self.tagName.get() == "" or self.tagValue.get() == "":
			return
		elif self.tagName.get() in self.tagsDict:
			MsgBox = messagebox.showerror('Error', 'There is already a tag with this name')
			return

		print("Adding Tag:   @ " + self.tagName.get() + "  ~  " + self.tagValue.get())

		width = self.master.winfo_width()
		height = self.master.winfo_height()

		scrollHeight = height*0.05*(len(self.tagsList) + 1)
		if scrollHeight > height*0.2:
			self.tagsCanvas.configure(scrollregion=(0, 0, width*0.425, scrollHeight), height=scrollHeight)

		tag = Button(self.tagsCanvasFrame)
		tag["bd"] = 3
		tag["relief"] = "ridge"
		tag["bg"] = "#dddddd"
		tag["text"] = self.tagName.get() + "  ~  " + self.tagValue.get()
		scrollRegion = (0, height*0.05*len(self.tagsList))
		self.tagsCanvas.create_window(scrollRegion, width=width*0.4125, height=height*0.05, window=tag, anchor='nw')

		self.tagsList.append((self.tagName.get(), tag))
		self.tagName.set("")
		self.tagValue.set("")


	def addResource(self):
		if self.newResourceName.get() == "":
			return
		elif self.newResourceName.get() in self.resourceDict:
			MsgBox = messagebox.showerror('Error', 'There is already a resource with this name')
			return

		print("Adding Resource:   + " + self.newResourceName.get())

		width = self.master.winfo_width()
		height = self.master.winfo_height()

		scrollHeight = height*0.05*(len(self.resourceButtonList) + 1)
		if scrollHeight > height*0.2:
			self.canvas.configure(scrollregion=(0, 0, width*0.425, scrollHeight), height=scrollHeight)

		res = Button(self.canvasFrame)
		res["bd"] = 3
		res["relief"] = "ridge"
		res["bg"] = "#dddddd"
		res["text"] = self.newResourceName.get()
		scrollRegion = (0, height*0.05*len(self.resourceButtonList))
		self.canvas.create_window(scrollRegion, width=width*0.4125, height=height*0.05, window=res, anchor='nw')
		self.resourceButtonList.append((res["text"], res))

		resource = Resource(self.newResourceName.get())
		resource.ami = self.ami.get()
		resource.instanceType = self.instanceType.get()
		resource.tags = self.tagsDict
		self.resourceDict[res["text"]] = resource
		res["command"] = lambda: self.showResource(res["text"])
		self.clearNewResource()

	def clearNewResource(self):
		self.newResourceName.set("")
		self.ami.set("")
		self.tagName.set("")
		self.tagValue.set("")
		self.instanceType.set("")

		for tagName, tagButton in self.tagsList:
			tagButton.destroy()

		self.tagsList.clear()
		self.tagsDict.clear()


	def showResource(self, name):
		pass

	def applyResource(self, name):
		pass












