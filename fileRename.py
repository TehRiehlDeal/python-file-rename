import os
import sys
import re

regex = re.compile(r'S\d*E\d*', re.IGNORECASE)
folder = sys.argv[1] #raw_input("Please select a directory: ")
show = sys.argv[2] #raw_input("Input Show's Title: ")

for file in os.listdir(folder):
	extension = "." + file.split(".")[len(file.split("."))-1]
	matched = regex.findall(file)
	if matched:
		season = matched[0]
		season = season.upper()
		episodeName = show + " " + season + extension
		os.rename(os.path.join(folder, file), os.path.join(folder, episodeName))
