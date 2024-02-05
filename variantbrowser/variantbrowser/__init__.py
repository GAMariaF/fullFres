from variantbrowser.vb_app import *
from variantbrowser.userdb import db


db_user = db
app = create_app(db_user)

#db_user.app = app


#db_user = SQLAlchemy(app)

__all__ = ["routes", "user", "importutils",  "vcfutils", "dbutils", "cmd_functions"]
