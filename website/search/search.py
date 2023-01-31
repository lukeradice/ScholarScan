from flask import flash
from website import db
from website.models import Study, Author, AuthorStudyLink, Government, __repr__, Organisation, Journal
import tldextract
import sqlite3
from scholarly import scholarly

dummyStudy1 = {'container_type': 'Publication', 'source': "<PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>", 'bib': {'title': 'Nose picking and nasal carriage of Staphylococcus aureus', 'author': 'Wertheim, Heiman FL and Van Kleef, Menno and Vos, Margreet C and Ott, Alewijn and Verbrugh, Henri A and Fokkens, Wytske', 'pub_year': '2006', 'venue': 'Infection Control & …', 'abstract': 'part of the nose, we considered the habit of nose picking as a  a positive correlation between  nose picking and S. aureus  in a larger cohort with predefined criteria for nose picking.', 
'publisher': 'Cambridge University Press', 'pages': '863--867', 'number': '8', 'volume': '27', 'journal': 'Infection Control \\& Hospital Epidemiology', 'pub_type': 'article', 'bib_id': 'wertheim2006nose'}, 'filled': True, 'gsrank': 1, 'pub_url': 'https://www.cambridge.org/core/journals/infection-control-and-hospital-epidemiology/article/nose-picking-and-nasal-carriage-of-staphylococcus-aureus/DC21FFA771693C772308530D2B1A1452', 'author_id': ['JVFGW64AAAAJ', '', 'RAV-bbIAAAAJ', ''], 'url_scholarbib': '/scholar?hl=en&q=info:KyKH-9mNPpcJ:scholar.google.com/&output=cite&scirp=0&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3Dnose%2Bpicking%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=KyKH-9mNPpcJ&ei=gQ2zY6CMLc6TywSl1LXoCA&json=', 'num_citations': 90, 'citedby_url': '/scholar?cites=10898304115650535979&as_sdt=5,33&sciodt=0,33&hl=en', 'url_related_articles': '/scholar?q=related:KyKH-9mNPpcJ:scholar.google.com/&scioq=nose+picking&hl=en&as_sdt=0,33', 'eprint_url': 'https://www.academia.edu/download/46395935/Nose_picking_and_nasal_carriage_of_Staph20160611-15499-1ngo5wz.pdf'}

dummyStudy2 = {'container_type': 'Publication', 'source': "<PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>", 'bib': {'title': 'A comparison of compensation for release timing and maximum hand speed in recreational and competitive darts players', 'author': 'Burke, D and Yeadon, F', 'pub_year': '2009', 'venue': 'ISBS-Conference Proceedings Archive', 'abstract': 'The level of accuracy achieved by darts players is dependent on their timing capabilities,   a competitive darts player in a throwing task. The inaccuracy of the throws by both players were', 'booktitle': 'ISBS-Conference Proceedings Archive', 'pub_type': 'inproceedings', 'bib_id': 'burke2009comparison'}, 'filled': True, 'gsrank': 1, 'pub_url': 'https://ojs.ub.uni-konstanz.de/cpa/article/view/3166', 'author_id': ['T_nKvbgAAAAJ', ''], 'url_scholarbib': '/scholar?hl=en&q=info:dfry9K19sYUJ:scholar.google.com/&output=cite&scirp=0&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3Ddarts%2Bplayers%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=dfry9K19sYUJ&ei=1xGzY93FO-iSy9YPlIeUiAU&json=', 'num_citations': 11, 'citedby_url': '/scholar?cites=9633619264014580341&as_sdt=5,33&sciodt=0,33&hl=en', 'url_related_articles': '/scholar?q=related:dfry9K19sYUJ:scholar.google.com/&scioq=darts+players&hl=en&as_sdt=0,33', 'eprint_url': 'https://ojs.ub.uni-konstanz.de/cpa/article/download/3166/2970'}

dummyAuthor1 = {'container_type': 'Author', 'filled': ['basics', 'indices', 'counts'], 'scholar_id': 'RAV-bbIAAAAJ', 'source': "<AuthorSource.AUTHOR_PROFILE_PAGE: 'AUTHOR_PROFILE_PAGE'>", 'name': 'Margreet Vos', 'url_picture': 'https://scholar.googleusercontent.com/citations?view_op=view_photo&user=RAV-bbIAAAAJ&citpid=2', 'affiliation': 'professor', 'interests': ['infection prevention'], 'email_domain': '@erasmusmc.nl', 'citedby': 15008, 'citedby5y': 7008, 'hindex': 47, 'hindex5y': 34, 
'i10index': 112, 'i10index5y': 81, 'cites_per_year': {1998: 41, 1999: 38, 2000: 53, 2001: 63, 2002: 74, 2003: 79, 2004: 84, 2005: 149, 2006: 239, 2007: 244, 2008: 312, 2009: 403, 2010: 528, 2011: 709, 2012: 805, 2013: 862, 2014: 956, 2015: 1003, 2016: 1030, 2017: 1019, 2018: 1073, 2019: 1248, 2020: 1222, 2021: 1274, 2022: 1148}}

dummyAuthor2 = {'container_type': 'Author', 'filled': ['basics', 'indices', 'counts'], 'scholar_id': 'T_nKvbgAAAAJ', 'source': "<AuthorSource.AUTHOR_PROFILE_PAGE: 'AUTHOR_PROFILE_PAGE'>", 'name': 'Dave Burke', 'affiliation': 'Loughborough University', 'organization': 16161526096496270291, 'interests': ['biomechanics', 'computer simulation', 'technique', 'variability', 'sport performance'], 'email_domain': '@lboro.ac.uk', 'citedby': 15, 'citedby5y': 7, 'hindex': 1, 'hindex5y': 1, 'i10index': 1, 'i10index5y': 0, 'cites_per_year': {2011: 5, 2012: 1, 2013: 2, 2014: 1, 2015: 1, 2016: 2, 2017: 1, 2018: 2}}

dummyStudies = [dummyStudy1, dummyStudy2]
dummyAuthors = [dummyAuthor1, dummyAuthor2]

def search(searchQuery, peerReviewedFilter, governmentAffiliationFilter, overNStudiesFilter, resultAmount):
    # studyDB = Government.query.all()
    # print(studyDB)
    searchedStudies = []
    searchIterations = 2
    if resultAmount > searchIterations:
         searchIterations = resultAmount
    studies = scholarly.search_pubs(str(searchQuery))
    for i in range (0, searchIterations):
        print("iteration", i)
        #this won't run if my api credits have been used up
        #studyUnfull = next(studies)
        #study = scholarly.fill(studyUnfull)
        #print(study)
        #if study:
        study = dummyStudies[i]
        if True:
            #adding information for study entity
            #first checks if it already exists within the database
            title = study.get('bib').get('title')
            if not studyExists(title):
                abstract = study.get('bib').get('abstract')
                pub_year = study.get('bib').get('pub_year')
                num_citations = study.get('num_citations')
                publisher = study.get('bib').get('publisher')
                gs_rank = study.get('gsrank')

                # governmentAffiliation = attributeHandler.governmentAffiliatior(study.get('pub_url'))
                # levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                governmentFind = attributeHandler()
                governmentAffiliation = governmentFind.governmentAffiliatior(study.get('pub_url'))
                levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                government = governmentAffiliation.government
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

                #adding information for author entity
                #first checks if it already exists within the database
                print(study.get('bib').get('author'))
                authorScholarIDs = study.get('author_id')
                authors = study.get('bib').get('author')
                authorList = authors.split(",")
                print("list of author ids", authorScholarIDs)
                print("list of authors", authorList)
                #NEED TO CONSIDER WHEN THERE IS A BLANK SCRAPE AS PROCESSING IS INVOLVED
                authorOrgUpdate = attributeHandler()
                authorOrgInfo = authorOrgUpdate.authorOrgUpdater(authorScholarIDs, authorList, title, i)


                #creating study entry in database
                new_study = Study(searchDepth=searchIterations, governmentAffiliation=levelOfAffiliation, title=title, abstract=abstract, pub_year=pub_year, num_citations=num_citations, 
                publisher=publisher, gs_rank=gs_rank, authorStrings=authors, government_id=government_id, journal_id=journal_id)
                db.session.add(new_study)
                db.session.commit()

                #setting up ID to establish link table relationship between Study and Author entries
                studyID = db.session.query(Study.id).filter_by(title=title).first()[0]  
                
                    
                # submitting link table entry
                # may need a more reliable secondary index than author name, author names could be shared, alternatively I could just set more attributes in the criteria
                for author in authorOrgInfo:
                    try:
                        authorName = author.get('authorName')
                        authorID = db.session.query(Author.id).filter_by(authorName=authorName).first()[0]
                        print("authorId", authorID)
                        new_authorStudyLink = AuthorStudyLink(author_id=authorID, study_id=studyID)
                        db.session.add(new_authorStudyLink)
                        db.session.commit()
                    except Exception:
                        pass


                
            else:
                print("ALREADY STORED IN DB, FETCHING INFO")

                #getting information about study from the database to input into the searchedStudies list
                fetchedStudy = db.session.query(Study).filter_by(title=title).first()
                title = fetchedStudy.title
                abstract = fetchedStudy.abstract
                pub_year = fetchedStudy.pub_year
                num_citations = fetchedStudy.num_citations
                publisher = fetchedStudy.publisher
                gs_rank = fetchedStudy.gs_rank
                levelOfAffiliation = fetchedStudy.governmentAffiliation

                #update search depth info
                fetchedStudy.searchDepth = searchIterations
                db.session.commit()

                #getting info about the journal by using the foreign key relationship between journal and study
                journal_id = fetchedStudy.journal_id
                associatedJournal = db.session.query(Journal).filter_by(id=journal_id).first()
                journal = associatedJournal.journalName

                #getting info about the authors using the author link table
                study_id = fetchedStudy.id
                associatedLinkedAuthors = db.session.query(AuthorStudyLink).filter_by(study_id=study_id).all()
                authorOrgInfo = []
                for author in associatedLinkedAuthors:
                    associatedAuthorID = author.author_id                    
                    print("associated author", associatedAuthorID)
                    associatedAuthor = db.session.query(Author).filter_by(id=associatedAuthorID).first()[0]
                    print("associated author", associatedAuthor)
                    authorName = associatedAuthor.authorName
                    authorCitations = associatedAuthor.authorCitations
                    associatedOrgID = associatedAuthor.organisation_id
                    associatedOrg = db.session.query(Organisation).filter_by(id=associatedOrgID).first()[0]
                    print("associated org", associatedOrg)
                    orgName = associatedOrg.orgName
                    authorInfo = {
                         'authorName': authorName,
                         'authorCitations': authorCitations,
                         'orgName': orgName
                    }
                    authorOrgInfo.append(authorInfo)

                government_id = fetchedStudy.government_id
                associatedGovernment = db.session.query(Government).filter_by(id=government_id).first()
                government = associatedGovernment.government

            print("title", title)
            print("abstract", abstract)
            print("citations", num_citations)
            print("pub year", pub_year)
            print("publisher", publisher)
            print("gs rank", gs_rank)
            print('levelofaffiliation', levelOfAffiliation)
            print("search depth", searchIterations)
            print("journal", journal)
            print("authors", authors)
            print("authorOrgInfo", authorOrgInfo)
            print("government", government)
            #adding information about the study to searchedStudies list after it has been gathered via scraping or database
            newStudy = SearchResponse(title, abstract, pub_year, num_citations, publisher, gs_rank, levelOfAffiliation, searchIterations, journal, authors, authorOrgInfo, government)
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
        government = countryToFind.government
        if 'edu' in suffix or 'ac' in suffix:
            return governmentAffiliationResponse(50, government, countryToFind.id)
        elif '.gov' in suffix:
            return governmentAffiliationResponse(100, government, countryToFind.id)
        else:
            return governmentAffiliationResponse(0, government, countryToFind.id)
    
    def authorOrgUpdater(self, authorScholarIDs, authorList, title, i):
        #comparing corresponding author and authorID lists, ideally I want to search with authorID because two different authors
        #could share the same name, however some author's don't have an author_id so I would have to search by name in that case,
        #if duplicate names come up in that case then that will reflect poorly on the author in terms of trustworthiness as 
        #getting information about them becomes more difficult
        authorInfo = []
        for x in range(0, len(authorScholarIDs)):
            correspondingID = authorScholarIDs[x]
            print(correspondingID)
            if correspondingID == "":
                print("CAN'T SEARCH ", authorList[x])
                # authorName_query = scholarly.search_author(a)
                # #finding the correct author with just their name, COME BACK TO LATER
                # #authorFound = False 
                # # authorFound = False
                # # while authorFound == False:
                # author_query = next(authorName_query) 
                # author = scholarly.fill(author_query, sections=['publications']) 
                # pubList = author.get('publications')
                # authorFound = False
                # i = 0
                # while authorFound == False or i == len(pubList):
                #     pubTitle = pubTitle[i].get('bib').get('title')
                #     if pubTitle == title:
                #         authorFound = True
                #     else:
                #         authorFound = False
                #     i = i + 1
            else:
                try:
                    #author_query = scholarly.search_author_id(correspondingID)
                    #author = scholarly.fill(author_query, sections=['basics', 'indices', 'counts']) 
                    author = dummyAuthors[i]
                    print(author)
                    authorName = author.get('name')   
                    if not authorExists(authorName):  
                        authorCitations = author.get('citedby')

                        #adding information about each author's main organisation to the organisation entity, this effects an author's scoring
                        #first checks if it already exists within the database
                        orgName = author.get('affiliation')
                        print(orgName, "orgname")
                        if not organisationExists(orgName):
                            new_org = Organisation(orgName=orgName)
                            db.session.add(new_org)
                            db.session.commit()
                        organisation_id = db.session.query(Organisation.id).filter_by(orgName=orgName).one()[0]
                        print("organisation id", organisation_id)
                        new_author = Author(authorName=authorName, authorCitations=authorCitations, organisation_id=organisation_id)
                        db.session.add(new_author)
                        db.session.commit()
                    else:
                        authorToFind = Author.query.filter(Author.authorName == authorName).one()[0]
                        authorName = authorToFind.authorName
                        authorCitations = authorToFind.authorCitations
                        organisation_id = authorToFind.organisation_id
                        orgToFind = Organisation.query.filter(Organisation.id == organisation_id).one()[0]
                        orgName = orgToFind.orgName

                    authorDict = {
                        'authorName': authorName,
                        'authorCitations': authorCitations,
                        'affiliation': orgName
                    }
                    authorInfo.append(authorDict)
                except:
                    print("COULDN'T SEARCH ID", correspondingID)

        return authorInfo

#used to return two items for the governmentAffiliation method of attributeHandler object
class governmentAffiliationResponse():
    def __init__(self, levelOfAffiliation, government, government_id=None):
        self.levelOfAffiliation = levelOfAffiliation 
        self.government = government
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
    def __init__(self, title, abstract, pub_year, num_citations, publisher, gs_rank, levelOfAffiliation, searchDepth, journal, authors, authorOrgInfo, government):
        self.title = title
        self.abstract = abstract
        self.pub_year = pub_year
        self.num_citations = num_citations
        self.publisher = publisher
        self.gs_rank = gs_rank
        self.levelOfAffiliation = levelOfAffiliation
        self.searchDepth = searchDepth
        self.journal = journal
        self.authors = authors
        self.authorOrgInfo = authorOrgInfo
        self.government = government