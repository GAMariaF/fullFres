from variantbrowser.backend import db_user as db
from variantbrowser.backend.users_db import Users
import uuid
from werkzeug.security import generate_password_hash
import maskpass

def main():

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
    


    
if __name__ == "__main__":

    print("\n-----------Change password------------")

    while(not main()):
        pass
    