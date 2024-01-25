from variantbrowser.backend import db_user as db
from variantbrowser.backend.user import Users
import uuid
from werkzeug.security import generate_password_hash
import maskpass

def main():

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

    admin = bool(input("\nShould the user be an admin? (True or False) "))

    db.session.add(Users(public_id=str(uuid.uuid4()), name=name, password=hashed_password, admin=admin))

    db.session.commit()
    print("\n----User added successfully!----\n")
    return True

 

    
if __name__ == "__main__":

    print("\n-----------Add New User------------")

    while(not main()):
        pass