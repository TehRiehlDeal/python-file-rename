import os
import sys
import re
from tkinter import *
import tkinter.filedialog

regex = re.compile(r'S\d*E\d*', re.IGNORECASE)
dir_path = os.path.dirname(os.path.realpath(__file__))
favicon = os.path.join(dir_path, "favicon.ico")
folder = ""
clickCount = 0
class App:
	def __init__(self,master):

		def getFiles():
			global folder
			folder = tkinter.filedialog.askdirectory(parent=root, initialdir="./", title="Please Select a Directory")
			if (folder == ""):
				self.folderSelected.delete(0, END)
				self.folderSelected.insert(0, "No folder selected, try again.")
				delRename()
			else:
				addRename()                        
				self.folderSelected.delete(0, END)
				self.folderSelected.insert(0,folder)


		def renameFiles(show, season):
			count = 1
			for file in os.listdir(folder):
				extension = "." + file.split(".")[len(file.split("."))-1]
				if (count < 10):
					episode = show + " S0" +str(season) + "E0" + str(count) + extension
				else:
					episode = show + " S0" +str(season) + "E" + str(count) + extension

				os.rename(os.path.join(folder, file), os.path.join(folder, episode))

				count+=1


			self.folderSelected.delete(0, END)
			self.show.delete(0, END)
			self.season.delete(0, END)
			delRename()

		def addRename():
			self.rename.config(command=lambda:renameFiles(self.show.get(), self.season.get()), state=ACTIVE, relief=RAISED)

		def delRename():
			self.rename.config(state=DISABLED, relief=SUNKEN)

		self.input = Label(master, text="Show Name:")
		self.input.grid(row=0)
		self.show = Entry(master, width="50")
		self.show.grid(row=0,column=1)

		self.seasonInput = Label(master, text="Season Number:")
		self.seasonInput.grid(row=1)
		self.season = Entry(master, width="50")
		self.season.grid(row=1,column=1)

		self.selectedFolder = Label(master, text="Selected Folder:")
		self.selectedFolder.grid(row=2)
		self.folderSelected = Entry(master, width="50")
		self.folderSelected.grid(row=2,column=1)

		self.openFiles = Button(master, text="Select Folder", command=getFiles)
		self.openFiles.grid(row=3)
		self.quit = Button(master, text="Quit", command=root.destroy)
		self.quit.grid(row=3,column=1)

		self.rename = Button(master, text="Rename Files", state=DISABLED, relief=SUNKEN)
		self.rename.grid(row=0, column=3, columnspan=2, rowspan=4, sticky='WENS')

root = Tk()
root.geometry("477x89")
root.iconbitmap(favicon)
root.title("Rename Show")
app = App(root)

root.mainloop()
