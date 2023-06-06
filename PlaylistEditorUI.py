# Author: James Balden
# GitHub username: baldenosu
# Date: 4/24/2023
# Description: User Interface for the Playlist Editor Window for creating playlists as part of the music player project.

# Imports
import customtkinter
import os
import shutil
from tkinter import filedialog
from tinytag import TinyTag


class PlaylistEditor(customtkinter.CTkToplevel):
    """
    Class for creating a window instance of the playlist Editor screen
    """
    def __init__(self, update_playlist_view, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('500x500')
        self.title('Playlist Editor')
        self.minsize(500, 500)

        self.update_playlist_view = update_playlist_view

        # Playlist Title, and Create Button
        self.playlist_label = customtkinter.CTkLabel(master=self, text='Playlist Name')
        self.playlist_label.grid(row=0, column=0, pady=10)
        self.playlist_name = customtkinter.CTkEntry(master=self, placeholder_text='Playlist 1')
        self.playlist_name.grid(row=0, column=1, pady=10)
        self.create_button = customtkinter.CTkButton(master=self, command=self.build_playlist, text='Create')
        self.create_button.grid(row=0, column=2, pady=10)

        # Tracks List label
        self.tracks_label = customtkinter.CTkLabel(master=self, text='Tracks')
        self.tracks_label.grid(row=2, column=0, pady=10)

        # Tracks list
        self.tracks_list = TracksListFrame(master=self, width=475, height=400)
        self.tracks_list.grid(row=3, column=0, columnspan=4)

        # Add Tracks system
        self.add_tracks_label = customtkinter.CTkLabel(master=self, text='Add Tracks')
        self.add_tracks_label.grid(row=1, column=0, pady=10)
        self.add_tracks_button = customtkinter.CTkButton(master=self, command=self.tracks_list.add_track, text='Choose File')
        self.add_tracks_button.grid(row=1, column=1, pady=10)

    def build_playlist(self):
        """
        function for building playlist based on the current tracklist. Saves the track files to a folder with the
        name of the playlist stored in the playlist folder.

        :return: None
        """
        # Create a folder with the playlist name
        playlist_name = self.playlist_name.get()
        playlists_folder_path = 'D:/OSU Spring 2023/CS 361 Software Development/Assignments/Assignment-5/Playlists'
        playlist_location = playlists_folder_path + '/' + playlist_name
        os.mkdir(playlist_location)
        # grab all the track files from the tracklist and store them as files in the folder
        playlist_tracks = self.tracks_list.get_tracks()
        for filename in playlist_tracks:
            if os.path.isfile(filename):
                shutil.copy(filename, playlist_location)
        # Give message that playlist was successfully created
        playlist_built_message = customtkinter.CTkInputDialog(text='Playlist built successfully, you may close the editor', title='Playlist Created')
        self.update_playlist_view(playlist_name)


class TracksListFrame(customtkinter.CTkScrollableFrame):
    """
    Class for the frame that holds all the track information for the playlist being created. All stored in scrollable
    frame if contents of playlist become to large for window.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Create a list for holding the songs in the playlist
        self.tracks = []

        self.columnconfigure(0, weight=1)

    def add_track(self):
        """
        Function for adding a track file to the track list.

        :return: None
        """
        track_file = filedialog.askopenfilename()
        self.focus()
        metadata = TinyTag.get(track_file, image=True)
        new_track = TrackFrame(master=self, track_file=track_file, track_num=len(self.tracks)+1, metadata=metadata)
        self.tracks.append(new_track)
        new_track.grid(row=len(self.tracks), column=0, pady=10)

    def get_tracks(self):
        """
        Gets the list of track files from the tracklist frame for use in creating the playlist

        :return: track_files a list of track files for the playlist
        """
        track_files = []
        for track in self.tracks:
            track_files.append(track.get_track_file())
        return track_files


class TrackFrame(customtkinter.CTkFrame):
    """
    Class for individual track frame to be stored in the tracklist frame
    """
    def __init__(self, master, track_file: str, track_num: int, metadata: object, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((1, 2), weight=1)

        self.track_file = track_file

        # Track Number
        self.track_number = track_num
        self.track_number_label = customtkinter.CTkLabel(self, text=track_num)
        self.track_number_label.grid(row=0, column=0, padx=5, sticky="ew")

        # Track Name
        self.track_name = metadata.title
        self.track_name_label = customtkinter.CTkLabel(self, text=self.track_name)
        self.track_name_label.grid(row=0, column=1)

        # Artist
        self.artist = metadata.artist
        self.artist_label = customtkinter.CTkLabel(self, text=self.artist)
        self.artist_label.grid(row=0, column=2, padx=10)

        # Length
        self.track_length = metadata.duration
        self.track_length_label = customtkinter.CTkLabel(self, text=f'{int(metadata.duration//60)}:{int(metadata.duration%60):02d}')
        self.track_length_label.grid(row=0, column=3, padx=10)

        # Delete Button
        self.delete_button = customtkinter.CTkButton(self, command=self.delete_track, text='Delete', width=60, hover_color='red')
        self.delete_button.grid(row=0, column=4, padx=10)

    def delete_track(self):
        """
        Function that deletes a track from the track list

        :return: None
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()

    def get_track_file(self):
        """
        Function to retrieve the file for the track

        :return: track file location
        """
        return self.track_file



