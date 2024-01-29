from sqlalchemy import create_engine, text
import argparse
import uuid
import maskpass
from werkzeug.security import generate_password_hash
import os.path

from variantbrowser.backend import app, db_user
from variantbrowser.backend.user import Users

from variantbrowser.db.dbutils import get_config, generate_db,  generate_user_db

config = get_config()

def remove_sample():

    parser = argparse.ArgumentParser()
    parser.add_argument("-S", metavar="Sample ID", required=True, nargs=1,  help="The ID of the sample which should be unapproved and unsigned.")
    args = parser.parse_args()

    db = config['Paths']['db_full_path']

    engine = create_engine("sqlite:///"+db, echo=False, future=True)

    stmt = f"DELETE FROM Samples WHERE sampleid = '{args.S}';"
    stmt2 = f"DELETE FROM VariantsPerSample WHERE sampleid = '{args.S}';"

    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        result2 = conn.execute(text(stmt2))
        conn.commit()


def unapprove_sample():
    # Beware that samples that get unapproved and unsigned will automatically get newer classifications.

    parser = argparse.ArgumentParser()
    parser.add_argument("-S", metavar="Sample ID", required=True, nargs=1, help="The ID of the sample which should be unapproved and unsigned.")
    args = parser.parse_args()

    db = config['Paths']['db_full_path']

    engine = create_engine("sqlite:///"+db, echo=False, future=True)

    stmt = f"""UPDATE Samples set 
        User_Signoff = '', Date_Signoff = '',
        User_Approval = '', Date_Approval = '',
        User_Lock = '', Date_Lock = '',
        Status = '' 
        WHERE sampleid = '{args.S}';
        """

    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        conn.commit()

def add_user():

    def add_user_internal(db):

        name = input("\nEnter a new user name: ")
        
        user = Users.query.filter_by(name=name).first()

        if user is not None:
            print("User name already taken!")
            return False

        new_password = maskpass.askpass("\nEnter password: ")

        if (len(new_password) < 5):
            print("Too short, minumim five characters!")
            return False
        
        new_password_2 = maskpass.askpass("Enter it again: ")


        if new_password != new_password_2:
            print("\n---------Not equal, try again---------")
            return False

        hashed_password = generate_password_hash(new_password, method='scrypt')

        admin = bool(input("\nShould the user be an admin? (True or False) (Also, does not actually make a difference.) "))

        db.session.add(Users(public_id=str(uuid.uuid4()), name=name, password=hashed_password, admin=admin))

        db.session.commit()
        print("\n-----User added successfully!-----\n")
        return True

 
    print("\n-----------Add New User------------")
    with app.app_context():
        while(not add_user_internal(db_user)):
            pass


def change_pwd():

    def change_pwd_internal(db):

        user = Users.query.filter_by(name=input("\nEnter username: ")).first()

        if user is None:
            print("User not found!")
            return False

        new_password = maskpass.askpass("\nEnter new password: ")

        if (len(new_password) < 5):
            print("Too short, minumim five characters!")
            return False
        
        new_password_2 = maskpass.askpass("Enter it again: ")


        if new_password == new_password_2:
            hashed_password = generate_password_hash(new_password, method='scrypt')
            user.set_pwd(hashed_password)
            db.session.commit()
            print("\n----Password changed successfully!----\n")
            return True

        else:
            print("\n---------Not equal, try again---------")
            return False
        

    print("\n-----------Change password------------")
    with app.app_context():
        while(not change_pwd_internal(db_user)):
            pass

def generate_dbs():
    
    # If exists, do not create.
    
    db_path = config['Paths']['db_full_path']
    user_db_path = config['Paths']['db_users']

    if not os.path.isfile(db_path):
        generate_db(db_path)
        print("Variant DB created at: " + db_path)
    else:
        print("The variant db already exists. Delete or rename then run again.")

    if not os.path.isfile(user_db_path):
        generate_user_db(user_db_path)
        print("User DB created at: " + user_db_path)
    else:
        print("The user db already exists. Delete or rename then run again.")

    

