import time
import sys

def prompt_filename():
    try:
        filename: str = input('Please, enter the file name: ').lower().strip()

        if not filename:
            print("Error: Filename cannot be empty.")
            return None

        print(f"Using filename: {filename}")
        return filename

    except Exception as e:
        print(f"An error occurred while getting the filename: {e}")
        return None

def createfile():
    try:
        filename: str = prompt_filename()

        if filename is None:
            print("File creation cancelled.")
            
            return

        print('Opening file for edition...')
        
        time.sleep(2)

        with open(filename, 'w', encoding='utf-8') as new_file:
            print("File opened. Enter text line by line.")
            print("Press Ctrl+D (Unix/macOS) or Ctrl+Z then Enter (Windows) to finish input.")
            
            # Read from standard input line by line until EOF or Ctrl+Q
            try:
                while True:
                    line = sys.stdin.readline()
                    
                    if not line: # Check for EOF (Ctrl+D or Ctrl+Z+Enter)
                        break

                    new_file.write(line) # Write the line (includes newline)
 
            except KeyboardInterrupt: # Handle Ctrl+C
                print("\nInput interrupted (Ctrl+C). File might be incomplete.")

        print(f"Saving and closing file: {filename}")

    # FileNotFoundError is less pretty rare on write mode ('w') unless there are permission issues
    except FileNotFoundError:
        print(f"Error: Could not create or access file '{filename}'. Check permissions.")
    except Exception as e:
        fn = filename if 'filename' in locals() else "unknown"
        print(f"A fatal error occurred during file operation for '{fn}': {e}")
