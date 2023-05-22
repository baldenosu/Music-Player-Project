# Author: James Balden
# GitHub username: baldenosu
# Date: 4/24/2023
# Description: User Interface for the Track Trimming Tool Window

# Imports
import customtkinter
import pygame
from tinytag import TinyTag
from PlayerUI import TrackInformation
# from PIL import Image

pygame.mixer.init()
track = 'Griffin McElroy - Music from The Adventure Zone- Ethersea Vol. 1 - 01 The Adventure Zone- Ethersea - Main Theme.mp3'
metadata = TinyTag.get(track, image=True)


class TrimmingTool(customtkinter.CTkToplevel):
    """
    Class for creating a window instance of the playlists screen
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('700x400')
        self.title('Track Trimmer')

        self.track_info = TrackInformation(master=self, width=500, height=25, orientation='horizontal')
        self.track_info.grid(row=0, column=1, columnspan=4)

        self.slider = customtkinter.CTkSlider(master=self, from_=0, to=100, width=500, progress_color='purple')
        self.slider.grid(row=1, column=1, columnspan=4)
        self.slider.set(0)

        # Track elapsed time, track information, track length
        self.track_time = customtkinter.CTkLabel(master=self, text=f'{pygame.mixer.music.get_pos()}')
        self.track_length = customtkinter.CTkLabel(master=self,
                                                   text=f'{int(metadata.duration // 60)}:{int(metadata.duration % 60):2d}')
        self.track_time.grid(row=2, column=0, padx=20)
        self.track_length.grid(row=2, column=5, padx=20)

        # textbox for manual input of clipping positions
        self.track_time_input = customtkinter.CTkEntry(master=self, placeholder_text=f'{pygame.mixer.music.get_pos()}', width=60)
        self.track_length_input = customtkinter.CTkEntry(master=self, placeholder_text=f'{int(metadata.duration // 60)}:{int(metadata.duration % 60):2d}', width=60)

        self.track_time_input.grid(row=3, column=0, padx=20)
        self.track_length_input.grid(row=3, column=5, padx=20)
