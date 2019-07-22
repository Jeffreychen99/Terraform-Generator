from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import util.tf_util as tf_util
import util.web_util as web_util
from util.gui_util import *
from util.web_util import *

from tf_generation.terra import *
from tf_generation.terraResource import *
from tf_generation.terraDatasource import *

class Resource_GUI:

	terra = None
	tf = None

	def __init__(self, master, terra, provider_util):             
		self.master = master
		self.master.title("Terraform Generator")

		self.terra = terra
		self.tf = provider_util

		self.createPlanApplyButtons()
		self.resourceCreation()

	def createPlanApplyButtons(self):
		width = self.master.winfo_width()
		height = self.master.winfo_height()

		title = placeView(self.master, Label, x=0, y=0, w=width, h=height*0.1)
		title["text"] = "Terraform Infrastructure Generator:   " + self.terra.provider.upper()
		title["font"] = "Helvetica 25 bold"
		title["bg"] = "#5C4EE5"
		title["fg"] = "white"

		planButtonFrame = createFrame(self.master, x=width*0.05, y=height*0.85, w=width*0.2, h=height*0.1)
		self.planButton = Button(planButtonFrame, command=self.plan , text="Plan")
		self.planButton["font"] = "fixedsys 20 bold"
		self.planButton.pack(fill=BOTH, expand=1)

		applyButtonFrame = createFrame(self.master, x=width*0.75, y=height*0.85, w=width*0.2, h=height*0.1)
		self.applyButton = Button(applyButtonFrame, text="Apply")
		self.applyButton["command"] = lambda: None
		self.applyButton["fg"] = "#999999"
		self.applyButton["font"] = "fixedsys 20 bold"
		self.applyButton.pack(fill=BOTH, expand=1)


	def resourceCreation(self):
		width = self.master.winfo_width()
		height = self.master.winfo_height()

		resources = placeView(self.master, Label, x=width*0.05, y=height*0.125, w=width*0.25, h=height*0.05)
		resources["anchor"] = 'w'
		resources["justify"] = 'left'
		resources["font"] = "fixedsys 18 bold"
		resources["fg"] = "black"
		resources["text"] = "List of Resources:"

		self.canvasFrame = createFrame(self.master, x=width*0.05, y=height*0.2, w=width*0.425, h=height*0.35)
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

		self.createNewResourceLabel = placeView(self.master, Label, x=width*0.525, y=height*0.125, w=width*0.15, h=height*0.05)
		self.createNewResourceLabel["anchor"] = 'w'
		self.createNewResourceLabel["justify"] = 'left'
		self.createNewResourceLabel["font"] = "fixedsys 18 bold"
		self.createNewResourceLabel["fg"] = "black"
		self.createNewResourceLabel["text"] = "Create Resource:"

		self.resourceType = placeView(self.master, Label, x=width*0.525, y=height*0.175, w=width*0.15, h=height*0.025)
		self.resourceType["anchor"] = 'sw'
		self.resourceType["justify"] = 'left'
		self.resourceType["font"] = "fixedsys 12 italic"
		self.resourceType["fg"] = "#4e4e4e"
		self.resourceType["text"] = "  Resource Type"
		self.resourceTypeFrame = createFrame(self.master, x=width*0.525, y=height*0.2, w=width*0.175, h=height*0.05)
		resourceTypeOptions = web_util.getResourceList(self.terra.provider)
		self.selectedResourceType = StringVar(self.resourceTypeFrame); self.selectedResourceType.set(resourceTypeOptions[0])
		self.resourceTypeMenu = OptionMenu(self.resourceTypeFrame, self.selectedResourceType, *resourceTypeOptions)
		self.resourceTypeMenu.pack(fill=BOTH, expand=1)

		self.newResourceLabel = placeView(self.master, Label, x=width*0.725, y=height*0.175, w=width*0.175, h=height*0.025)
		self.newResourceLabel["anchor"] = 'sw'
		self.newResourceLabel["justify"] = 'left'
		self.newResourceLabel["font"] = "fixedsys 12 italic"
		self.newResourceLabel["fg"] = "#4e4e4e"
		self.newResourceLabel["text"] = "  New Resource Name"
		self.newResourceName = StringVar()
		self.newResourceEntry = placeView(self.master, Entry, x=width*0.725, y=height*0.2 , w=width*0.225, h=height*0.05)
		self.newResourceEntry["textvariable"] = self.newResourceName
		self.newResourceEntry["borderwidth"] = 0
		self.newResourceEntry["bg"] = "#dddddd"

		self.argsCanvasFrame = createFrame(self.master, x=width*0.525, y=height*0.275, w=width*0.425, h=height*0.2)
		self.argsCanvas = Canvas(self.argsCanvasFrame)
		scrollBar = Scrollbar(self.argsCanvasFrame, orient="vertical",command=self.argsCanvas.yview)
		self.argsCanvas.configure(yscrollcommand=scrollBar.set)
		scrollBar.pack(side="right",fill="y")
		self.argsCanvas.pack(side="left")
		argsFrame = Frame(self.argsCanvas)
		self.argsCanvas.create_window((0,0), width=width*0.525, height=height*0.2, window=argsFrame, anchor='nw')
		argsFrame["bg"] = "#eeeeee"
		self.argsCanvas.configure(scrollregion=(0, 0, width*0.525, height*0.2), width=width*0.425, height=height*0.2)

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
		self.tagsCanvas.create_window((0,0), width=width*0.525, height=height*0.15, window=tagsFrame, anchor='nw')
		tagsFrame["bg"] = "#eeeeee"
		self.tagsCanvas.configure(scrollregion=(0, 0, width*0.525, height*0.15), width=width*0.425, height=height*0.15)

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

		width = self.master.winfo_width()
		height = self.master.winfo_height()

		scrollHeight = height*0.05*(len(self.tagsList) + 1)
		if scrollHeight > height*0.15:
			self.tagsCanvas.configure(scrollregion=(0, 0, width*0.425, scrollHeight), height=scrollHeight)

		tag = Button(self.tagsCanvasFrame)
		tag["bd"] = 3
		tag["relief"] = "ridge"
		tag["bg"] = "#dddddd"
		tag["text"] = self.tagName.get() + "  ~  " + self.tagValue.get()
		scrollRegion = (0, height*0.05*len(self.tagsList))
		self.tagsCanvas.create_window(scrollRegion, width=width*0.4125, height=height*0.05, window=tag, anchor='nw')

		self.tagsList.append((self.tagName.get(), tag))
		self.tagsDict[self.tagName.get()] = self.tagValue.get()
		print("Adding Tag:   @ " + self.tagName.get() + "  ~  " + self.tagValue.get())
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

		resTypeFull = self.terra.provider + "_" + self.selectedResourceType.get()
		resource = Resource(self.newResourceName.get(), resTypeFull, {})
		resource.tags = self.tagsDict
		self.terra.resources.append(resource)

		self.resourceDict[res["text"]] = resource
		res["command"] = lambda: self.showResource(res["text"])
		self.clearNewResource()

	def clearNewResource(self):
		self.newResourceName.set("")
		self.tagName.set("")
		self.tagValue.set("")

		for tagName, tagButton in self.tagsList:
			tagButton.destroy()

		self.tagsList.clear()
		self.tagsDict.clear()

	def plan(self):
		tf_util.writeProvider(self.terra)
		tf_util.writeResources(self.terra)
		tf_util.writeDatasources(self.terra)

		self.tf.init()
		self.tf.plan()

		if self.tf.checkValidPlan():
			self.applyButton["command"] = self.apply
			self.applyButton["fg"] = "#000000"
		else:
			self.applyButton["command"] = lambda: None
			self.applyButton["fg"] = "#999999"
		print("# Planning complete")

	def apply(self):
		MsgBox = messagebox.askquestion('Apply the current infrastructure plan', 'Are you sure?')
		if MsgBox == "yes":
			self.tf.apply()













