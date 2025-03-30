import os
import sys
from filehandler import create_file, read_file

def main():
    print("||==================================||======================||=============================||")
    print("||==================================||Welcome to TextEditee!||=============================||")
    print("||==================================||======================||=============================||")
    print("||                                                                                         ||")
    print("|| (w) new file  | (d) delete file   | (c) continue editing | (r) read file  |  (q) quit   ||")
    print("||                                                                                         ||")
    print("||==================================||======================||=============================||")
    print("||==================================||======================||=============================||")
    print("")

    user_selection: str = str(input()).strip().lower()

    match user_selection:
        case 'w':
            create_file.createfile()
        case 'd':
            print('Enter the name of the file to delete:')
            return None
        case 'c':
            print('Select the file you want to continue editing...')
            return None
        case 'r':
            read_file.fileread()
            return None
        case 'q':
            print('Thank you for using TextEditee! Bye.')
            sys.exit()
        case _:
            print('Error parsing user input!')
            return None

while __name__ == '__main__':
    main()

