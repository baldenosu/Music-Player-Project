# Author: James Balden
# GitHub username: baldenosu
# Date: 4/22/2023
# Description: User Interface for the player window of the music player app.

# code citations : https://customtkinter.tomschimansky.com/documentation/

# Imports
import customtkinter
from PIL import Image
import PlaylistsUI

customtkinter.set_appearance_mode('dark')


class Player(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('400x400')
        self.title('Music Player')
        self.minsize(400, 400)

        # Load Images
        self.album_image = customtkinter.CTkImage(light_image=Image.open('astleyAlbumArt.png'), size=(200, 200))
        # self.playlist_image = customtkinter.CTkImage(Image.open('Images/Playlists.png'), size=(28, 21))
        # self.back_image = customtkinter.CTkImage(Image.open('Images/Back.png'), size=(31, 22))
        # self.play_image = customtkinter.CTkImage(Image.open('Images/Play.png'), size=(29, 33))
        # self.pause_image = customtkinter.CTkImage(Image.open('Images/Pause.png'), size=(23, 32))
        # self.skip_image = customtkinter.CTkImage(Image.open('Images/Skip.png'), size=(31, 22))
        # self.repeat_image = customtkinter.CTkImage(Image.open('Images/Repeat.png'), size=(31, 22))

        # Album Art Image
        self.album_art_label = customtkinter.CTkLabel(master=self, text='', image=self.album_image)
        self.album_art_label.grid(row=0, column=0, columnspan=5)

        # Track Information
        self.track_info = customtkinter.CTkLabel(master=self, text='Song: Never Gonna Give You Up  Artist: Rick Astley')
        self.track_info.grid(row=1, column=0, columnspan=5)

        # Track Slider
        self.slider = customtkinter.CTkSlider(master=self, from_=0, to=100, width=400)
        self.slider.grid(row=2, column=0, columnspan=5)

        # Track elapsed time, track information, track length
        self.track_time = customtkinter.CTkLabel(master=self, text='0:00')
        self.track_length = customtkinter.CTkLabel(master=self, text='5:00')
        self.track_time.grid(row=3, column=0)
        self.track_length.grid(row=3, column=4)

        # Player Button Controls
        self.playlist_button = customtkinter.CTkButton(master=self, command=self.open_playlists, text='Playlists', width=60)
        self.playlist_button.grid(row=4, column=0)
        self.back_button = customtkinter.CTkButton(master=self, text='Back', width=60)
        self.back_button.grid(row=4, column=1)
        self.play_button = customtkinter.CTkButton(master=self, text='Play', width=60)
        self.play_button.grid(row=4, column=2)
        self.pause_button = customtkinter.CTkButton(master=self, text='Pause', width=60)
        # self.pause_button.grid(row=3,column=0)
        self.skip_button = customtkinter.CTkButton(master=self, text='Skip', width=60)
        self.skip_button.grid(row=4, column=3)
        self.repeat_button = customtkinter.CTkButton(master=self, text='Repeat', width=60)
        self.repeat_button.grid(row=4, column=4)

        self.playlist_window = None

    def open_playlists(self):
        if self.playlist_window is None or not self.playlist_window.winfo_exists():
            self.playlist_window = PlaylistsUI.Playlists(self)
            self.playlist_window.after(20, self.playlist_window.lift)
        else:
            self.playlist_window.focus()


if __name__ == "__main__":
    app = Player()
    app.mainloop()



