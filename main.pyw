import os
import sys
import re
from tkinter import filedialog, END, ACTIVE, RAISED, DISABLED, SUNKEN, Label, Entry, Button, Tk, Text, NORMAL, font, OptionMenu, StringVar
from tvdbAPI import TVDB
from File import File

regex = re.compile(r'S\d*E\d*', re.IGNORECASE)
dir_path = os.path.dirname(os.path.realpath(__file__))
t = TVDB()
favicon = os.path.join(dir_path, "favicon.ico")
folder = ""
clickCount = 0
validExtensions = ['.mp4', '.mkv', '.avi', '.m4v', '.mov', '.ts', '.m2ts', ".srt"]
optionList = ['AIRED', 'DVD']
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
				#grabFiles(folder)
				addRename()                        
				self.folderSelected.delete(0, END)
				self.folderSelected.insert(0,folder)
			if (len(self.showID.get()) == 0):
				searchShow()

		def grabFiles(folder):
			count = 1
			self.files = []
			for file in os.listdir(folder):
				
				self.files.append(File(count, folder, file))
				count += 1
			
		def searchShow():
			""" WIP to be used for live searching of show """
			shows = t.getShow(self.show.get())
			if (len(shows['data']) > 1):
				self.output.configure(state=NORMAL)
				self.output.insert('end', "Multiple shows detected, please find the one you searched for and enter the ID in the box above." + "\n")
				self.output.configure(state=DISABLED)
				self.output.see('end')
				self.output.update_idletasks()
			for show in shows['data']:
				self.output.configure(state=NORMAL)
				self.output.insert('end', "Show Title: " + show['seriesName'] + " | Show ID: " + str(show['id']) + "\n")
				self.output.configure(state=DISABLED)
				self.output.update_idletasks()


		def renameFiles(show, season):
			""" Takes in the given show title and season number and renames all files within the folder. """
			grabFiles(folder)
			for file in self.files:
				extension = "." + file.startName.split(".")[len(file.startName.split("."))-1].lower()
				if (len(self.showID.get()) == 0):
					id = None
				else:
					id = self.showID.get()
				if (extension in validExtensions):
					order = self.variable.get()
					if 'AIRED' in order:
						episodeName = t.getEpisodeName(show, int(season), file.id, order='AIRED', id=id)
					elif 'DVD' in order:
						episodeName = t.getEpisodeName(show, int(season), file.id, order='DVD', id=id)
					else:
						episodeName = t.getEpisodeName(show, int(season), file.id, id=id)

					episode = show + " S" + "{0:0=2d}".format(int(season)) + "E" + "{0:0=2d}".format(file.id) + f" {episodeName}{extension}"
					
					file.setEndName(episode)
					self.output.configure(state=NORMAL)
					self.output.insert('end', 'Renaming: ' + file.startName + " --> " + episode + "\n")
					self.output.configure(state=DISABLED)
					self.output.see('end')
					self.output.update_idletasks()
					os.rename(os.path.join(folder, file.startName), os.path.join(folder, episode))

			self.undo = Button(master, text="Undo Rename")
			self.undo.place(x=875, y=27)
			self.undo.config(command=undoRename)

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

		def undoRename():
			for file in self.files:
				self.output.configure(state=NORMAL)
				self.output.insert('end', 'Undoing Rename: ' +
				                   file.endName + " --> " + file.startName + "\n")
				self.output.configure(state=DISABLED)
				self.output.see('end')
				self.output.update_idletasks()
				os.rename(os.path.join(file.path, file.endName),
                                    os.path.join(file.path, file.startName))

			self.undo.destroy()			

		self.input = Label(master, text="Show Name:")
		self.input.place(x=200, y=0)
		self.show = Entry(master)
		#self.show.bind("<KeyRelease>", searchShow)
		self.show.place(x=273, y=0, width=237, height=22)
		self.id = Label(master, text="Show ID:", fg="grey")
		self.id.place(x=512, y=0)
		self.showID = Entry(master)
		self.showID.place(x=562, y=0, width=188, height=22)

		self.variable = StringVar(master)
		self.variable.set(optionList[0])
		self.orderLabel = Label(master, text="Order Type:")
		self.orderLabel.place(x=47, y=8)
		self.order = OptionMenu(master, self.variable, *optionList)
		self.order.place(x=47, y=27, width=100, height=22)

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
