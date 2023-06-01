# Author: James Balden
# GitHub username: baldenosu
# Date: 4/24/2023
# Description: User Interface for the Playlist Editor Window for creating playlists

# Imports
import customtkinter
import os


class PlaylistEditor(customtkinter.CTkToplevel):
    """
    Class for creating a window instance of the playlist Editor screen
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('500x500')
        self.title('Playlist Editor')
        self.minsize(500, 500)

        # Playlist Title, and Create Button
        self.playlist_label = customtkinter.CTkLabel(master=self, text='Playlist Name')
        self.playlist_label.grid(row=0, column=0, pady=10)
        self.playlist_name = customtkinter.CTkEntry(master=self, placeholder_text='Playlist 1')
        self.playlist_name.grid(row=0, column=1, pady=10)
        self.create_button = customtkinter.CTkButton(master=self, command=self.build_playlist, text='Create')
        self.create_button.grid(row=0, column=2, pady=10)

        # Add Tracks
        self.add_tracks_label = customtkinter.CTkLabel(master=self, text='Add Tracks')
        self.add_tracks_label.grid(row=1, column=0, pady=10)
        self.add_tracks_button = customtkinter.CTkButton(master=self, text='Chose File')
        self.add_tracks_button.grid(row=1, column=1, pady=10)

        # Tracks List label
        self.tracks_label = customtkinter.CTkLabel(master=self, text='Tracks')
        self.tracks_label.grid(row=2, column=0, pady=10)

        # Tracks list
        self.tracks_list = TracksListFrame(master=self, width=475, height=400)
        self.tracks_list.grid(row=3, column=0, columnspan=4)

    def build_playlist(self):
        """
        function for building playlist based on the current tracklist. Saves the track files to a folder with the
        name of the playlist stored in the playlist folder.

        :return:
        """
        # Create a folder with the playlist name
        playlist_name = self.playlist_name.get()
        playlists_folder_path = 'D:/OSU Spring 2023/CS 361 Software Development/Assignments/Assignment-5/Playlists'
        playlist_location = playlists_folder_path + '/' + playlist_name
        os.mkdir(playlist_location)
        # grab all the track files from the tracklist and store them as files in the folder
        # Give message that playlist was successfully created


class TracksListFrame(customtkinter.CTkScrollableFrame):
    """
    Class for the frame that holds all the track information for the playlist being created. All stored in scrollable
    frame if contents of playlist become to large for window.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tracks = []

        self.columnconfigure(0, weight=1)

        # Frame to hold tracks information for the playlist
        for i in range(10):
            track = TrackFrame(master=self, track_num= i+1)
            track.grid(row=i, column=0, pady=10)
            self.tracks.append(track)


class TrackFrame(customtkinter.CTkFrame):
    """
    Class for individual track frame to be stored in the tracklist frame
    """
    def __init__(self, master, track_num: int, **kwargs):
        super().__init__(master, **kwargs)

        # Track Number
        self.track_number = track_num
        self.track_number_label = customtkinter.CTkLabel(self, text=track_num)
        self.track_number_label.grid(row=0, column=0)

        # Track Name
        self.track_name = customtkinter.CTkLabel(self, text='track name')
        self.track_name.grid(row=0, column=1, padx=10)

        # Artist
        self.artist = customtkinter.CTkLabel(self, text='Artist Name')
        self.artist.grid(row=0, column=2, padx=10)

        # Length
        self.track_length = customtkinter.CTkLabel(self, text='5:00')
        self.track_length.grid(row=0, column=3, padx=10)

        # Delete Button
        self.delete_button = customtkinter.CTkButton(self, command=self.delete_track, text='Delete', width=60)
        self.delete_button.grid(row=0, column=4, padx=10)

    def delete_track(self):
        """
        Function that deletes a track from the track list

        :return: None
        """
        for widget in self.winfo_children():
            widget.destroy()



