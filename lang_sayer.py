import keyboard
import ctypes
import time
import threading
from win32com.client import Dispatch
import pythoncom
import argparse

# Constants
COOLDOWN_DURATION = 10  # Cooldown duration in seconds

LANGUAGE_NAMES = {
    0x0409: "English",   # English - United States
    0x040D: "Hebrew",    # Hebrew
    # Add more language IDs and their names as needed
}

class LanguageDetector:
    def __init__(self, debug=False):
        self.debug = debug
        self.current_language = ""
        self.last_key_press_times = [0, 1000]
        self.speak_lock = threading.Lock()
        self.speak_engine = Dispatch("SAPI.SpVoice")

    def debug_print(self, message):
        if self.debug:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [DEBUG] {message}")

    def speak_language(self, language):
        current_time = time.time()
        if self.current_language != language or self.last_key_press_times[1] - self.last_key_press_times[0] >= COOLDOWN_DURATION:
            self.current_language = language
            pythoncom.CoInitialize()
            with self.speak_lock:
                self.speak_engine.Speak(language)
            self.debug_print(f"Speaking language: {language}")

    def get_keyboard_layout_language(self):
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
        layout_id = user32.GetKeyboardLayout(thread_id)
        lang_id = layout_id & 0xFFFF
        return LANGUAGE_NAMES.get(lang_id, "Unknown")

    def key_event(self, event):
        if event.event_type == keyboard.KEY_UP:
            self.last_key_press_times[0] = self.last_key_press_times[1]
            self.last_key_press_times[1] = time.time()
            self.update_history_window(event.name)  # Pass the detected key to the function

    def update_history_window(self, key_name):
        language_display = self.get_keyboard_layout_language()
        self.speak_language(language_display)
        self.debug_print(f"Detected language: {language_display}, Key: {key_name}")  # Include the detected key

    def start(self):
        self.debug_print("Language detector started")
        keyboard.hook(self.key_event)
        keyboard.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Language Detector")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    detector = LanguageDetector(debug=args.debug)
    detector.start()
