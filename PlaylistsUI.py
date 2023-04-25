# Author: James Balden
# GitHub username: baldenosu
# Date: 4/24/2023
# Description: User interface for the playlists window

# Imports
import customtkinter
import PlaylistEditorUI
# from PIL import Image


class Playlists(customtkinter.CTkToplevel):
    """
    Class for creating a window instance of the playlists screen
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('800x500')
        self.title('Playlists')
        self.editor_window = None

        # Playlists Frames containing playlist names and buttons for functions you can perform on the playlist.
        self.playlist_frame = PlaylistFrame(master=self)
        self.playlist_frame.grid(row=0, column=0)

        self.playlist_frame2 = PlaylistFrame(master=self)
        self.playlist_frame2.grid(row=1, column=0)

        # Create a new Playlist button
        self.create_playlist_button = customtkinter.CTkButton(master=self, command=self.create_playlist, text='Create Playlist')
        self.create_playlist_button.grid(row=2, column=0, pady=10)

    def create_playlist(self):
        if self.editor_window is None or not self.editor_window.winfo_exists():
            self.editor_window = PlaylistEditorUI.PlaylistEditor(self)
            self.editor_window.after(20, self.editor_window.lift)
        else:
            self.editor_window.focus()


class PlaylistFrame(customtkinter.CTkFrame):
    """
    Class for creating a single playlist inside a tkinter frame for adding to the list of playlists
    """
    def __init__(self, master):
        super().__init__(master)

        self.editor_window = None
        self.delete_window = None

        # Playlist title
        self.playlist_name = customtkinter.CTkLabel(self, text='Playlist Name', width=500, height=50)
        self.playlist_name.grid(row=0, column=0)

        # Play Button
        self.play_button = customtkinter.CTkButton(self, text='Play', width=60)
        self.play_button.grid(row=0, column=1, padx=20)
        # Edit Button
        self.edit_button = customtkinter.CTkButton(master=self, command=self.open_playlist_editor, text='Edit', width=60)
        self.edit_button.grid(row=0, column=2, padx=20)
        # Delete Button
        self.delete_button = customtkinter.CTkButton(self, command=self.delete_playlist, text='Delete', width=60)
        self.delete_button.grid(row=0, column=3, padx=20)

    def open_playlist_editor(self):
        if self.editor_window is None or not self.editor_window.winfo_exists():
            self.editor_window = PlaylistEditorUI.PlaylistEditor(self)
            self.editor_window.after(20, self.editor_window.lift)
        else:
            self.editor_window.focus()

    def delete_playlist(self):
        delete_message = customtkinter.CTkInputDialog(text='Are you sure your want to delete this Playlist? Type "Yes" to continue', title='Warning: Deleting Playlist')
        choice = delete_message.get_input()
        if choice == 'Yes':
            for widget in self.winfo_children():
                widget.destroy()


class DeleteWarning(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.delete_message = customtkinter.CTkLabel(self, text='Are you sure you want to delete this Playlist?')
        self.delete_message.grid(row=0)

        self.yes_button = customtkinter.CTkButton(self, text='Yes')
        self.yes_button.grid(row=0, column=0, padx=10, pady=10)

        self.cancel_button = customtkinter.CTkButton(self, text='Cancel')
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)



