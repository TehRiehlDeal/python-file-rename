import os
import sys
import re
from tkinter import filedialog, END, ACTIVE, RAISED, DISABLED, SUNKEN, Label, Entry, Button, Tk, Text, NORMAL, font
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

		def getFolder(event):
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
				extension = "." + file.split(".")[len(file.split("."))-1].lower()
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

					self.output.configure(state=NORMAL)
					self.output.insert('end', 'Renaming: ' + file + " --> " + episode + "\n")
					self.output.configure(state=DISABLED)
					self.output.see('end')
					self.output.update_idletasks()
					print("Renaming: " + file)
					os.rename(os.path.join(folder, file), os.path.join(folder, episode))

					count+=1
			self.output.configure(state=NORMAL)
			self.output.insert('end', "Renaming Complete.\n")
			self.output.configure(state=DISABLED)
			self.output.see("end")
			self.output.update_idletasks()
					
			self.folderSelected.delete(0, END)
			delRename()

		def addRename():
			""" Adds the button used to rename the files in a folder. """
			self.rename.config(command=lambda:renameFiles(self.show.get(), self.season.get()), state=ACTIVE, relief=RAISED)

		def delRename():
			""" Deletes the rename button when no folder is selected. """
			self.rename.config(state=DISABLED, relief=SUNKEN)

		self.input = Label(master, text="Show Name:")
		self.input.place(x=200, y=0)
		self.show = Entry(master)
		self.show.bind("<KeyRelease>", searchShow)
		self.show.place(x=273, y=0, width=477, height=22)

		self.seasonInput = Label(master, text="Season Number:")
		self.seasonInput.place(x=180, y=23)
		self.season = Entry(master, width="50")
		self.season.place(x=273, y=23, width=477, height=22)
		
		self.selectedFolder = Label(master, text="Selected Folder:")
		self.selectedFolder.place(x=184, y=46)
		self.folderSelected = Entry(master, width="50")
		self.folderSelected.insert(0, "Click here to select folder.")
		self.folderSelected.bind("<Button-1>", getFolder)
		self.folderSelected.place(x=273, y=46, width=477, height=22)

		self.rename = Button(master, text="Rename Files", state=DISABLED, relief=SUNKEN)
		self.rename.place(x=750, y=0, width=80, height=69)

		"""
		self.quit = Button(master, text="Quit", command=root.destroy)
		self.quit.grid(row=3,column=1)
		"""

		self.Font = font.Font(size=8)

		self.output = Text(master, state=DISABLED)
		self.output['font'] = self.Font
		self.output.place(x=0, y=70, width=1024, height=219)

root = Tk()
root.geometry("1024x289") #477x89
root.resizable(False, False)
root.iconbitmap(favicon)
root.title("Rename Show")
app = App(root)

root.mainloop()
