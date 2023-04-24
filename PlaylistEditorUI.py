# Author: James Balden
# GitHub username: baldenosu
# Date: 4/24/2023
# Description: User Interface for the Playlist Editor Window for creating playlists

# Imports
import customtkinter


class PlaylistEditor(customtkinter.CTkToplevel):
    """
    Class for creating a window instance of the playlists screen
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('500x500')
        self.title('Playlist Editor')

        # Playlist Title
        self.playlist_label = customtkinter.CTkLabel(master=self, text='Playlist Name')
        self.playlist_label.grid(row=0, column=0)
        self.playlist_name = customtkinter.CTkEntry(master=self, placeholder_text='Playlist 1')
        self.playlist_name.grid(row=0, column=1)

        # Add Tracks

        # Tracks list