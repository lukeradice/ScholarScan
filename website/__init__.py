from flask import Flask
#importing Flask object, allows for creation of app
from flask_sqlalchemy import SQLAlchemy
#importing SQLAlchemy so I can create my database

db = SQLAlchemy()
#creating database object
DB_NAME = "StudyStronghold.db"
#Initialising database and assigning name

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b\\xf6;B\\xef\\xda-e\\x08%q\\xfe\\xe5\\xc4,i\\t\\xf5\\x87<E\\x9d\\x9a\\xdf\\xb6'
    #secret key is used to encrypt session/cookies data

    app.config['SQLCLECHMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #stores the database in the webiste folder
    #f string allows DB_NAME to be evaluated as a string
    db.init_app(app)
    #this links the app with the database