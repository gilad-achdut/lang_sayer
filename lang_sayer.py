import keyboard
import ctypes
import time
import threading
from win32com.client import Dispatch
import pythoncom
import argparse
import logging

# Constants
COOLDOWN_DURATION = 10  # Cooldown duration in seconds

LANGUAGE_NAMES = {
    0x0409: "English",   # English - United States
    0x040D: "Hebrew",    # Hebrew
    0x041F: "Russian",   # Russian
    0x040C: "French",    # French
    0x0410: "Italian",   # Italian
    0x0411: "Japanese",  # Japanese
    0x0412: "Korean",    # Korean
    0x0416: "Portuguese",# Portuguese
    0x0419: "Russian",   # Russian
    # Add more language IDs and their names as needed
}

class LanguageDetector:
    def __init__(self, debug=False):
        self.debug = debug
        self.current_language = ""
        self.last_key_press_times = [0, 1000]
        self.speak_lock = threading.Lock()
        self.speak_engine = Dispatch("SAPI.SpVoice")

        # Configure logging
        self.logger = logging.getLogger("LanguageDetector")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def speak_language(self, language):
        current_time = time.time()
        if self.current_language != language or self.last_key_press_times[1] - self.last_key_press_times[0] >= COOLDOWN_DURATION:
            self.current_language = language
            try:
                pythoncom.CoInitialize()
                with self.speak_lock:
                    self.speak_engine.Speak(language)
                self.logger.debug(f"Speaking language: {language}")
            except Exception as e:
                self.logger.error(f"Error while speaking: {e}")

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
            
            language_display = self.get_keyboard_layout_language()
            self.speak_language(language_display)
            self.logger.debug(f"Detected language: {language_display}")

    def start(self):
        self.logger.debug("Language detector started")
        keyboard.hook(self.key_event)
        keyboard.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Language Detector")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    detector = LanguageDetector(debug=args.debug)
    detector.start()
