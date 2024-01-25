
from dbutils import generate_db,  generate_user_db, get_config

def main():
    
    config = get_config()

    db_path = config['Paths']["db_full_path"]
    user_db_path = config["Paths"]["db_users"]

    generate_db(db_path)
    generate_user_db(user_db_path)


if __name__ == '__main__':
    main()
