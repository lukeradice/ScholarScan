from flask import flash
from . import db
from .models import Study, Author, AuthorStudyLink, Government, __repr__, Organisation, Journal
import tldextract
import sqlite3
from scholarly import scholarly

def search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount):
    # studyDB = Government.query.all()
    # print(studyDB)
    searchedStudies = []
    searchIterations = 1
    if resultAmount > searchIterations:
         searchIterations = resultAmount
    studies = scholarly.search_pubs(str(searchQuery))
    for i in range (0, searchIterations):
        print("iteration", i)
        #this won't run if my api credits have been used up
        study = next(studies)
        print(study)
        if study:
            #adding information for study entity
            #first checks if it already exists within the database
            title = study.get('bib').get('title')
            if not studyExists(title):
                abstract = study.get('bib').get('abstract')
                # governmentAffiliation = attributeHandler.governmentAffiliatior(study.get('pub_url'))
                # levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                governmentFind = attributeHandler()
                governmentAffiliation = governmentFind.governmentAffiliatior(study.get('pub_url'))
                levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                countryToFind = governmentAffiliation.countryToFind
                government_id = governmentAffiliation.government_id

                #adding the details of the journal and checking to see if info on it is already stored in the database
                journal = study.get('bib').get('venue')
                print('journal', journal)
                if not journalExists(journal):
                    new_journal = Journal(journalName=journal)
                    db.session.add(new_journal)
                    db.session.commit()
                    print("journal didn't exist, been added")
                #journal_id = db.session.query(Journal.id).filter_by(journalName=journal).first()
                #print(journal_id)
                journal_id = Journal.query.filter_by(journalName=journal).first()
                #print(journal_id)
                journal_id = journal_id.id
                print("journal_id", journal_id)
                #journal_id = Journal.query.filter_by(journalName=journal).first()


                #back to finishing adding of Study entity details
                new_study = Study(searchDepth=searchIterations, governmentAffiliation=levelOfAffiliation, title=title, abstract=abstract, government_id=government_id, journal_id=journal_id)
                db.session.add(new_study)
                db.session.commit()

                #setting up ID to establish link table relationship between Study and Author entries
                studyID = db.session.query(Study.id).filter_by(title=title).first()
                
                #adding information for author entity
                #first checks if it already exists within the database
                print(study.get('bib').get('author'))
                authorScholarIDs = study.get('author_id')
                authors = study.get('bib').get('author')
                print("list of author ids", authorScholarIDs)
                print("list of authors", authors)
                #NEED TO CONSIDER WHEN THERE IS A BLANK SCRAPE AS PROCESSING IS INVOLVED
                authorOrgUpdate = attributeHandler()
                authorOrgUpdate.authorOrgUpdater(authorScholarIDs, authors)
                    
                #submitting link table entry
                #may need a more reliable secondary index than author name, author names could be shared, alternatively I could just set more attributes in the criteria
                for author in authors:
                    authorID = db.session.query(Author.id).filter_by(authorName=author).first()
                    new_authorStudyLink = AuthorStudyLink(author_id=authorID, study_id=studyID)
                    db.session.add(new_authorStudyLink)
                    db.session.commit()
                
                searchDepth = searchIterations

                
            else:
                print("ALREADY STORED IN DB, FETCHING INFO")
                #getting information about study from the database to input into the searchedStudies list
                fetchedStudy = db.session.query(Study).filter_by(title=title).first()
                title = fetchedStudy.title
                abstract = fetchedStudy.abstract
                levelOfAffiliation = fetchedStudy.governmentAffiliation
                searchDepth = fetchedStudy.searchDepth

                #getting info about the journal by using the foreign key relationship between journal and study
                journal_id = fetchedStudy.journal_id
                associatedJournal = db.session.query(Journal).filter_by(id=journal_id).first()
                journal = associatedJournal.journalName

                #getting info about the authors using the author link table
                study_id = fetchedStudy.id
                associatedLinkedAuthors = db.session.query(AuthorStudyLink).filter_by(study_id=study_id).all()
                authors = []
                for author in associatedLinkedAuthors:
                    associatedAuthorID = author.author_id
                    associatedAuthor = db.session.query(Author).filter_by(id=associatedAuthorID).first()
                    authorName = associatedAuthor.authorName
                    authors.append(authorName)

                government_id = fetchedStudy.government_id
                associatedGovernment = db.session.query(Government).filter_by(id=government_id).first()
                countryToFind = associatedGovernment.government

            print("title", title)
            print("abstract", abstract)
            print('levelofaffiliation', levelOfAffiliation)
            print("search depth", searchDepth)
            print("journal", journal)
            print("authors", authors)
            print("country to find", countryToFind)
            #adding information about the study to searchedStudies list after it has been gathered via scraping or database
            newStudy = SearchResponse(title, abstract, levelOfAffiliation, searchDepth, journal, authors, countryToFind)
            searchedStudies.append(newStudy)
            
            ##
            #IN FUTURE ITERATIONS I MUST CREATE CLASSES TO STORE INFO ABOUT JOURNAL, AUTHORS AND ORGANISATION WHICH OBJECTS WILL BE STORED IN THE STUDY OBJECT THAT WILL 
            #BE PLACED IN THE SEARCHEDSTUDIES LIST
            ##

            print(Study.query.all())
            print(Journal.query.all())
            print(Organisation.query.all())
            print(Author.query.all())
    return searchedStudies

class attributeHandler():
    def __init__(self):
        pass
    #handling government affiliation, only considered fully affiliated with .gov in domain
    #it is 50/50 with .ac and .edu as some education facilities are private
    def governmentAffiliatior(self, domain):
        suffix = tldextract.extract(domain).suffix
        suffix = '.' + suffix
        print('suffix', suffix)
        countryToFind = Government.query.filter(Government.correspondingDomain == suffix).one()
        if 'edu' in suffix or 'ac' in suffix:
            return governmentAffiliationResponse(50, countryToFind, countryToFind.id)
        elif '.gov' in suffix:
            return governmentAffiliationResponse(100, countryToFind, countryToFind.id)
        else:
            return governmentAffiliationResponse(0, countryToFind, countryToFind.id)
    
    def authorOrgUpdater(self, authorScholarIDs, authors):
        #comparing corresponding author and authorID lists, ideally I want to search with authorID because two different authors
        #could share the same name, however some author's don't have an author_id so I would have to search by name in that case,
        #if duplicate names come up in that case then that will reflect poorly on the author in terms of trustworthiness as 
        #getting information about them becomes more difficult
        for a in authors:
            correspondingIndex = authors.index(a)
            correspondingID = authorScholarIDs[correspondingIndex]
            if correspondingID == "":
                authorName_query = scholarly.search_author(a)
                #finding the correct author with just their name, COME BACK TO LATER
                #authorFound = False 
                print("GOING TO TRY SEARCH ", a)
                author_query = next(authorName_query) 
            else:
                author_query = scholarly.search_author_id(correspondingID)

            author = scholarly.fill(author_query, sections=['basics', 'indices', 'counts']) 
            authorName = author.get('name')   
            if not authorExists(authorName):  
                authorCitations = author.get('citedby')

                #adding information about each author's main organisation to the organisation entity, this effects an author's scoring
                #first checks if it already exists within the database
                orgName = author.get('affiliation')
                if not organisationExists(orgName):
                    scholar_id = author.get('organization')
                    new_org = Organisation(scholar_id=scholar_id, orgName=orgName)
                    db.session.add(new_org)
                    db.session.commit()
                organisation_id = db.session.query(Organisation.id).filter_by(orgName=orgName).first()
                new_author = Author(authorName=authorName, authorCitations=authorCitations, organisation_id=organisation_id)
                db.session.add(new_author)
                db.session.commit()
                #NEED TO FIGURE OUT HOW TO RETURN THIS AUTHOR INFORMATION FOR THE WEBPAGE

#used to return two items for the governmentAffiliation method of attributeHandler object
class governmentAffiliationResponse():
    def __init__(self, levelOfAffiliation, countryToFind, government_id=None):
        self.levelOfAffiliation = levelOfAffiliation 
        self.countryToFind = countryToFind
        self.government_id = government_id 
        
            #SELECT government.id FROM Government WHERE correspondingDomain = domain
            #db.session.execute(db.select(Government).filter_by(correspondingDomain=suffix)).scalars()


def studyExists(title):
    #need the try except statement for when the database doesn't exist yet so it can't check for it
    try:
        exists = db.session.query(Study).filter_by(title=title).first()
        return exists
        # if exists:
        #     return True
        # else:
        #     return False
    except sqlite3.OperationalError:
        return False

def authorExists(name):
    try:
        #exists = db.session.query(Author).filter_by(authorName=name).first()
        exists = Author.query.filter_by(authorName=name).first()
        return exists
        # if exists:
        #     return True
        # else:
        #     return False
    except sqlite3.OperationalError:
        return False

def organisationExists(orgName):
    try:
        exists = Organisation.query.filter_by(orgName=orgName).first()
        #exists = db.session.query(Organisation).filter_by(orgName=orgName).first()
        return exists
        # if exists:
        #     return True
        # else:
        #     return False
    except sqlite3.OperationalError:
        return False
        
def journalExists(journal):
    try:
        #exists = db.session.query(Journal).filter_by(journalName=journal).first()
        exists = Journal.query.filter_by(journalName=journal).first()
        return exists
        # if exists:
        #     return True
        # else:
        #     return False
    except sqlite3.OperationalError:
        return False

        
class SearchResponse():
    def __init__(self, title, abstract, levelOfAffiliation, searchDepth, journal, authors, countryToFind):
        self.title = title
        self.abstract = abstract
        self.levelOfAffiliation = levelOfAffiliation
        self.searchDepth = searchDepth
        self.journal = journal
        self.authors = authors
        self.countryToFind = countryToFind

