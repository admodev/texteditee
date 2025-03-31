import os
from utils import regexes

home_dir: str
files_path: str
editee_files: str

try:
    home_dir = os.path.expanduser("~")
    files_path = os.path.join(home_dir, "editee")
    editee_files = os.listdir(files_path)
except Exception as e:
  print(f"An error has occured while trying to set directories. {e}")

def list_files():
  try:
    home_dir = os.path.expanduser("~")
    files_path = os.path.join(home_dir, "editee")
    editee_files = os.listdir(files_path)
    
    return editee_files
  except Exception as e:
    print(f"An error has occured while trying to list files. {e}")
    return []

def loop_files(files: list[str]):
  for i in range(len(files)):
    print(f"{i}: {files[i]}")

def fileread():
  files: list[str] = list_files()
  selected_file: str = ""
  selected_file_index: int
  selected_file_path: str
  has_selected_file: bool = False
  
  if not files:
    print("No files found in editee directory.")
    return
  
  print('Select the file you want to read:')
  
  loop_files(files)
        
                
  while has_selected_file is not True:
    selected_file = str(input()).strip().lower()
        
    if regexes.contains_non_numeric_char(selected_file) or regexes.is_whitespace(selected_file) or len(selected_file) == 0:
      print("Please, select the file by inserting the number that corresponds to its index.")
      loop_files(files)
    else:
      has_selected_file = True

  selected_file_index: int = int(selected_file)
  selected_file_path = os.path.join(files_path, files[selected_file_index])
  print(f"Reading selected file: {files[selected_file_index]}")



  try:
      with open(selected_file_path, 'r', encoding='utf-8') as file_to_read:
          file_content: str = file_to_read.read()
          
          print(file_content)
          
          return file_content
  except FileNotFoundError:
      print(f"The file %s cannot be found.", file)
  except Exception as e:
      print(f"An error has occured! %v", e)

