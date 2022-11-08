#importing Flask object, allows for creation of app
from flask import Flask
#importing SQLAlchemy so I can create my database
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
#Initialising database and assigning name
DB_NAME = "StudyStronghold.db"


def create_app():
    app = Flask(__name__)
    #secret key is used to encrypt session/cookies data
    app.config['SECRET_KEY'] = 'b\\xf6;B\\xef\\xda-e\\x08%q\\xfe\\xe5\\xc4,i\\t\\xf5\\x87<E\\x9d\\x9a\\xdf\\xb6'
    

    #stores the database in the webiste folder
    #f string allows DB_NAME to be evaluated as a string
    app.config['SQLCLECHMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    #this links the app with the database
    db.init_app(app)


    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app


