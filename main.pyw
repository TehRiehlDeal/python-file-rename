#!/usr/bin/python3

import os
import re
from tkinter import filedialog, END, ACTIVE, RAISED, DISABLED, SUNKEN, Label, Entry, Button, Text, Tk, NORMAL, font, StringVar, OptionMenu, Frame, Canvas
from tkinter.constants import ALL, NW
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
from PIL import Image, ImageTk

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
        self.root.title(title)
        geometry = str(width) + "x" + str(height)
        self.root.geometry(geometry)
        self.root.protocol("WM_DELETE_WINDOW", self.end)
        self.root.iconbitmap(FAVICON)
        self.frame = Frame(master=self.root)

        self.canvas = Canvas(master=self.root, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0, width=width, height=height)

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

        self.animation = self.animation(1,1)

        """ Initialize all Label Components """
        self.showNameLabel = ShowLabel(self, "Show Name:", 200, 0)

        """ Initialize all Entry Components """
        self.showName = ShowName(self, 237, 22, 273, 0)

    def animation(window, xinc, yinc):
        window.pic = Image.open("./favicon.ico")
        window.picTK = ImageTk.PhotoImage(window.pic)
        window.canvas.create_image(0,0, image=window.picTK)

class UserEntry:
    def __init__(self, mainwindow):
        self.canvas = Canvas(master=mainwindow.canvas, width=1024, height=70, bg="#FAF9F6", highlightthickness=0)
        self.canvas.grid(row=0, column=1)

class MyLabel:
    def __init__(self, mainwindow, text, x, y, bg="#FAF9F6"):
        self.label = Label(master=mainwindow.canvas, text=text, bg=bg)
        self.label.place(x=x, y=y)

class ShowLabel(MyLabel):
    def __init__(self,mainwindow, text, x, y):
        super().__init__(mainwindow, text, x, y)

class MyEntry:
    def __init__(self, mainwindow, width, height, x, y):
        self.entry = Entry(master=mainwindow.canvas)
        self.entry.place(x=x, y=y, width=width, height=height)

class ShowName(MyEntry):
    def __init__(self, mainwindow, width, height, x, y):
        super().__init__(mainwindow, width, height, x, y)




def main():
    mainApp = App("Teh Riehl TV Show Renamer", 1024, 768)
    mainApp.initialize()
    mainApp.run()

if __name__ == '__main__':
    main()
