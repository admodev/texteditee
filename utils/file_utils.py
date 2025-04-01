import os

def list_files():
  try:
    home_dir = os.path.expanduser("~")
    files_path = os.path.join(home_dir, "editee")
    editee_files = os.listdir(files_path)
    
    return editee_files
  except Exception as e:
    print(f"An error has occurred while trying to list files. {e}")
    return []

def loop_files(files: list[str]):
    for i in range(len(files)):
        print(f"{i}: {files[i]}")
