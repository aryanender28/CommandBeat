import pygame #for the music playing
import os # clear screen 
import sys # for exit 
import time # for duration counting 
import random # for shuffle option   
import msvcrt # for reading the key press from keyboard
import shutil # for moving the file to our directory 
from tkinter import filedialog, Tk #for opening file dialog

pygame.init()
pygame.mixer.init()

# Constants for volume adjustments
VOLUME_INCREMENT = 0.1
MIN_VOLUME = 0.0
MAX_VOLUME = 1.0

last_shuffled_song = None  # Global variable to store the last shuffled song

def select_song():
    print("Select an option:")
    print("1. Select from Playlist")
    print("2. Add Song to Playlist")
    print("3. Delete Song From Playlist")
    print("4. Shuffle Song From Playlist")
    print("5. Exit Player")
    
    choice = input("Enter the number of the option you want: ")
    if choice == "1":
        clear_screen()
        return select_from_playlist()
    elif choice == "2":
        clear_screen()
        return add_song_to_playlist()
    elif choice == "3":
        clear_screen()
        delete_song_from_playlist()
        return select_song()
    elif choice == "4":
        return shuffle_song_from_playlist()
    elif choice == "5":
        sys.exit()
    else:
        print("Invalid option Select the right Song!")

def select_from_playlist():
    available_songs = get_available_songs()
    print("Select a song:")
    for index, song in enumerate(available_songs, start=1):
        print(f"{index}. {song}")
    song_choice = input("Enter the number of the song you want to play: ")
    try:
        song_choice = int(song_choice)
        if 1 <= song_choice <= len(available_songs):
            return available_songs[song_choice - 1]
        else:
            print("Invalid choice. Defaulting to Tyla.mp3.")
            return "Tyla.mp3"
    except ValueError:
        print("Invalid choice. Defaulting to Tyla.mp3.")
        return "Tyla.mp3"

def add_song_to_playlist():
    root = Tk()
    root.attributes("-topmost", True)  
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    root.destroy()  
    if file_path:
        filename = os.path.basename(file_path)
        destination = os.path.join(os.path.dirname(__file__), "MyPlaylist", filename)
        shutil.copy(file_path, destination)
        return filename
    else:
        print("No file selected. Defaulting to Tyla.mp3.")
        return "Tyla.mp3"
    
def delete_song_from_playlist():
    available_songs = get_available_songs()
    print("Select a song to delete:")
    for index, song in enumerate(available_songs, start=1):
        print(f"{index}. {song}")
    song_choice = input("Enter the number of the song you want to delete: ")
    try:
        song_choice = int(song_choice)
        if 1 <= song_choice <= len(available_songs):
            song_to_delete = available_songs[song_choice - 1]
            os.remove(os.path.join(os.path.dirname(__file__), "MyPlaylist", song_to_delete))
            print(f"{song_to_delete} deleted successfully.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice.")

def shuffle_song_from_playlist():
    global last_shuffled_song  
    available_songs = get_available_songs()
    if last_shuffled_song in available_songs:
        available_songs.remove(last_shuffled_song)
    random_song = random.choice(available_songs)
    last_shuffled_song = random_song  
    print(f"Shuffling and playing random song: {random_song}")
    return random_song

def get_available_songs():
    """
    Get a list of available songs in the MyPlaylist folder within the current directory.
    """
    playlist_dir = os.path.join(os.path.dirname(__file__), "MyPlaylist")
    available_songs = [filename for filename in os.listdir(playlist_dir) if filename.endswith(".mp3")]
    return available_songs

def play_music(file):
    try:
        # For Loading the music file
        pygame.mixer.music.load(file)  
        pygame.mixer.music.play()    
        print("Welcome To Vp Player:")
        print("Music playing...")
        instruct()
        
        # Get the duration of the song
        song_info = pygame.mixer.Sound(file)
        duration_in_seconds = song_info.get_length()
        total_duration = format_time(duration_in_seconds)

        paused = False  
        volume_level = 0.5 
        pygame.mixer.music.set_volume(volume_level)  
        
        #For updating song duration in runtime
        while True:
            if not paused:
                current_time = pygame.mixer.music.get_pos() / 1000
                current_position = format_time(current_time)
                print(f"\rDuration: {current_position}/{total_duration}", end='')

            time.sleep(1)  
            
            # Check if a key is pressed
            if msvcrt.kbhit():
                user_input = msvcrt.getch().decode().lower()
                if user_input == 'p':
                    if not paused:
                        pygame.mixer.music.pause()  # Pause the music
                        paused = True
                        clear_screen()
                        instruct()
                        print("\nMusic paused.")
                elif user_input == 'r':
                    if paused:
                        pygame.mixer.music.unpause()  # resume the music
                        paused = False
                        clear_screen()
                        instruct()
                        print("Music resumed.")
                elif user_input == 'q':
                    pygame.mixer.music.stop()  # Stop the music
                    print()
                    print("Music stopped.")
                    return  
                elif user_input == '+': #increase volume
                    volume_level = min(volume_level + VOLUME_INCREMENT, MAX_VOLUME)
                    pygame.mixer.music.set_volume(volume_level)
                    clear_screen()
                    instruct()
                    print(f"\nVolume increased to {int(volume_level * 100)}%")
                elif user_input == '-': #decrease volume
                    volume_level = max(volume_level - VOLUME_INCREMENT, MIN_VOLUME)
                    pygame.mixer.music.set_volume(volume_level)
                    clear_screen()
                    instruct()
                    print(f"\nVolume decreased to {int(volume_level * 100)}%")

    except pygame.error as e:
        print("Error loading music:", e)

def format_time(duration):
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    return f"{minutes}:{seconds:02d}"
# just a function for clearing the terminal
def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
#instruction of player
def instruct():
    """
    For Instructions
    """
    print("Press 'p' to pause, 'r' to resume, '+' to increase volume, '-' to decrease volume, or 'q' to quit.")    

# Main loop for selecting and playing music
while True:
    current_dir = os.path.join(os.path.dirname(__file__), "MyPlaylist")
    choice = select_song()
    if choice == "4":
        file_path = os.path.join(current_dir, shuffle_song_from_playlist())
    else:
        file_path = os.path.join(current_dir, choice)
    play_music(file_path)
