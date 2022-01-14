#!/usr/bin/python3
import os
import re
from tkinter import filedialog, END, ACTIVE, RAISED, DISABLED, SUNKEN, Label, Entry, Button, Tk, Text, NORMAL, font, StringVar, OptionMenu
try:
	from tmdbAPI import TMDB, ShowNotFound, NoSuchEpisode, InvalidShowID, InvalidInput, InvalidCredentials
	tmdbImported = True
except ImportError:
	tmdbImported = False
	raise ImportError("Unable to import tmdbAPI, please make sure it is installed globally with pip3")
try:
	from tvdbAPI import TVDB, ShowNotFound, NoSuchEpisode, InvalidShowID, InvalidInput, InvalidCredentials
	tvdbImported = True
except ImportError:
	tvdbImported = False
	raise ImportError("Unable to import tvdbAPI, please make sure it is installed globally with pip3")	
from File import File
import webbrowser

regex = re.compile(r'S\d*E\d*', re.IGNORECASE)
multiEpRegex = re.compile(r'E\d*-E\d*', re.IGNORECASE)
dir_path = os.path.dirname(os.path.realpath(__file__))
tmdb = TMDB()
tvdb = TVDB()
favicon = os.path.join(dir_path, "favicon.ico")
folder = ""
clickCount = 0
validExtensions = ['.mp4', '.mkv', '.avi', '.m4v', '.mov', '.ts', '.m2ts', ".srt"]
siteList = ['TVDB', 'TMDB']
orderOptionList = ['AIRED', 'DVD']
tvdbActive = True
tmdbActive = True

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
				if 'TVDB' in self.site.get():
					searchShowTVDB()
				elif 'TMDB' in self.site.get():
					searchShowTMDB()

		def grabFiles(folder):
			count = 1
			self.files = []
			for file in sorted(os.listdir(folder)):
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
			
		def searchShowTVDB():
			global tvdbActive
			try: 
				shows = tvdb.getShow(self.show.get())
				if (len(shows['data']) > 1 ):
					self.output.configure(state=NORMAL)
					if len(self.output.get(1.0, END)) > 0:
						self.output.delete(1.0, END)
					self.output.insert('end', "Multiple shows detected, please find the one you searched for and enter the ID in the box above." + "\n")
					self.output.configure(state=DISABLED)
					self.output.see('end')
					self.output.update()
					for show in shows['data']:
						self.output.configure(state=NORMAL)
						self.output.insert('end', "Show Title: " + show['seriesName'] + " | Show ID: ")
						self.output.insert('end', str(show['id']), (str(show['id']), str(1)))
						self.output.insert('end', "\n")
						self.output.tag_config(str(show['id']), foreground="blue")
						self.output.tag_bind(str(show['id']), '<Button-1>', lambda event, url = "https://thetvdb.com/series/" + str(show['slug']): openLink(url))
						self.output.configure(state=DISABLED)
						self.output.update()
				elif (len(shows['data']) == 1):
					self.showID.insert('end', shows['data'][0]['id'])
			except InvalidCredentials:
				self.output.configure(state=NORMAL)
				self.output.insert(
					'end', "Unable to authorize with TVDB, try selecting TMDB. Otherwise you will be unable to grab episode data.")
				self.output.configure(state=DISABLED)
				self.output.see('end')
				self.output.update()
				tvdbActive = False
			except ShowNotFound:
				self.output.configure(state=NORMAL)
				self.output.insert(
					'end', "Unable to find any shows with TVDB, try selecting TMDB. Otherwise you will be unable to grab episode data.")
				self.output.configure(state=DISABLED)
				self.output.see('end')
				self.output.update()
			 

		def searchShowTMDB():
			""" WIP to be used for live searching of show """
			global tmdbActive
			try:
				shows = tmdb.getShow(self.show.get())
				if (len(shows['results']) > 1):
					self.output.configure(state=NORMAL)
					if len(self.output.get(1.0, END)) > 0:
						self.output.delete(1.0, END)
					self.output.insert('end', "Multiple shows detected, please find the one you searched for and enter the ID in the box above." + "\n")
					self.output.configure(state=DISABLED)
					self.output.see('end')
					self.output.update()
					for show in shows['results']:
						self.output.configure(state=NORMAL)
						self.output.insert('end', "Show Title: " + show['name'] + " | Show ID: ")
						self.output.insert('end', str(show['id']), (str(show['id']), str(1)))
						self.output.insert('end', "\n")
						self.output.tag_config(str(show['id']), foreground="blue")
						self.output.tag_bind(str(show['id']), '<Button-1>', lambda event, url = "https://www.themoviedb.org/tv/" + str(show["id"]) + "-" + str(show['name']): openLink(url))
						self.output.configure(state=DISABLED)
						self.output.update()
				elif (len(shows['results']) == 1):
					self.showID.insert('end', shows['results'][0]['id']) 
			except InvalidCredentials:
				self.output.configure(state=NORMAL)
				self.output.insert('end', "Unable to authorize with TMDB, try selecting TVDB. Otherwise you will be unable to grab episode data.")
				self.output.configure(state=DISABLED)
				self.output.see('end')
				self.output.update()
				tmdbActive = False
			except ShowNotFound:
				self.output.configure(state=NORMAL)
				self.output.insert('end', "Unable to find shows with TMDB, check for any spelling errors in provided title and try again.")
				self.output.configure(state=DISABLED)
				self.output.see('end')
				self.output.update()


		def renameFilesTVDB(show, season):
			try:
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
						order = self.variable.get()
						if (file.numEp > 0):
							i = 0
							while i <= file.numEp:
								if (i == 0):
									episodeName = tvdb.getEpisodeName(show, int(season), count, id=id, order=order)
									if len(self.files) >= 100:
										episodeNumber = "E{0:0=3d}".format(count)
									else:
										episodeNumber = "E{0:0=2d}".format(count)
								elif (i == file.numEp):
									episodeName = episodeName + " - " + tvdb.getEpisodeName(show, int(season), count, id=id, order=order)
									if len(self.files) >= 100:
										episodeNumber = episodeNumber + "-" + "E{0:0=3d}".format(count)
									else:
										episodeNumber = episodeNumber + "-" + "E{0:0=2d}".format(count)
								else:
									episodeName = episodeName + " - " + tvdb.getEpisodeName(show, int(season), count, id=id, order=order)								
								count += 1
								i += 1
						else:
							episodeName = tvdb.getEpisodeName(show, int(season), count, id=id, order=order)
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
						self.output.update()
						os.rename(os.path.join(self.folderSelected.get(), file.startName), os.path.join(self.folderSelected.get(), episode))					

				self.output.configure(state=NORMAL)
				self.output.insert('end', "Renaming Complete.\n")
				self.output.configure(state=DISABLED)
				self.output.see("end")
				self.output.update()
						
				self.selectFolder.config(relief=RAISED)

			except NoSuchEpisode:
				self.output.configure(state=NORMAL)
				self.output.insert('end', "No episode found in season for episode number, possibly too many files in folder.\n")
				self.output.configure(state=DISABLED)
				self.output.see("end")
				self.output.update()
						
				self.selectFolder.config(relief=RAISED)

		def renameFilesTMDB(show, season):
			try:
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
									episodeName = tmdb.getEpisodeName(show, int(season), count, id=id)
									if len(self.files) >= 100:
										episodeNumber = "E{0:0=3d}".format(count)
									else:
										episodeNumber = "E{0:0=2d}".format(count)
								elif (i == file.numEp):
									episodeName = episodeName + " - " + tmdb.getEpisodeName(show, int(season), count, id=id)
									if len(self.files) >= 100:
										episodeNumber = episodeNumber + "-" + "E{0:0=3d}".format(count)
									else:
										episodeNumber = episodeNumber + "-" + "E{0:0=2d}".format(count)
								else:
									episodeName = episodeName + " - " + tmdb.getEpisodeName(show, int(season), count, id=id)								
								count += 1
								i += 1
						else:
							episodeName = tmdb.getEpisodeName(show, int(season), count, id=id)
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
						self.output.update()
						os.rename(os.path.join(self.folderSelected.get(), file.startName), os.path.join(self.folderSelected.get(), episode))					

				self.output.configure(state=NORMAL)
				self.output.insert('end', "Renaming Complete.\n")
				self.output.configure(state=DISABLED)
				self.output.see("end")
				self.output.update()
						
				self.selectFolder.config(relief=RAISED)

			except NoSuchEpisode:
				self.output.configure(state=NORMAL)
				self.output.insert('end', "No episode found in season for episode number, possibly too many files in folder.\n")
				self.output.configure(state=DISABLED)
				self.output.see("end")
				self.output.update()
						
				self.selectFolder.config(relief=RAISED)

		def renameFiles(show, season):
			""" Takes in the given show title and season number and renames all files within the folder. """
			global tvdbActive
			global tmdbActive
			if ('TVDB' in self.site.get() and tvdbActive):
				renameFilesTVDB(show, season)
			elif ('TMDB' in self.site.get() and tmdbActive):
				renameFilesTMDB(show, season)
			else:
				grabFiles(self.folderSelected.get())
				
				self.undo.config(command=undoRename, state=ACTIVE, relief=RAISED)
				count = 1
				skipEpisodes = self.skipEpisodes.get().split(",")
				for file in self.files:
					extension = "." + file.startName.split(".")[len(file.startName.split("."))-1].lower()
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
									if len(self.files) >= 100:
										episodeNumber = "E{0:0=3d}".format(count)
									else:
										episodeNumber = "E{0:0=2d}".format(count)
								elif (i == file.numEp):
									if len(self.files) >= 100:
										episodeNumber = episodeNumber + "-" + "E{0:0=3d}".format(count)
									else:
										episodeNumber = episodeNumber + "-" + "E{0:0=2d}".format(count)								
								count += 1
								i += 1
						else:
							if len(self.files) >= 100:
								episodeNumber = "E{0:0=3d}".format(count)
							else:
								episodeNumber = "E{0:0=2d}".format(count)
							count += 1

						episode = show + " S" + "{0:0=2d}".format(int(season)) + episodeNumber
						
						file.setEndName(episode)
						self.output.configure(state=NORMAL)
						self.output.insert('end', 'Renaming: ' + file.startName + " --> " + episode + "\n")
						self.output.configure(state=DISABLED)
						self.output.see('end')
						self.output.update()
						os.rename(os.path.join(self.folderSelected.get(), file.startName), os.path.join(self.folderSelected.get(), episode))					

				self.output.configure(state=NORMAL)
				self.output.insert('end', "Renaming Complete.\n")
				self.output.configure(state=DISABLED)
				self.output.see("end")
				self.output.update()
						
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
				self.output.update()
				os.rename(os.path.join(file.path, file.endName),
                                    os.path.join(file.path, file.startName))

			self.undo.config(state=DISABLED, relief=SUNKEN)

		def openLink(url):
			webbrowser.open_new(url)

		def toggleEpisodeOrder(*args):
			if 'TVDB' in self.site.get():
				if len(self.folderSelected.get()) > 0 and 'No Folder Selected' not in self.folderSelected.get():
					searchShowTVDB()
				self.showID.delete(0, END)
				self.orderLabel.destroy()
				self.order.destroy()
				self.orderLabel = Label(master, text="Order Type:")
				self.orderLabel.place(x=8, y=34)
				self.order = OptionMenu(master, self.variable, *orderOptionList)
				self.order.place(x=75, y=34, width=75, height=22)
			elif 'TMDB' in self.site.get():
				if len(self.folderSelected.get()) > 0 and 'No Folder Selected' not in self.folderSelected.get():
					searchShowTMDB()
				self.showID.delete(0, END)
				self.orderLabel.destroy()
				self.order.destroy()

		def clearAll(event):
			self.show.delete(0, END)
			self.showID.delete(0, END)
			self.season.delete(0, END)
			self.skipEpisodes.delete(0, END)
			self.folderSelected.delete(0, END)
			self.undo.config(state=DISABLED, relief=SUNKEN)

		#Show Name
		self.input = Label(master, text="Show Name:")
		self.input.place(x=200, y=0)
		self.show = Entry(master)
		self.show.place(x=273, y=0, width=237, height=22)

		#Show ID
		self.id = Label(master, text="Show ID:", fg="grey")
		self.id.place(x=512, y=0)
		self.showID = Entry(master)
		self.showID.place(x=562, y=0, width=188, height=22)

		#Show Season
		self.seasonInput = Label(master, text="Season Number:")
		self.seasonInput.place(x=180, y=23)
		self.season = Entry(master, width="50")
		self.season.place(x=273, y=23, width=45, height=22)
		
		#Skipped Episodes
		self.skipEpisodeLabel = Label(master, text="Skip Missing Episodes:")
		self.skipEpisodeLabel.place(x=320, y=23)
		self.skipEpisodes = Entry(master)
		self.skipEpisodes.place(x=442, y=23, width=208, height=22)

		#Clear Button
		self.clearButton = Button(master, text="CLEAR ALL", fg="Red")
		self.clearButton.place(x=650, y=23, width=100, height=22)
		self.clearButton.bind("<Button-1>", clearAll)

		#Metadata Site Selector
		self.site = StringVar(master)
		self.site.set(siteList[0])
		self.siteSelectionLabel = Label(master, text="Site:")
		self.siteSelectionLabel.place(x=8, y=12)
		self.SiteSelection = OptionMenu(master, self.site, *siteList, command=toggleEpisodeOrder)
		self.SiteSelection.place(x=75, y=12, width=75, height=22)
		
		#Episode Ordering Selector
		self.variable = StringVar(master)
		self.variable.set(orderOptionList[0])
		self.orderLabel = Label(master, text="Order Type:")
		self.orderLabel.place(x=8, y=34)
		self.order = OptionMenu(master, self.variable, *orderOptionList)
		self.order.place(x=75, y=34, width=75, height=22)
		
		#Selected Folder
		self.selectedFolder = Label(master, text="Selected Folder:")
		self.selectedFolder.place(x=184, y=46)
		self.folderSelected = Entry(master, width="50")
		self.folderSelected.place(x=273, y=46, width=377, height=22)
		self.selectFolder = Button(master, text="Select Folder")
		self.selectFolder.place(x=650, y=47, width= 100, height=20)
		self.selectFolder.bind("<Button-1>", getFolder)

		#Rename Button
		self.rename = Button(master, text="Rename Files", state=DISABLED, relief=SUNKEN)
		self.rename.place(x=750, y=0, width=80, height=69)

		#Undo Button
		self.undo = Button(master, text="Undo Rename", state=DISABLED, relief=SUNKEN)
		self.undo.place(x=875, y=27)

		self.Font = font.Font(size=8)

		#Output Text Box
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
