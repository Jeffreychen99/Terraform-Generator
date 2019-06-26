from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import getpass
import os

from provider_gui.aws_gui import aws_gui
from provider_gui.digitalocean_gui import digitalocean_gui

from util.tf_util import *
from util.gui_util import *

class gui:
	def __init__(self, master):             
		self.master = master
		self.master.title("Terraform Generator")
		self.menuScreen()

	def clearScreen(self):
		for child in self.master.winfo_children():
			child.destroy()
		self.master.update_idletasks()

	def menuScreen(self):
		self.clearScreen()
		width = self.master.winfo_width()
		height = self.master.winfo_height()

		title = placeView(self.master, Label, x=0, y=0, w=width, h=height*0.1)
		title["text"] = "Terraform Infrastructure Generator"
		title["font"] = "Helvetica 25 bold"
		title["bg"] = "#6f24e8"
		title["fg"] = "white"

		introText = placeView(self.master, Label, x=width*0.05, y=height*0.1125, w=width*0.9, h=height*0.15)
		introText["anchor"] = 'w'
		introText["justify"] = 'left'
		introText["font"] = "fixedsys 15"
		introText["fg"] = "#4e4e4e"
		introText["text"] = "Welcome to the Terraform infrastructure generator. \n\n" \
						  + "This is a python based GUI program to help create infrastructure to run on service providers.\n" \
						  + "Based on user selection, Terraform code will be generated to support your servers' needs."

		step1 = placeView(self.master, Label, x=width*0.05, y=height*0.3125, w=width*0.6, h=height*0.05)
		step1["anchor"] = 'w'
		step1["justify"] = 'left'
		step1["font"] = "fixedsys 18 bold"
		step1["fg"] = "black"
		step1["text"] = "Step #1:     Select your provider"
		optionFrame = createFrame(self.master, x=width*0.05, y=height*0.375, w=width*0.4, h=height*0.05)
		options = ["AWS", "Digital Ocean"]
		selectedOption = StringVar(optionFrame); selectedOption.set(options[0])
		optionMenu = OptionMenu(optionFrame, selectedOption, *options)
		optionMenu.pack(fill=BOTH, expand=1)


		step2 = placeView(self.master, Label, x=width*0.05, y=height*0.5125, w=width*0.6, h=height*0.05)
		step2["anchor"] = 'w'
		step2["justify"] = 'left'
		step2["font"] = "fixedsys 18 bold"
		step2["fg"] = "black"
		step2["text"] = "Step #2:     Choose destination directory"
		directoryLabel = placeView(self.master, Label, x=width*0.05, y=height*0.575, w=width*0.4, h=height*0.025)
		directoryLabel["anchor"] = 'w'
		directoryLabel["justify"] = 'left'
		directoryLabel["font"] = "fixedsys 15 italic"
		directoryLabel["fg"] = "#4e4e4e"
		directoryLabel["text"] = "No directory selected"
		folderButtonFrame = createFrame(self.master, x=width*0.05, y=height*0.60625, w=width*0.3, h=height*0.075)
		chosen_directory = None
		def chooseDirectory(submitButton):
			chosen_directory = filedialog.askdirectory(initialdir="/Users/" + getpass.getuser())
			if chosen_directory:
				directoryLabel.configure(text=chosen_directory)
				submitButton["fg"] = "black"
		folderButton = Button(folderButtonFrame, command=lambda: chooseDirectory(submitButton), text="Choose directory")
		folderButton["font"] = "fixedsys 15 bold"
		folderButton.pack(fill=BOTH, expand=1)

		provider_functions = {	"AWS":aws_gui, 
								"Digital Ocean":digitalocean_gui
							 }

		submitButtonFrame = createFrame(self.master, x=width*0.4, y=height*0.8, w=width*0.2, h=height*0.1)
		def submit(directoryLabel): 
			directory = directoryLabel["text"]
			if directoryLabel["text"] != "No directory selected":
				provider_gui = provider_functions[selectedOption.get()](self.master)
				gui.clearScreen(provider_gui)
				provider_gui.implement(directory)
		submitButton = Button(submitButtonFrame, command=lambda: submit(directoryLabel), text="Continue")
		submitButton["fg"] = "#999999"
		submitButton["font"] = "fixedsys 15 bold"
		submitButton.pack(fill=BOTH, expand=1)


root = Tk()
root.geometry("1000x750")
root.resizable(False, False)

app = gui(root)
root.mainloop()















