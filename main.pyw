#!/usr/bin/python3
import os
import re
from tkinter import filedialog, END, ACTIVE, RAISED, DISABLED, SUNKEN, Label, Entry, Button, Tk, Text, NORMAL, font
from tmdbAPI import TMDB
from File import File
import webbrowser

regex = re.compile(r'S\d*E\d*', re.IGNORECASE)
multiEpRegex = re.compile(r'E\d*-E\d*', re.IGNORECASE)
dir_path = os.path.dirname(os.path.realpath(__file__))
t = TMDB()
favicon = os.path.join(dir_path, "favicon.ico")
folder = ""
clickCount = 0
validExtensions = ['.mp4', '.mkv', '.avi', '.m4v', '.mov', '.ts', '.m2ts', ".srt"]

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
			if (len(self.showID.get()) == 0):
				searchShow()

		def grabFiles(folder):
			count = 1
			self.files = []
			for file in os.listdir(folder):
				if (re.search(multiEpRegex, file) != None):
					match = re.search(multiEpRegex, file)
					episodes = match.group(0)
					episodes = episodes.replace("E", "")
					episodes = episodes.replace("e", "")
					episodes = episodes.split("-")
					numEp = int(episodes[1]) - int(episodes[0])
					self.files.append(File(count, folder, file, multiEpisode=True, numEp=numEp))
					count += 1
				else:
					self.files.append(File(count, folder, file))
					count += 1
			
		def searchShow():
			""" WIP to be used for live searching of show """
			shows = t.getShow(self.show.get())
			if (len(shows['results']) > 1):
				self.output.configure(state=NORMAL)
				self.output.insert('end', "Multiple shows detected, please find the one you searched for and enter the ID in the box above." + "\n")
				self.output.configure(state=DISABLED)
				self.output.see('end')
				self.output.update_idletasks()
				for show in shows['results']:
					self.output.configure(state=NORMAL)
					self.output.insert('end', "Show Title: " + show['name'] + " | Show ID: ")
					self.output.insert('end', str(show['id']), (str(show['id']), str(1)))
					self.output.insert('end', "\n")
					self.output.tag_config(str(show['id']), foreground="blue")
					self.output.tag_bind(str(show['id']), '<Button-1>', lambda event, url = "https://www.themoviedb.org/tv/" + str(show["id"]) + "-" + str(show['name']): openLink(url))
					self.output.configure(state=DISABLED)
					self.output.update_idletasks()
			elif (len(shows['results']) == 1):
				self.showID.insert('end', shows['results'][0]['id']) 


		def renameFiles(show, season):
			""" Takes in the given show title and season number and renames all files within the folder. """
			grabFiles(self.folderSelected.get())
			
			self.undo.config(command=undoRename, state=ACTIVE, relief=RAISED)
			count = 1
			skipEpisodes = self.skipEpisodes.get().split(",")
			for file in self.files:
				extension = "." + file.startName.split(".")[len(file.startName.split("."))-1].lower()
				episodeName = ""
				episodeNumber = ""
				for ep in skipEpisodes:
					if str(count) == ep:
						count += 1
				if (len(self.showID.get()) == 0):
					id = None
				else:
					id = self.showID.get()
				if (extension in validExtensions):
					if (file.numEp > 0):
						i = 0
						while i <= file.numEp:
							if (i == 0):
								episodeName = t.getEpisodeName(show, int(season), count, id=id)
								if len(self.files) >= 100:
									episodeNumber = "E{0:0=3d}".format(count)
								else:
									episodeNumber = "E{0:0=2d}".format(count)
							elif (i == file.numEp):
								episodeName = episodeName + " - " + t.getEpisodeName(show, int(season), count, id=id)
								if len(self.files) >= 100:
									episodeNumber = episodeNumber + "-" + "E{0:0=3d}".format(count)
								else:
									episodeNumber = episodeNumber + "-" + "E{0:0=2d}".format(count)
							else:
								episodeName = episodeName + " - " + t.getEpisodeName(show, int(season), count, id=id)								
							count += 1
							i += 1
					else:
						episodeName = t.getEpisodeName(show, int(season), count, id=id)
						if len(self.files) >= 100:
							episodeNumber = "E{0:0=3d}".format(count)
						else:
							episodeNumber = "E{0:0=2d}".format(count)
						count += 1

					episode = show + " S" + "{0:0=2d}".format(int(season)) + episodeNumber + f" {episodeName}{extension}"
					
					file.setEndName(episode)
					self.output.configure(state=NORMAL)
					self.output.insert('end', 'Renaming: ' + file.startName + " --> " + episode + "\n")
					self.output.configure(state=DISABLED)
					self.output.see('end')
					self.output.update_idletasks()
					os.rename(os.path.join(self.folderSelected.get(), file.startName), os.path.join(self.folderSelected.get(), episode))					

			self.output.configure(state=NORMAL)
			self.output.insert('end', "Renaming Complete.\n")
			self.output.configure(state=DISABLED)
			self.output.see("end")
			self.output.update_idletasks()
					
			self.selectFolder.config(relief=RAISED)

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

			self.undo.config(state=DISABLED, relief=SUNKEN)

		def openLink(url):
			webbrowser.open_new(url)

		self.input = Label(master, text="Show Name:")
		self.input.place(x=200, y=0)
		self.show = Entry(master)
		self.show.place(x=273, y=0, width=237, height=22)
		self.id = Label(master, text="Show ID:", fg="grey")
		self.id.place(x=512, y=0)
		self.showID = Entry(master)
		self.showID.place(x=562, y=0, width=188, height=22)

		self.skipEpisodeLabel = Label(master, text="Skip Missing Episodes:")
		self.skipEpisodeLabel.place(x=32, y=8)
		self.skipEpisodes = Entry(master)
		self.skipEpisodes.place(x=47, y=27, width=100, height=22)

		self.seasonInput = Label(master, text="Season Number:")
		self.seasonInput.place(x=180, y=23)
		self.season = Entry(master, width="50")
		self.season.place(x=273, y=23, width=477, height=22)
		
		self.selectedFolder = Label(master, text="Selected Folder:")
		self.selectedFolder.place(x=184, y=46)
		self.folderSelected = Entry(master, width="50")
		self.folderSelected.place(x=273, y=46, width=377, height=22)
		self.selectFolder = Button(master, text="Select Folder")
		self.selectFolder.place(x=650, y=47, width= 100, height=20)
		self.selectFolder.bind("<Button-1>", getFolder)

		self.rename = Button(master, text="Rename Files", state=DISABLED, relief=SUNKEN)
		self.rename.place(x=750, y=0, width=80, height=69)

		self.undo = Button(master, text="Undo Rename", state=DISABLED, relief=SUNKEN)
		self.undo.place(x=875, y=27)

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
