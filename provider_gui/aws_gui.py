from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import os

from util.tf_util import *
from util.gui_util import *

import util.provider_utils.aws_tf as tf
from tf_generation.terra import *

from resource_gui import Resource_GUI

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

		submitButtonFrame = createFrame(self.master, x=width*0.4, y=height*0.8, w=width*0.2, h=height*0.1)
		def submit(): 
			if self.selectedRegion.get() != "" and self.secretKey.get() != "" and self.accessKey.get() != "":
				tf.storeKeys(self.accessKey.get(), self.secretKey.get())

				arguments = {	"region":self.selectedRegion.get(),
							 	"access_key":tf_variable("access_key"), 
							 	"secret_key":tf_variable("secret_key")
							}
				parameters = ["access_key", "secret_key"]
				terra = Terra("aws", arguments, parameters)

				clearScreen(self)
				resData = Resource_GUI(self.master, terra, tf)
			else:
				MsgBox = messagebox.showerror('Error', 'Please fill out all required fields')
				return

		submitButton = Button(submitButtonFrame, command=submit, text="Continue")
		submitButton["fg"] = "black"
		submitButton["font"] = "fixedsys 15 bold"
		submitButton.pack(fill=BOTH, expand=1)












