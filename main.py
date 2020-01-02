import os
import sys
import re
from tkinter import filedialog, END, ACTIVE, RAISED, DISABLED, SUNKEN, Label, Entry, Button, Tk
from tvdbAPI import TVDB

regex = re.compile(r'S\d*E\d*', re.IGNORECASE)
dir_path = os.path.dirname(os.path.realpath(__file__))
t = TVDB()
favicon = os.path.join(dir_path, "favicon.ico")
folder = ""
clickCount = 0
validExtensions = ['.mp4', '.mkv', '.avi', '.m4v', '.mov', '.ts', '.m2ts']
class App:
	def __init__(self,master):

		def getFolder():
			""" Opens a folder select window for user to select the folder in which the show is located, and sets
				the global variable 'folder' to that folder. Also adds or removes the rename button accordingly. """
			global folder
			if (folder == ""):
				folder = filedialog.askdirectory(parent=root, initialdir="./", title="Please Select a Directory")
			else:
				folder = filedialog.askdirectory(parent=root, initialdir=folder, title="Please Select a Directory")
			if (folder == ""):
				self.folderSelected.delete(0, END)
				self.folderSelected.insert(0, "No folder selected, try again.")
				delRename()
			else:
				addRename()                        
				self.folderSelected.delete(0, END)
				self.folderSelected.insert(0,folder)
			
		def searchShow(event):
			""" WIP to be used for live searching of show """
			print (self.show.get())

		def renameFiles(show, season):
			""" Takes in the given show title and season number and renames all files within the folder. """
			count = 1
			for file in os.listdir(folder):
				extension = "." + file.split(".")[len(file.split("."))-1]
				if (extension in validExtensions):
					episodeName = t.getEpisodeName(show, int(season), count)
					if (count < 10):
						if (int(season) >= 10):
							episode = show + " S" + str(season) + "E0" + str(count) + \
														" " + \
														episodeName + \
														extension
						else:
							episode = show + " S0" + \
														str(season) + "E0" + str(count) + " " + \
														episodeName + \
														extension
					else:
						if (int(season) >= 10):
							episode = show + " S" + \
														str(season) + "E" + str(count) + " " + \
														episodeName + \
														extension
						else:
							episode = show + " S0" + \
														str(season) + "E" + str(count) + " " + \
														episodeName + \
														extension

					os.rename(os.path.join(folder, file), os.path.join(folder, episode))

					count+=1
					
			self.folderSelected.delete(0, END)
			delRename()

		def addRename():
			""" Adds the button used to rename the files in a folder. """
			self.rename.config(command=lambda:renameFiles(self.show.get(), self.season.get()), state=ACTIVE, relief=RAISED)

		def delRename():
			""" Deletes the rename button when no folder is selected. """
			self.rename.config(state=DISABLED, relief=SUNKEN)

		self.input = Label(master, text="Show Name:")
		self.input.grid(row=0)
		self.show = Entry(master, width="50")
		self.show.bind("<Key>", searchShow)
		self.show.grid(row=0,column=1)

		self.seasonInput = Label(master, text="Season Number:")
		self.seasonInput.grid(row=1)
		self.season = Entry(master, width="50")
		self.season.grid(row=1,column=1)

		self.selectedFolder = Label(master, text="Selected Folder:")
		self.selectedFolder.grid(row=2)
		self.folderSelected = Entry(master, width="50")
		self.folderSelected.grid(row=2,column=1)

		self.openFiles = Button(master, text="Select Folder", command=getFolder)
		self.openFiles.grid(row=3)
		self.quit = Button(master, text="Quit", command=root.destroy)
		self.quit.grid(row=3,column=1)

		self.rename = Button(master, text="Rename Files", state=DISABLED, relief=SUNKEN)
		self.rename.grid(row=0, column=3, columnspan=2, rowspan=4, sticky='WENS')

root = Tk()
root.geometry("477x89")
root.resizable(False, False)
root.iconbitmap(favicon)
root.title("Rename Show")
app = App(root)

root.mainloop()
