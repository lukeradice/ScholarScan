#importing Flask object, allows for creation of app
from flask import Flask
#importing SQLAlchemy so I can create my database
from flask_sqlalchemy import SQLAlchemy
from os import path
from scholarly import scholarly, ProxyGenerator 
from datetime import datetime, date
import csv
import requests

db = SQLAlchemy()
#Initialising database and assigning name
DB_NAME = "studystronghold.db"
#define the proxies I'll be using to do my own beautiful soup scraping, used in search and here briefly
myProxies = {"http": "http://scraperapi:556657541da89a70985be0bd8e9874d1@proxy-server.scraperapi.com:8001",
            "https": "http://scraperapi:556657541da89a70985be0bd8e9874d1@proxy-server.scraperapi.com:8001"}

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
    success = pg.ScraperAPI('556657541da89a70985be0bd8e9874d1')
    # success = pg.ScraperAPI('d1318296d4d6fc658b1e373287da15fe')
    #success = pg.ScraperAPI('ffe4db9384d81641640ddb6976087dae')
    #success = pg.ScraperAPI('57465d56ed88087e0fd9239e56ace84b')
    #success = pg.ScraperAPI('d07eb644f66c41a5ebf97168156dc1d5')
    #success = pg.ScraperAPI('f171d0c5dd2ec4eb81c87ab25875fdd9')
    if success:
        print("successful proxy connection")

    #registering the views blueprint with the app, so the app has access to the view functions
    #which determines what ports it will listen to for inputs
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .models import Study, Government, AuthorStudyLink, Author, Organisation, Journal, Feedback, Journals, lastUpdates
    #creation of database and linking it with the app
    create_database(app)

    #calling of function to update the journal table if it hasn't been updated in a year
    # with app.app_context():
    #     #try except is for the state where the database doesn't exist yet
    #     try:
            # lastJournalUpdate = lastUpdates.query.all()[0].lastJournalUpdate
            # todaysDate = date.today()
            # if todaysDate.days - lastJournalUpdate.days > 365:
            #     updateJournalinformation(todaysDate)
        # except IndexError:
        #     pass

    return app

#classes/entities for db will have been defined at this point
#database is created if it doesn't exist, we pass app to make sure the 
#software knows what the associated software is
def create_database(app):
    from .models import Government, Journals, lastUpdates
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
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

            #url for the csv containing sjr data for scholarly journals
            #this url should be the same every year so don't need to scrape it
            journalUrl ="https://www.scimagojr.com/journalrank.php?out=xls"

            #the url variable only stores the download link for the csv file so have to use requests to get the info
            #requests.Session provides cookie persistence which is useful when scraping
            with requests.Session() as s:
                #get request for the download url
                download = s.get(journalUrl, proxies=myProxies, verify=False)
                #defines the lines of the csv file as being character set utf-8 and puts them as a unique
                #item in the list
                lines = (line.decode('utf-8') for line in download.iter_lines())

            #interpretation of csv data, delimiter is what separates each element and quotechar links elements
            #that are only linked by speech marks
            journalData = csv.reader(lines, delimiter=';', quotechar='"')
            i = 0
            # test = True
            for row in journalData:
                #the use of variable is to ensure the top row isn't scraped as that is the headers
                #so will cause an error trying to convert those strings to integers
                if i != 0:
                    #the extraction of the csv row values that I will store for each Journals record
                    title = row[2]
                    issns = row[4]
                    sjrScore = int(row[5].replace(",","") or "0")
                    journalHIndex = int(row[7])
                    publisher = row[17]

                    newJournals = Journals(journalTitle=title, issns=issns, sjrScore=sjrScore, journalHIndex=journalHIndex, 
                                            publisherName=publisher)
                    db.session.add(newJournals)
                    db.session.commit()

                    # print(title)
                    # print(issns)
                    # print(sjrScore)
                    # print(journalHIndex)
                    # print(government)
                    # print(publisher)
                    # print()
                # elif i == 5:
                    # test = False
                i = i + 1
            #saving the date the dynamic sjr information was added to the database so it can be checked and updated if past a year
            lastJournalUpdate = date.today()
            newJournalUpdate = lastUpdates(lastJournalUpdate=lastJournalUpdate)
            db.session.add(newJournalUpdate)
            db.session.commit()
            print(Journals.query.all())
        print('Created Database!')
    else:
        with app.app_context():
            lastJournalUpdate = lastUpdates.query.all()[0].lastJournalUpdate
            todaysDate = date.today()
            if (todaysDate - lastJournalUpdate).days > 365:
                updateJournalinformation(todaysDate)

def updateJournalinformation(todaysDate):
    from .models import Government, Journals, lastUpdates
    #url for the csv containing sjr data for scholarly journals
    #this url should be the same every year so don't need to scrape it
    journalUrl ="https://www.scimagojr.com/journalrank.php?out=xls"

    #the url variable only stores the download link for the csv file so have to use requests to get the info
    #requests.Session provides cookie persistence which is useful when scraping
    with requests.Session() as s:
        #get request for the download url
        download = s.get(journalUrl, proxies=myProxies, verify=False)
        #defines the lines of the csv file as being character set utf-8 and puts them as a unique
        #item in the list
        lines = (line.decode('utf-8') for line in download.iter_lines())

    #interpretation of csv data, delimiter is what separates each element and quotechar links elements
    #that are only linked by speech marks
    journalData = csv.reader(lines, delimiter=';', quotechar='"')
    i = 0
    for row in journalData:
        #the use of variable is to ensure the top row isn't scraped as that is the headers
        #so will cause an error trying to convert those strings to integers
        if i != 0:
            #the extraction of the csv row values that I will store for each Journals record
            title = row[2]
            journalToUpdate = db.session.query(Journals).filter(Journals.journalTitle==title)
            journalToUpdate.sjrScore = int(row[5].replace(",","") or "0")
            journalToUpdate.journalHIndex = int(row[7])
            db.session.commit()
        i = i + 1
    #saving the date the dynamic sjr information was added to the database so it can be checked and updated if past a year
    newJournalUpdate = lastUpdates(lastJournalUpdate=todaysDate)
    db.session.add(newJournalUpdate)
    db.session.commit()
    print(Journals.query.all())
