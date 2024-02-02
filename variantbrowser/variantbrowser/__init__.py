from variantbrowser.vb_app import *
from variantbrowser.userdb import db as db_user

app = create_app()

#db_user.app = app
db_user.init_app(app)

#db_user = SQLAlchemy(app)

__all__ = ["routes", "user", "importutils",  "vcfutils", "dbutils", "cmd_functions"]
