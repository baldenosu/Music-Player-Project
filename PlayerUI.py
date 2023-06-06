# Author: James Balden
# GitHub username: baldenosu
# Date: 4/22/2023
# Description: User Interface for the player window of the music player app.

# code citations : https://customtkinter.tomschimansky.com/documentation/
# Help with transferring data between windows: https://www.youtube.com/watch?v=wHeoWM4xv0U

# Imports
import os
import customtkinter
from PIL import Image
import pygame
from tinytag import TinyTag
from tktooltip import ToolTip
import PlaylistsUI
import zmq

# Set up for communication with metadata microservice
context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:7854")

# Set up for UI appearance
customtkinter.set_appearance_mode('dark')

# Setup Sound control
pygame.mixer.init()
pygame.init()


class TrackInformation(customtkinter.CTkScrollableFrame):
    """
    Class for the frame that contains track data including track title, artist, album, made scrollable for when metadata
    does not fit in window.
    """
    def __init__(self,  master, track_title='none', track_artist='none', track_album='none', track_number='none', **kwargs):
        super().__init__(master, **kwargs)

        self.track_info = customtkinter.CTkLabel(master=self, text=f'Song: {track_title} | Artist: {track_artist} | Album: {track_album} | Track number: {track_number}')
        self.track_info.grid(row=1, column=0, columnspan=5)

    def update_information(self, track_title, track_artist, track_album, track_number):
        self.track_info.configure(text=f'Song: {track_title} | Artist: {track_artist} | Album: {track_album} | Track number: {track_number}')


class Player(customtkinter.CTk):
    """
    Player class that creates the user interface window for the player. Contains functions for various UI buttons.
    """
    def __init__(self):
        super().__init__()

        self.geometry('400x400')
        self.title('Music Player')
        self.minsize(400, 400)

        self.queued_tracks = []
        self.current_playlist = None
        self.track_number_playing = 0
        self.track_position = 0

        # Set music end
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

        # for recurring functions
        self.after_current_time_id = None
        self.after_track_slide_id = None
        self.after_start_next_track_id = None

        # Load Images
        self.album_image = customtkinter.CTkImage(dark_image=Image.open('MUSIC PLAYER.png'), size=(200, 200))
        self.playlist_image = customtkinter.CTkImage(Image.open('Images/Playlists.png'), size=(28, 21))
        self.back_image = customtkinter.CTkImage(Image.open('Images/Back.png'), size=(31, 22))
        self.play_image = customtkinter.CTkImage(Image.open('Images/Play.png'), size=(29, 33))
        self.pause_image = customtkinter.CTkImage(Image.open('Images/Pause.png'), size=(23, 32))
        self.skip_image = customtkinter.CTkImage(Image.open('Images/Skip.png'), size=(31, 22))
        self.repeat_image = customtkinter.CTkImage(Image.open('Images/Repeat.png'), size=(31, 22))

        # Album Art Image
        self.album_art_label = customtkinter.CTkLabel(master=self, text='', image=self.album_image)
        self.album_art_label.grid(row=1, column=0, columnspan=5, pady=(25, 5))

        # Track Information
        self.track_info = TrackInformation(master=self, width=350, height=25, orientation='horizontal')
        self.track_info.grid(row=2, column=0, columnspan=5)

        # Track Slider
        self.slider = customtkinter.CTkSlider(master=self, from_=0, to=100, width=400, progress_color='purple')
        self.slider.grid(row=3, column=0, columnspan=5)
        self.slider.set(0)

        # Track elapsed time, track information, track length
        self.track_time = customtkinter.CTkLabel(master=self, text='0:00')
        self.track_length = customtkinter.CTkLabel(master=self, text='0:00')
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

        self.start_next_track()
        self.track_slide()

    def play_pause_button(self):
        """
        Function for pausing and unpausing the track when the play/pause button is pressed, this also changes the button
        image accordingly.

        :return: None
        """
        if self.play_button.cget('image') == self.play_image:
            self.play_button.configure(image=self.pause_image, text='', height=60, width=60)
            pygame.mixer.music.unpause()
            self.current_time()
        else:
            self.play_button.configure(image=self.play_image, text='', height=60, width=60)
            pygame.mixer.music.pause()

    def current_time(self):
        """
        Function for updating the current time location in the track for the UI time and slider

        :return: None
        """
        # Stop any unnecessary calls to the function
        if self.after_current_time_id is not None:
            self.after_cancel(self.after_current_time_id)
            self.after_current_time_id = None
        # get the current position of the track in milliseconds and format it to something more readable
        self.track_position = self.track_position + 1
        self.slider.set(int(self.track_position))
        formatted_time = f'{int(self.track_position//60)}:{int(self.track_position%60):02d}'
        self.track_time.configure(text=formatted_time)
        # continue tracking the time as long as the track is playing
        if self.play_button.cget('image') == self.pause_image:
            self.after_current_time_id = self.after(1000, self.current_time)

    def track_slide(self):
        """
        Function for moving the position of the track by moving the position of the track slider. This allows for the
        user to adjust the point in the track at which playback is happening.

        :return: None
        """
        # Stop any unnecessary calls to the function
        if self.after_track_slide_id is not None:
            self.after_cancel(self.after_track_slide_id)
            self.after_track_slide_id = None
        # When the track is playing if the slider position is different from the position of the song move to that position in the track.
        if self.play_button.cget('image') == self.pause_image:
            if self.slider.get() != int(self.track_position):
                pygame.mixer.music.set_pos(self.slider.get())
                self.track_position = self.slider.get()
                self.slider.set(self.track_position)
        self.after_track_slide_id = self.after(1000, self.track_slide)

    def start_next_track(self):
        """
        Function to monitor when a track ends and start the next track in a playlist
        :return: None
        """
        # Stop any unnecessary calls to the function
        if self.after_start_next_track_id is not None:
            self.after_cancel(self.after_start_next_track_id)
            self.after_start_next_track_id = None
        # if the get position is at the end of the song call
        for event in pygame.event.get():
            if event.type == self.MUSIC_END:
                self.current_track_playing()
                pygame.mixer.music.unpause()
        self.after_start_next_track_id = self.after(1000, self.start_next_track)

    def open_playlists(self):
        """
        function that opens the playlists window when the playlist button is pressed

        :return: None
        """
        if self.playlist_window is None or not self.playlist_window.winfo_exists():
            self.playlist_window = PlaylistsUI.Playlists(self.queue_playlist)
            self.playlist_window.after(20, self.playlist_window.lift)
        else:
            self.playlist_window.focus()

    def queue_playlist(self, playlist):
        """
        Function for transitioning playlist from playlist window to main player and queuing up the playlist for
        playback.

        :param playlist: The name of the playlist to find and queue up for playback

        :return: None
        """
        # get the name of the folder for the playlist
        playlists_folder_path = 'D:/OSU Spring 2023/CS 361 Software Development/Assignments/Assignment-5/Playlists'
        queue_playlist_path = playlists_folder_path + '/' + playlist
        # put the tracks in an array
        with os.scandir(queue_playlist_path) as playlist_tracks:
            for track in playlist_tracks:
                if track.is_file():
                    self.queued_tracks.append(track)
        self.current_playlist = playlist
        self.current_track_playing()

    def current_track_playing(self):
        """
        Function to facilitate the playing of songs from playlist in the main player.
        :return:
        """
        # get the song from the playlist array, check if end of the playlist, stop if so otherwise play next track
        if self.track_number_playing >= len(self.queued_tracks):
            self.end_playlist()
            return
        current_track = self.queued_tracks[self.track_number_playing]
        metadata = TinyTag.get(current_track, image=True)
        self.track_number_playing += 1

        # Send track file path to microservice to get the metadata then retrieve it and store it for display
        playlists_folder_path = 'D:/OSU Spring 2023/CS 361 Software Development/Assignments/Assignment-5/Playlists'
        socket.send_pyobj(playlists_folder_path + '/' + self.current_playlist + '/' + current_track.name)
        track_title, track_album, track_artist, track_number = socket.recv_pyobj()

        # update the music mixer
        pygame.mixer.music.load(current_track)
        pygame.mixer.music.play()
        pygame.mixer.music.pause()

        # update the UI
        self.slider.configure(number_of_steps=int(metadata.duration), to=int(metadata.duration))
        self.track_position = 0
        self.slider.set(self.track_position)
        self.track_info.update_information(track_title, track_artist, track_album, track_number)
        self.track_time.configure(text=f'0:00')
        self.track_length.configure(text=f'{int(metadata.duration//60)}:{int(metadata.duration%60):2d}')

    def end_playlist(self):
        # update the UI
        self.play_button.configure(image=self.play_image, text='', height=60, width=60)
        pygame.mixer.music.pause()
        self.slider.configure(number_of_steps=100)
        self.track_position = 0
        self.slider.set(self.track_position)
        self.track_info.update_information(track_title='none', track_artist='none', track_album='none', track_number='none')
        self.track_time.configure(text=f'0:00')
        self.track_length.configure(text=f'0:00')



if __name__ == "__main__":
    app = Player()
    app.mainloop()



