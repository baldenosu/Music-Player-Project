# Author: James Balden
# GitHub username: baldenosu
# Date: 4/19/2023
# Description: User Interface for Music Player Program built as term project
# CS 361.
# Code citation: https://www.geeksforgeeks.org/python-gui-tkinter/
#

# Set up Imports
from tkinter import *
from tkinter.ttk import *

# Set up GUI window
main = Tk()

# Layout
main.title('Music Player')
# image holder
album_art = PhotoImage(file = 'astleyAlbumArt.png')
Label(main, image = album_art).grid(row = 0, column = 0)
# music slider
#track_slider
# timing current, song info, timing total
# playlist button, back button, play/pause button, forward button, repeat button

# Set up main loop.
main.mainloop()