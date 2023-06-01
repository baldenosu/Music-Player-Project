# Author: James Balden
# GitHub username: baldenosu
# Date: 4/22/2023
# Description: User Interface for the player window of the music player app.

# code citations : https://customtkinter.tomschimansky.com/documentation/

# Imports
import customtkinter
from PIL import Image
import pygame
from tinytag import TinyTag
from tktooltip import ToolTip
import PlaylistsUI
import TrimmingToolUI
import zmq

# Set up for communication with metadata microservice
context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:7854")

# Set up for UI appearance
customtkinter.set_appearance_mode('dark')

# Setup Sound control
pygame.mixer.init()
track = 'Main Theme.mp3'
metadata = TinyTag.get(track, image=True)

# Send track file path to microservice to get the metadata then retrieve it and store it for display
socket.send_pyobj(track)
track_title, track_album, track_artist, track_number = socket.recv_pyobj()

pygame.mixer.music.load(track)
pygame.mixer.music.play()
pygame.mixer.music.pause()


class TrackInformation(customtkinter.CTkScrollableFrame):
    """
    Class for the frame that contains track data including track title, artist, album, made scrollable for when metadata
    does not fit in window.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.track_info = customtkinter.CTkLabel(master=self, text=f'Song: {track_title} | Artist: {track_artist} | Album: {track_album} | Track number: {track_number}')
        self.track_info.grid(row=1, column=0, columnspan=5)


class Player(customtkinter.CTk):
    """
    Player class that creates the user interface window for the player. Contains functions for various UI buttons.
    """
    def __init__(self):
        super().__init__()

        self.geometry('400x400')
        self.title('Music Player')
        self.minsize(400, 400)

        # Load Images
        self.album_image = customtkinter.CTkImage(light_image=Image.open('cover.png'), size=(200, 200))
        self.playlist_image = customtkinter.CTkImage(Image.open('Images/Playlists.png'), size=(28, 21))
        self.back_image = customtkinter.CTkImage(Image.open('Images/Back.png'), size=(31, 22))
        self.play_image = customtkinter.CTkImage(Image.open('Images/Play.png'), size=(29, 33))
        self.pause_image = customtkinter.CTkImage(Image.open('Images/Pause.png'), size=(23, 32))
        self.skip_image = customtkinter.CTkImage(Image.open('Images/Skip.png'), size=(31, 22))
        self.repeat_image = customtkinter.CTkImage(Image.open('Images/Repeat.png'), size=(31, 22))

        # Advanced Tools Menu
        self.advanced_var = customtkinter.StringVar(value='Advanced Tools')
        self.tools_menu = customtkinter.CTkOptionMenu(master=self, values=['Trimming Tool'], variable=self.advanced_var, command=self.tool_menu_control)
        self.tools_menu.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10))

        # Album Art Image
        self.album_art_label = customtkinter.CTkLabel(master=self, text='', image=self.album_image)
        self.album_art_label.grid(row=1, column=0, columnspan=5)

        # Track Information
        self.track_info = TrackInformation(master=self, width=300, height=25, orientation='horizontal')
        self.track_info.grid(row=2, column=0, columnspan=5)

        # Track Slider
        self.slider = customtkinter.CTkSlider(master=self, from_=0, to=100, width=400, progress_color='purple')
        self.slider.grid(row=3, column=0, columnspan=5)
        self.slider.set(0)

        # Track elapsed time, track information, track length
        self.track_time = customtkinter.CTkLabel(master=self, text=f'{pygame.mixer.music.get_pos()}')
        self.track_length = customtkinter.CTkLabel(master=self, text=f'{int(metadata.duration//60)}:{int(metadata.duration%60):2d}')
        self.track_time.grid(row=4, column=0)
        self.track_length.grid(row=4, column=4)

        # Player Button Controls
        self.playlist_button = customtkinter.CTkButton(master=self, command=self.open_playlists, image=self.playlist_image, text='', height=60, width=60)
        self.playlist_button.grid(row=5, column=0)
        self.back_button = customtkinter.CTkButton(master=self, image=self.back_image, text='', height=60, width=60)
        self.back_button.grid(row=5, column=1)
        self.play_button = customtkinter.CTkButton(master=self, command=self.play_pause_button, image=self.play_image, text='', height=60, width=60)
        self.play_button.grid(row=5, column=2)
        self.skip_button = customtkinter.CTkButton(master=self, image=self.skip_image, text='', height=60, width=60)
        self.skip_button.grid(row=5, column=3)
        self.repeat_button = customtkinter.CTkButton(master=self, image=self.repeat_image, text='', height=60, width=60)
        self.repeat_button.grid(row=5, column=4)

        # Tooltips
        self.playlist_tooltip = ToolTip(self.playlist_button, msg='Opens the playlist menu for selecting and creating playlists', delay=1.0)

        self.playlist_window = None
        self.trimmer_window = None

    def open_playlists(self):
        """
        function that opens the playlists window when the playlist button is pressed

        :return: None
        """
        if self.playlist_window is None or not self.playlist_window.winfo_exists():
            self.playlist_window = PlaylistsUI.Playlists(self)
            self.playlist_window.after(20, self.playlist_window.lift)
        else:
            self.playlist_window.focus()

    def play_pause_button(self):
        """
        Function for pausing and unpausing the track when the play/pause button is pressed, this also changes the button
        image accordingly.

        :return: None
        """
        current_state = self.play_button.cget('image')
        if current_state == self.play_image:
            self.play_button.configure(image=self.pause_image, text='', height=60, width=60)
            pygame.mixer.music.unpause()
        else:
            self.play_button.configure(image=self.play_image, text='', height=60, width=60)
            pygame.mixer.music.pause()

    def tool_menu_control(self, choice):
        """
        Function for controlling tool menu UI. Opens correct tool window based on user input click.

        :param choice: Clicked button in the tool selection menu

        :return: None
        """
        if choice == "Trimming Tool":
            if self.trimmer_window is None or not self.trimmer_window.winfo_exists():
                self.trimmer_window = TrimmingToolUI.TrimmingTool(self)
                self.trimmer_window.after(20, self.trimmer_window.lift)
            else:
                self.trimmer_window.focus()




if __name__ == "__main__":
    app = Player()
    app.mainloop()



