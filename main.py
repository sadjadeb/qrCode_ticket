from config import *
import sys

if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else 'help'

    if command == 'add_ticket_id':
        agree = input('This will overwrite the file. Are you sure? (y/n) ')
        if agree == 'y':
            from excel_handler import add_ticket_id
            add_ticket_id(INPUT_FILE_PATH)

    elif command == 'run_webserver':
        from webserver import run_server
        run_server()

    elif command == 'help':
        print('Available commands:')
        print('\tadd_ticket_id')
        print('\trun_webserver')
        print('\thelp')
