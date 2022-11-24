from scholarly import scholarly, ProxyGenerator
from flask import flash
from . import db
from .models import Study, Author, AuthorStudyLink, Government, __repr__, Organisation, Journal
import tldextract
import sqlite3

def search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount):
    #PROCESS ADDING DOMAINS IN DATABASE UPON DATABASE RESET
    # myfile = open("correspondingdomain.txt", "r")
    # myline = myfile.readline()
    # while myline:
    #     pair = myline.split(",")
    #     correspondingDomain = pair[0].strip()
    #     government = pair[1].strip()
    #     new_government = Government(government=government, correspondingDomain=correspondingDomain)
    #     db.session.add(new_government)
    #     db.session.commit()
    #     myline = myfile.readline()
    # myfile.close()   
    searchIterations = 1
    if resultAmount > searchIterations:
         searchIterations = resultAmount
    pg = ProxyGenerator()
    #success = pg.FreeProxies()
    success = pg.ScraperAPI('f171d0c5dd2ec4eb81c87ab25875fdd9')
    scholarly.use_proxy(pg)
    if success:
        print("success")
        studies = scholarly.search_pubs(str(searchQuery))
        for i in range (0, searchIterations):
            study = next(studies)
            if study:
                print("!")
                print(study)
                print("!")
                #adding information for study entity
                #first checks if it already exists within the database
                title = study.get('bib').get('title')
                if studyExists(title) == False:
                    abstract = study.get('bib').get('abstract')
                    print('abstract', abstract)
                    governmentAffiliation = attributeHandler.governmentAffiliatior(study.get('pub_url'))
                    levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                    print('levelofaffiliation', levelOfAffiliation)
                    government_id = governmentAffiliation.government_id
                    print('governmentid', government_id)

                    #adding the details of the journal and checking to see if info on it is already stored in the database
                    journal = study.get('bib').get('venue')
                    print('journal', journal)
                    if journalExists(journal) == False:
                        new_journal = Journal(journalName=journal)
                        db.session.add(new_journal)
                        db.session.commit()
                    journal_id = db.session.query(Journal.id).filter(journalName=journal).first()

                    #back to finishing adding of Study entity details
                    new_study = Study(SearchDepth=searchIterations, governmentAffiliation=levelOfAffiliation, title=title, abstract=abstract, government_id=government_id, journal_id=journal_id)
                    db.session.add(new_study)
                    db.session.commit()

                    #setting up ID to establish link table relationship between Study and Author entries
                    studyID = db.session.query(Study.id).filter_by(title=title).first()
                    
                    #adding information for author entity
                    #first checks if it already exists within the database
                    authorScholarIDs = study.get('author_id')
                    for i in authorScholarIDs:
                        author_query = scholarly.search_author_id(i)
                        author = scholarly.fill(author_query, sections=['basics', 'indices', 'counts'])
                        authorName = author.get('name')
                        if authorExists(authorName) == False:  
                            authorCitations = author.get('citedby')

                            #adding information about each author's main organisation to the organisation entity, this effects an author's scoring
                            #first checks if it already exists within the database
                            orgName = author.get('affiliation')
                            if organisationExists(orgName) == False:
                                scholar_id = author.get('organization')
                                new_org = Organisation(scholar_id=scholar_id, orgName=orgName)
                                db.session.add(new_org)
                                db.session.commit()
                            organisation_id = db.session.query(Organisation.id).filter_by(orgName=orgName).first()
                            new_author = Author(authorName=authorName, authorCitations=authorCitations, organisation_id=organisation_id)
                            db.session.add(new_author)
                            db.session.commit()
                        #submitting link table entry
                        #may need a more reliable secondary index than author name, author names could be shared, alternatively I could just set more attributes in the criteria
                        authorID = db.session.query(Author.id).filter_by(authorName=authorName).first()
                        new_authorStudyLink = AuthorStudyLink(author_id=authorID, study_id=studyID)
                        db.session.add(new_authorStudyLink)
                        db.session.commit()
                        
                        
                    print("Author added, number ", i)
            i = i + 1

class attributeHandler():
    def __init__(self) -> None:
        pass
    #handling government affiliation, only considered fully affiliated with .gov in domain
    #it is 50/50 with .ac and .edu as some education facilities are private
    def governmentAffiliatior(domain):
        suffix = tldextract.extract(domain).suffix
        suffix = '.' + suffix
        print('suffix', suffix)
        countryToFind = Government.query.filter(Government.correspondingDomain == suffix).one()
        print(countryToFind.id)
        if 'edu' in suffix or 'ac' in suffix:
            return governmentAffiliationResponse(50, countryToFind.id)
        elif '.gov' in suffix:
            return governmentAffiliationResponse(100, countryToFind.id)
        else:
            return governmentAffiliationResponse(0, countryToFind.id)

#used to return two items for the governmentAffiliation method of attributeHandler object
class governmentAffiliationResponse():
    def __init__(self, levelOfAffiliation, government_id=None):
        self.levelOfAffiliation = levelOfAffiliation 
        self.government_id = government_id 


            #SELECT government.id FROM Government WHERE correspondingDomain = domain
            #db.session.execute(db.select(Government).filter_by(correspondingDomain=suffix)).scalars()


def studyExists(title):
    #need the try except statement for when the database doesn't exist yet so it can't check for it
    try:
        exists = db.session.query(Study.title).filter_by(title=title).first()
        if exists:
            return True
        else:
            return False
    except sqlite3.OperationalError:
        return False

def authorExists(name):
    try:
        exists = db.session.query(Author.authorName).filter_by(authorName=name).first()
        if exists:
            return True
        else:
            return False
    except sqlite3.OperationalError:
        return False

def organisationExists(orgName):
    try:
        exists = db.session.query(Organisation.orgName).filter_by(orgName=orgName).first()
        if exists:
            return True
        else:
            return False
    except sqlite3.OperationalError:
        return False
        
def journalExists(journal):
    try:
        exists = db.session.query(Journal.journalName).filter_by(journalName=journal).first()
        if exists:
            return True
        else:
            return False
    except sqlite3.OperationalError:
        return False

        

        