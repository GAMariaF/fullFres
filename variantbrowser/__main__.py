import argparse
import logging
from . import db


def get_options():

    parser = argparse.ArgumentParser(description='Version: 0.0.1')
    parser.add_argument('program', nargs=1,
                        help='Select a program to run')

    args = parser.parse_args()

    return args


def main():

#    args = get_options()
#    
#    match args.program[0]:
#        case 'removesample':
#            db.remove_sample
#        case 'unlocksample':
#            db.unlock_sample
#        case 'adduser':
#            db.add_user
#        case 'changepwd':
#            db.change_pwd
#        case 'generatedbs':
#            db.generate_dbs
#        case _:
#            print("Not found")

    #if None in [args.adduser]:
    #    logging.error('ERROR in arguments')
    #    exit()
    
    print("""
    Uses:
          
    removesample: Delete a sample from the variant database.
          
    unlocksample: Unlock a locked sample. It is sent back to the initial interpretation stage.
          
    adduser: Add new user to user database.
          
    changepwd: Change password for user. Existing password not needed.
          
    generatedbs: Generate empty variant and user databases.
    
    """)
    exit()

    


if __name__ == '__main__':
    main()