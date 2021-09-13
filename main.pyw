#!/usr/bin/python3

import os
import re
from tkinter import filedialog, END, ACTIVE, RAISED, DISABLED, SUNKEN, Label, Entry, Button, Text, Tk, NORMAL, font, StringVar, OptionMenu, Frame, Canvas
from tkinter.constants import ALL
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

episodeRegex = re.compile(r'S\d*E\d*', re.IGNORECASE)
dir_path = os.path.dirname(os.path.realpath(__file__))
tmdb = TMDB()
tvdb = TVDB()
FAVICON = os.path.join(dir_path, 'favicon.ico')
VALID_VIDEO_EXTENSIONS = ['mp4', '.mkv', '.avi', '.m4v', '.mov', '.ts', '.m2ts']
VALID_SUBTITLE_EXTENSIONS = ['.srt']
OPTIONS_LIST = ['AIRED', 'DVD']

class MainWindow:
    def __init__(self, title, width, height):
        self.root = Tk()
        self.root.title = title
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.frame = Frame(master=self.root)

        self.canvas = Canvas(master=self.root, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=2, columnspan=1)

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def run(self):
        #self._run()
        self.root.mainloop()
        
    def _run(self):
        self.update()
        self.paint()

    def end(self):
        self.root.destroy()

    def update(self):
        for obj in self.objects:
            obj.update()
    
    def paint(self):
        self.canvas.delete(ALL)
        for obj in self.objects:
            obj.paint(self.canvas)

class App(MainWindow):
    def __init__(self, title, width, height):
        super().__init__(title, width, height)

    def initialize(self):
        self.userEntry = UserEntry(self)


    

    

class UserEntry:
    def __init__(self, mainwindow):
        self.canvas = Canvas(master=mainwindow.frame, width=1024, height=70, bg="black", highlightthickness=0)
        self.canvas.grid(row=0, column=1)



def main():
    mainApp = App("Teh Riehl TV Show Renamer", 1024, 1024)
    mainApp.initialize()
    mainApp.run()

if __name__ == '__main__':
    main()
