# Language Sayer

This script uses the `keyboard` and `win32com` modules to detect the active keyboard layout language and speak it out loud using the Windows Speech API.

## Requirements

- Python 3.x
- `keyboard` module
- `win32com` module

## Usage

1. Run the script using `python lang_sayer.py`.
2. Press any key to detect the active keyboard layout language and speak it out loud.

## Configuration

- `cooldown_duration`: The duration in seconds to wait before speaking the same language again.
- `language_names`: A dictionary of language IDs and their corresponding names. You can add more language IDs and names as needed.

## License

This script is licensed under the MIT License. See the `LICENSE` file for more information.