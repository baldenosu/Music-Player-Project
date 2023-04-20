# Author: James Balden
# GitHub username: baldenosu
# Date: 4/19/2023
# Description: User Interface for Music Player Program built as term project
# CS 361.
# Code citation: https://www.geeksforgeeks.org/python-gui-tkinter/
# https://docs.python.org/3/library/tkinter.ttk.html#widget
# https://docs.python.org/3/library/tkinter.html#tkinter-modules
# slider: youtube.com/watch?v=CXMcNbo8PLE


# Set up Imports
from tkinter import *
from tkinter.ttk import *

# Set up GUI window
main = Tk()
main.title('Music Player')

# Widgets Setup --------------------------------------------------------------

# image holder
album_art = PhotoImage(file = 'astleyAlbumArt.png')

# track slider
track_slider = Scale(main, from_ = 0, to = 100, orient = 'horizontal')

# timing current, song info, timing total

# playlist button, back button, play/pause button, forward button, repeat button
playlist_button = Button()
back_button = Button()
play_button = Button()
skip_button = Button()
repeat_button = Button()

# Grid Layout ----------------------------------------------------------------
Label(main, image = album_art).grid(row = 0, column = 0, columnspan = 5)
track_slider.grid(row = 1, column = 0, columnspan = 5)
playlist_button.grid(row = 2, column = 0)
back_button.grid(row = 2, column = 1)
play_button.grid(row= 2, column = 2)
skip_button.grid(row = 2, column = 3)
repeat_button.grid(row = 2, column = 4)

# Set up main loop.
main.mainloop()