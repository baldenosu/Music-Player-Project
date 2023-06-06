# Author: James Balden
# GitHub username: baldenosu
# Date: 4/24/2023
# Description: User interface for the playlists window, part of the music player project. Users can play, edit, and
# delete playlists.

# Imports
import os
import shutil
import customtkinter
import PlaylistEditorUI


class Playlists(customtkinter.CTkToplevel):
    """
    Class for creating a window instance of the playlists screen
    """
    def __init__(self, queue_playlist, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('800x500')
        self.title('Playlists')
        self.editor_window = None
        self.playlists = []

        # Playlists Frames containing playlist names and buttons for functions you can perform on the playlist.
        playlists_folder_path = 'D:/OSU Spring 2023/CS 361 Software Development/Assignments/Assignment-5/Playlists'
        with os.scandir(playlists_folder_path) as playlists_folder:
            for folder in playlists_folder:
                if folder.is_dir():
                    playlist = PlaylistFrame(master=self, playlist_name=folder.name, queue_playlist=queue_playlist, close_window=self.close_window)
                    self.playlists.append(playlist)
                    playlist.grid(row=len(self.playlists)+1, column=0)

        # Create a new Playlist button
        self.create_playlist_button = customtkinter.CTkButton(master=self, command=self.create_playlist, text='Create Playlist')
        self.create_playlist_button.grid(row=0, column=0, pady=10)

    def create_playlist(self):
        """
        Function for handling the opening of the playlist editor when the create playlist button is pressed. Also asks
        the user if they would like help in creating the playlist

        :return: None
        """
        create_message = customtkinter.CTkInputDialog(
            text='Would you like me to walk you through the process of creating a Playlist?',
            title='Creating New Playlist')
        choice = create_message.get_input()
        if self.editor_window is None or not self.editor_window.winfo_exists():
            self.editor_window = PlaylistEditorUI.PlaylistEditor(self)
            self.editor_window.after(20, self.editor_window.lift)
        else:
            self.editor_window.focus()

    def close_window(self):
        """
        Function to close window when playlist is selected to play.
        :return:
        """
        self.destroy()


class PlaylistFrame(customtkinter.CTkFrame):
    """
    Class for creating a single playlist inside a tkinter frame for adding to the list of playlists
    """
    def __init__(self, master, playlist_name: str, queue_playlist, close_window):
        super().__init__(master)

        self.editor_window = None
        self.delete_window = None
        self.queue_playlist = queue_playlist
        self.close_window = close_window

        # Playlist title
        self.playlist_name = playlist_name
        self.playlist_name_label = customtkinter.CTkLabel(self, text=playlist_name, width=500, height=50)
        self.playlist_name_label.grid(row=0, column=0)

        # Play Button
        self.play_button = customtkinter.CTkButton(self, text='Play', command=self.play_playlist, width=60)
        self.play_button.grid(row=0, column=1, padx=20)

        # Edit Button
        self.edit_button = customtkinter.CTkButton(master=self, command=self.open_playlist_editor, text='Edit', width=60)
        self.edit_button.grid(row=0, column=2, padx=20)

        # Delete Button
        self.delete_button = customtkinter.CTkButton(self, command=self.delete_playlist, text='Delete', width=60)
        self.delete_button.grid(row=0, column=3, padx=20)

    def play_playlist(self):
        """
        Function that facilitates the queuing up of a playlist for playback and transition back to the main player
        window.

        :return: None
        """
        # Get the location information for the playlist
        playlist_name = self.playlist_name
        # call the queuing function to transfer the playlist over to the main player
        self.queue_playlist(playlist_name)
        # close the playlist window
        self.close_window()

    def open_playlist_editor(self):
        """
        Function to facilitate opening the playlist editor window when the create playlist button, or edit button is
        clicked.
        :return: None
        """
        if self.editor_window is None or not self.editor_window.winfo_exists():
            self.editor_window = PlaylistEditorUI.PlaylistEditor(self)
            self.editor_window.after(20, self.editor_window.lift)
        else:
            self.editor_window.focus()

    def delete_playlist(self):
        """
        Function that deletes playlist from the list of available playlists

        :return: None
        """
        delete_message = customtkinter.CTkInputDialog(text='Are you sure you want to delete this Playlist? Type "Yes" to continue', title='Warning: Deleting Playlist')
        choice = delete_message.get_input()
        # Delete the directory and all its tracks from the playlist directory and remove widgets from frame.
        if choice == 'Yes':
            playlists_folder_path = 'D:/OSU Spring 2023/CS 361 Software Development/Assignments/Assignment-5/Playlists'
            playlist_name = self.playlist_name
            playlist_location = playlists_folder_path + '/' + playlist_name
            shutil.rmtree(playlist_location)
            for widget in self.winfo_children():
                widget.destroy()
            self.destroy()


class DeleteWarning(customtkinter.CTkFrame):
    """
    Class for creating a warning window when the delete button is pressed for deletion of a playlist.
    """
    def __init__(self, master):
        super().__init__(master)

        self.delete_message = customtkinter.CTkLabel(self, text='Are you sure you want to delete this Playlist?')
        self.delete_message.grid(row=0)

        self.yes_button = customtkinter.CTkButton(self, text='Yes')
        self.yes_button.grid(row=0, column=0, padx=10, pady=10)

        self.cancel_button = customtkinter.CTkButton(self, text='Cancel')
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)



