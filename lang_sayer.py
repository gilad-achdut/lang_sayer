import keyboard
import ctypes
import time
import threading
from win32com.client import Dispatch
import pythoncom

# Constants
cooldown_duration = 10  # Cooldown duration in seconds

language_names = {
    0x0409: "English",   # English - United States
    0x040D: "Hebrew",    # Hebrew
    # Add more language IDs and their names as needed
}

last_key_press_time = [0, 1000]

# Initialize global variables
current_language = ""
speak_lock = threading.Lock()
speak_engine = Dispatch("SAPI.SpVoice")

# make a list variable with 2 elements and assign 0 to both
# last_key_press_time = [0, 0]


def speak_language(language):
    global current_language

    current_time = time.time()
    # and current_time - last_key_press_time >= cooldown_duration:
    if current_language != language or last_key_press_time[1]-last_key_press_time[0] >= cooldown_duration:
        current_language = language
        pythoncom.CoInitialize()
        with speak_lock:
            speak_engine.Speak(language)


def get_keyboard_layout_language():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    layout_id = user32.GetKeyboardLayout(thread_id)
    lang_id = layout_id & 0xFFFF
    return language_names.get(lang_id, "Unknown")


def key_event(event):

    if event.event_type == keyboard.KEY_UP:
        last_key_press_time[0] = last_key_press_time[1]
        last_key_press_time[1] = time.time()
        # print(time.time(), threading.current_thread().name)
        update_history_window()


def update_history_window():
    language_display = get_keyboard_layout_language()
    speak_language(language_display)


def main():
    keyboard.hook(key_event)
    keyboard.wait()  # Keeps the script running


if __name__ == "__main__":
    main()
