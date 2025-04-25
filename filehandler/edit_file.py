from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import PromptSession
import os
from utils import file_utils, regexes

def editfile():
    files = file_utils.list_files()
    if not files:
        print("No files found.")
        return

    file_utils.loop_files(files)
    index = prompt("Select file index: ").strip()
    if not index.isdigit():
        print("Invalid input.")
        return

    path = os.path.join(os.path.expanduser("~"), "editee", files[int(index)])

    with open(path, 'r+', encoding='utf-8') as f:
        content = f.read()

    new_content = prompt("Editing file (Esc+Enter to save):\n", default=content, multiline=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("File saved.")

