import os
from utils import file_utils, regexes, screen_utils

home_dir: str
files_path: str
editee_files: str

try:
  home_dir = os.path.expanduser("~")
  files_path = os.path.join(home_dir, "editee")
  editee_files = os.listdir(files_path)
except Exception as e:
  print(f"An error has occurred while trying to set directories. {e}")

def deletefile():
  files: list[str] = file_utils.list_files()
  selected_file: str = ""
  selected_file_index: int
  selected_file_path: str
  has_selected_file: bool = False

  if not files:
    print("No files found in editee directory.")
    return

  print('Select the file you want to edit:')

  file_utils.loop_files(files)

  while has_selected_file is not True:
    selected_file = str(input()).strip().lower()

    if regexes.contains_non_numeric_char(selected_file) or regexes.is_whitespace(selected_file) or len(selected_file) == 0:
      print("Please, select the file by inserting the number that corresponds to its index.")
      file_utils.loop_files(files)
    else:
      has_selected_file = True

  selected_file_index: int = int(selected_file)
  selected_file_path = os.path.join(files_path, files[selected_file_index])

  screen_utils.clear_sc()
  print(f"Deleting selected file: {files[selected_file_index]}")

  try:
    if os.path.exists(selected_file_path):
      os.remove(selected_file_path)
      print('Successfully deleted file!')
  except FileNotFoundError:
    print(f"The file {files[selected_file_index]} cannot be found.")
  except Exception as e:
    print(f"An error has occurred! {e}")

