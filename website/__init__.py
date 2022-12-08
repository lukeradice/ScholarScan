#importing Flask object, allows for creation of app
from flask import Flask
#importing SQLAlchemy so I can create my database
from flask_sqlalchemy import SQLAlchemy
from os import path
from scholarly import scholarly, ProxyGenerator 


db = SQLAlchemy()
#Initialising database and assigning name
DB_NAME = "studystronghold.db"


def create_app():
    app = Flask(__name__)
    #secret key is used to encrypt session/cookies data
    app.config['SECRET_KEY'] = 'b\\xf6;B\\xef\\xda-e\\x08%q\\xfe\\xe5\\xc4,i\\t\\xf5\\x87<E\\x9d\\x9a\\xdf\\xb6'
    #stores the database in the webiste folder
    #f string allows DB_NAME to be evaluated as a string
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #this links the app with the database
    db.init_app(app)
    pg = ProxyGenerator() 
    scholarly.use_proxy(pg)
    success = pg.ScraperAPI('f171d0c5dd2ec4eb81c87ab25875fdd9')
    if success:
        print("successful proxy connection")


    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .models import Study, Government, AuthorStudyLink, Author, Organisation, Journal
    create_database(app)

    return app


#classes/entities for db will have been defined at this point
#database is created if it doesn't exist, we pass app to make sure the 
#software knows what the associated software is
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
        from .models import Government
        #allows the adding of the domains to the database outside of a view function, a flask sql_alchemy requirement
        with app.app_context():
            myfile = open("correspondingdomain.txt", "r")
            myline = myfile.readline()
            while myline:
                pair = myline.split(",")
                correspondingDomain = pair[0].strip()
                government = pair[1].strip()
                new_government = Government(government=government, correspondingDomain=correspondingDomain)
                db.session.add(new_government)
                db.session.commit()
                myline = myfile.readline()
            myfile.close()  
        print('Created Database!')
