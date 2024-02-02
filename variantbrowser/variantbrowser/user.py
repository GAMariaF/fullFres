#from variantbrowser.__init__ import db_user as db

from variantbrowser.userdb import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return "User({}, {})".format(self.name, self.password)
    
    def set_pwd(self, new_password):
        self.password = new_password
        