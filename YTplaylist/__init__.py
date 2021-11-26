from flask import Flask
# from f_colaskrs import CORS
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

#--------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object("YTplaylist.config.Config")

ENV = "dev"
TESTING = True

if ENV == "dev":
    if TESTING:
        app.config.from_object("YTplaylist.config.TestingConfig")
    else:
        app.config.from_object("YTplaylist.config.DevelopmentConfig")
else:
    app.config.from_object("YTplaylist.config.ProductionConfig")

#--------------------------------------------------------------------------------------------

# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

#--------------------------------------------------------------------------------------------    

# CORS(app)

#--------------------------------------------------------------------------------------------

from YTplaylist import routes