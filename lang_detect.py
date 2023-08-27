import langid
from pynput import keyboard

previous_language = None
current_word = ""

def on_key_release(key):
    global previous_language, current_word
    
    try:
        char = key.char
        current_word += char
    except AttributeError:
        pass

    if key == keyboard.Key.space:  # Compare the key with its string representation
        print(current_word)
        detect_language()
        current_word = ""

def detect_language():
    global previous_language, current_word
    detected_language, _ = langid.classify(current_word)
    
    if previous_language is None:
        previous_language = detected_language
    elif detected_language != previous_language:
        print(f"Warning: Detected language is {detected_language}, expected {previous_language}")
        previous_language = detected_language

def main():
    listener = keyboard.Listener(on_release=on_key_release)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
