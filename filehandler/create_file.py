from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession
import os, sys

def prompt_filename():
    filename = prompt('Please, enter the file name: ').strip().lower()
    return filename if filename else None

def createfile():
    filename = prompt_filename()
    if filename is None:
        print("Filename cannot be empty. Cancelling.")
        return

    home_dir = os.path.expanduser("~")
    os.makedirs(os.path.join(home_dir, "editee"), exist_ok=True)
    file_path = os.path.join(home_dir, "editee", f"{filename}.edtee")

    session = PromptSession()
    print("Enter text (multiline). Press Ctrl+D (Unix/macOS) or Ctrl+Z+Enter (Windows) to finish.")

    with open(file_path, 'w', encoding='utf-8') as f:
        try:
            while True:
                line = session.prompt('> ')
                f.write(line + '\n')
        except (EOFError, KeyboardInterrupt):
            pass

    print(f"File saved: {file_path}")

