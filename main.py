import sys
from filehandler import create_file, delete_file, edit_file, read_file
from utils import screen_utils

def main():
    screen_utils.clear_sc()
    
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
            delete_file.deletefile()
        case 'c':
            edit_file.editfile()
        case 'r':
            read_file.fileread()
        case 'q':
            print('Thank you for using TextEditee! Bye.')
            sys.exit()
        case _:
            print('Error parsing user input!')
            return None

while __name__ == '__main__':
    main()

