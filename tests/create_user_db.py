from backend import db_user as db
from variantbrowser.backend.user import Users
import uuid
from werkzeug.security import generate_password_hash

''' 
Lager bruker-databasen og legger til en eksempelbruker.

'''

# Create db
db.drop_all()
db.create_all()

# Populate
hashed_password = generate_password_hash('buso123', method='sha256')
db.session.add(Users(public_id=str(uuid.uuid4()), name='buso', password=hashed_password, admin=True))

hashed_password = generate_password_hash('strali123', method='sha256')
db.session.add(Users(public_id=str(uuid.uuid4()), name='strali', password=hashed_password, admin=True))

hashed_password = generate_password_hash('mfahl123', method='sha256')
db.session.add(Users(public_id=str(uuid.uuid4()), name='mfahl', password=hashed_password, admin=True))

hashed_password = generate_password_hash('sigve123', method='sha256')
db.session.add(Users(public_id=str(uuid.uuid4()), name='sigvla', password=hashed_password, admin=True))

db.session.commit()

