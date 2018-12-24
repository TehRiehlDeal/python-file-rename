import os
import sys
import re
from Tkinter import *
import tkFileDialog

regex = re.compile(r'S\d*E\d*', re.IGNORECASE)
folder = ""
clickCount = 0
class App:
	def __init__(self,master):

		def getFiles():
			global folder
			folder = tkFileDialog.askdirectory(parent=root, initialdir="./", title="Please Select a Directory")
			addRename()


		def renameFiles(show):
			for file in os.listdir(folder):
				extension = "." + file.split(".")[len(file.split("."))-1]
				matched = regex.findall(file)
				if matched:
					season = matched[0]
					season = season.upper()
					episodeName = show + " " + season + extension
					os.rename(os.path.join(folder, file), os.path.join(folder, episodeName))

		def addRename():
			self.rename = Button(master, text="Rename Files", command=lambda:renameFiles(self.show.get())).grid(row=2)
		self.input = Label(master, text="Show Name:")
		self.input.grid(row=0)
		self.show = Entry(master)
		self.show.grid(row=0,column=1)
		self.openFiles = Button(master, text="Select Folder", command=getFiles)
		self.openFiles.grid(row=1)
		self.quit = Button(master, text="Quit", command=root.destroy)
		self.quit.grid(row=1,column=1)

root = Tk()
root.title("Rename Show")
app = App(root)

root.mainloop()
