import sys
import configparser
config = configparser.ConfigParser()
config.read('backend/config.ini')
sys.path.insert(0, config['Paths']['backend_path'])
sys.path.insert(0, config['Paths']['db_path'])

from dbutils import generate_db,  generate_user_db

def main():
    
    db_path = "../db_test/test_empty.db"
    user_db_path = "../db_test/users.db"

    generate_db(db_path)
    generate_user_db(user_db_path)


if __name__ == '__main__':
    main()
