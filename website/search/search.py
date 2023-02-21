from website import db
from website.models import Study, Author, AuthorStudyLink, Government, __repr__, Organisation, Journal
import tldextract
import sqlite3
from scholarly import scholarly
import datetime

# dummyStudy1 = {'container_type': 'Publication', 'source': "<PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>", 'bib': {'title': 'Nose picking and nasal carriage of Staphylococcus aureus', 'author': 'Wertheim, Heiman FL and Van Kleef, Menno and Vos, Margreet C and Ott, Alewijn and Verbrugh, Henri A and Fokkens, Wytske', 'pub_year': '2006', 'venue': 'Infection Control & …', 'abstract': 'part of the nose, we considered the habit of nose picking as a  a positive correlation between  nose picking and S. aureus  in a larger cohort with predefined criteria for nose picking.', 
# 'publisher': 'Cambridge University Press', 'pages': '863--867', 'number': '8', 'volume': '27', 'journal': 'Infection Control \\& Hospital Epidemiology', 'pub_type': 'article', 'bib_id': 'wertheim2006nose'}, 'filled': True, 'gsrank': 1, 'pub_url': 'https://www.cambridge.org/core/journals/infection-control-and-hospital-epidemiology/article/nose-picking-and-nasal-carriage-of-staphylococcus-aureus/DC21FFA771693C772308530D2B1A1452', 'author_id': ['JVFGW64AAAAJ', '', 'RAV-bbIAAAAJ', ''], 'url_scholarbib': '/scholar?hl=en&q=info:KyKH-9mNPpcJ:scholar.google.com/&output=cite&scirp=0&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3Dnose%2Bpicking%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=KyKH-9mNPpcJ&ei=gQ2zY6CMLc6TywSl1LXoCA&json=', 'num_citations': 90, 'citedby_url': '/scholar?cites=10898304115650535979&as_sdt=5,33&sciodt=0,33&hl=en', 'url_related_articles': '/scholar?q=related:KyKH-9mNPpcJ:scholar.google.com/&scioq=nose+picking&hl=en&as_sdt=0,33', 'eprint_url': 'https://www.academia.edu/download/46395935/Nose_picking_and_nasal_carriage_of_Staph20160611-15499-1ngo5wz.pdf'}

# dummyStudy2 = {'container_type': 'Publication', 'source': "<PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>", 'bib': {'title': 'A comparison of compensation for release timing and maximum hand speed in recreational and competitive darts players', 'author': 'Burke, D and Yeadon, F', 'pub_year': '2009', 'venue': 'ISBS-Conference Proceedings Archive', 'abstract': 'The level of accuracy achieved by darts players is dependent on their timing capabilities,   a competitive darts player in a throwing task. The inaccuracy of the throws by both players were', 'booktitle': 'ISBS-Conference Proceedings Archive', 'pub_type': 'inproceedings', 'bib_id': 'burke2009comparison'}, 'filled': True, 'gsrank': 1, 'pub_url': 'https://ojs.ub.uni-konstanz.de/cpa/article/view/3166', 'author_id': ['T_nKvbgAAAAJ', ''], 'url_scholarbib': '/scholar?hl=en&q=info:dfry9K19sYUJ:scholar.google.com/&output=cite&scirp=0&hl=en', 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3Ddarts%2Bplayers%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=dfry9K19sYUJ&ei=1xGzY93FO-iSy9YPlIeUiAU&json=', 'num_citations': 11, 'citedby_url': '/scholar?cites=9633619264014580341&as_sdt=5,33&sciodt=0,33&hl=en', 'url_related_articles': '/scholar?q=related:dfry9K19sYUJ:scholar.google.com/&scioq=darts+players&hl=en&as_sdt=0,33', 'eprint_url': 'https://ojs.ub.uni-konstanz.de/cpa/article/download/3166/2970'}

# dummyAuthor1 = {'container_type': 'Author', 'filled': ['basics', 'indices', 'counts'], 'scholar_id': 'RAV-bbIAAAAJ', 'source': "<AuthorSource.AUTHOR_PROFILE_PAGE: 'AUTHOR_PROFILE_PAGE'>", 'name': 'Margreet Vos', 'url_picture': 'https://scholar.googleusercontent.com/citations?view_op=view_photo&user=RAV-bbIAAAAJ&citpid=2', 'affiliation': 'professor', 'interests': ['infection prevention'], 'email_domain': '@erasmusmc.nl', 'citedby': 15008, 'citedby5y': 7008, 'hindex': 47, 'hindex5y': 34, 
# 'i10index': 112, 'i10index5y': 81, 'cites_per_year': {1998: 41, 1999: 38, 2000: 53, 2001: 63, 2002: 74, 2003: 79, 2004: 84, 2005: 149, 2006: 239, 2007: 244, 2008: 312, 2009: 403, 2010: 528, 2011: 709, 2012: 805, 2013: 862, 2014: 956, 2015: 1003, 2016: 1030, 2017: 1019, 2018: 1073, 2019: 1248, 2020: 1222, 2021: 1274, 2022: 1148}}

# dummyAuthor2 = {'container_type': 'Author', 'filled': ['basics', 'indices', 'counts'], 'scholar_id': 'T_nKvbgAAAAJ', 'source': "<AuthorSource.AUTHOR_PROFILE_PAGE: 'AUTHOR_PROFILE_PAGE'>", 'name': 'Dave Burke', 'affiliation': 'Loughborough University', 'organization': 16161526096496270291, 'interests': ['biomechanics', 'computer simulation', 'technique', 'variability', 'sport performance'], 'email_domain': '@lboro.ac.uk', 'citedby': 15, 'citedby5y': 7, 'hindex': 1, 'hindex5y': 1, 'i10index': 1, 'i10index5y': 0, 'cites_per_year': {2011: 5, 2012: 1, 2013: 2, 2014: 1, 2015: 1, 2016: 2, 2017: 1, 2018: 2}}

# dummyStudies = [dummyStudy1, dummyStudy2]
# dummyAuthors = [dummyAuthor1, dummyAuthor2]

def search(searchQuery, studiesAnalysed):
    print(Study.query.all())
    # studyDB = Government.query.all()
    # print(studyDB)
    searchedStudies = []
    searchIterations = 2
    if studiesAnalysed:
        studiesAnalysed = int(studiesAnalysed)
    else: 
        studiesAnalysed = 5
    #increases search iteratrion to studiesAnalysed if above the planned iterations to meet the requirement
    if studiesAnalysed > searchIterations:
         searchIterations = studiesAnalysed      
    studies = scholarly.search_pubs(str(searchQuery))
    for i in range (0, searchIterations):
        print("iteration", i)
        #this won't run if my api credits have been used up
        try:
            studyUnfull = next(studies)
        except StopIteration:
            return searchedStudies
        study = scholarly.fill(studyUnfull)
        print(study)
        if study:
        # study = dummyStudies[i]
        # if True:
            #adding information for study entity
            #first checks if it already exists within the database
            title = study.get('bib').get('title')
            if not checkExists(title, Study, "title"): 
            # if not studyExists(title): 
                print("DIDNT EXIST")
                abstract = study.get('bib').get('abstract')
                pubYear = study.get('bib').get('pub_year')
                numCitations = study.get('num_citations')
                publisher = study.get('bib').get('publisher')
                gsRank = study.get('gsrank')
                citedByUrl = study.get('citedby_url')

                governmentFind = AttributeHandler()
                governmentAffiliation = governmentFind.governmentAffiliator(study.get('pub_url'))
                levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                government = governmentAffiliation.government
                govenrmentAffiliation = governmentAffiliation.governmentAffiliation
                affiliationNature = governmentAffiliation.affiliationNature
                government_id = governmentAffiliation.government_id

                #adding the details of the journal and checking to see if info on it is already stored in the database
                journal = study.get('bib').get('venue')
                print('journal', journal)
                if not journalExists(journal):
                    new_journal = Journal(journalName=journal)
                    db.session.add(new_journal)
                    db.session.commit()
                    print("journal didn't exist, been added")
                journal_id = Journal.query.filter_by(journalName=journal).first()
                journal_id = journal_id.id
                print("journal_id", journal_id)

                #adding information for author entity
                #first checks if it already exists within the database
                print(study.get('bib').get('author'))
                authorScholarIDs = study.get('author_id')
                authors = study.get('bib').get('author')
                authorList = authors.split(",")
                print("list of author ids", authorScholarIDs)
                print("list of authors", authorList)
                #NEED TO CONSIDER WHEN THERE IS A BLANK SCRAPE AS PROCESSING IS INVOLVED
                authorOrgUpdate = AttributeHandler()
                authorOrgInfo = authorOrgUpdate.authorOrgUpdater(authorScholarIDs, authorList)
                #authorOrgInfo = authorOrgUpdate.authorOrgUpdater(authorScholarIDs, authorList, i)

                #creating study entry in database
                new_study = Study(searchDepth=searchIterations, governmentAffiliation=levelOfAffiliation, title=title, abstract=abstract, pubYear=pubYear, numCitations=numCitations, 
                publisher=publisher, gsRank=gsRank, authorStrings=authors, government_id=government_id, journal_id=journal_id)
                db.session.add(new_study)
                db.session.commit()

                #setting up ID to establish link table relationship between Study and Author entries
                studyID = db.session.query(Study.id).filter_by(title=title).first() 
                
                # submitting link table entry
                # may need a more reliable secondary index than author name, author names could be shared, alternatively I could just set more attributes in the criteria
                for author in authorOrgInfo:
                    try:
                        authorName = author.get('authorName')
                        authorID = db.session.query(Author.id).filter_by(authorName=authorName).first()
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
                pubYear = fetchedStudy.pubYear
                numCitations = fetchedStudy.numCitations
                publisher = fetchedStudy.publisher
                gsRank = fetchedStudy.gsRank
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
                for author in associatedLinkedAuthors:
                    associatedAuthorID = author.author_id                    
                    print("associated author", associatedAuthorID)
                    associatedAuthor = db.session.query(Author).filter_by(id=associatedAuthorID).first()
                    print("associated author", associatedAuthor)
                    authorName = associatedAuthor.authorName
                    authorCitations = associatedAuthor.authorCitations
                    authorCitations5y = associatedAuthor.authorCitations5y
                    hIndex = associatedAuthor.hIndex
                    hIndex5y = associatedAuthor.hIndex5y
                    i10index = associatedAuthor.i10index
                    i10index5y = associatedAuthor.i10index5y
                    citesPerYear = associatedAuthor.citesPerYear
                    associatedOrgID = associatedAuthor.organisation_id
                    associatedOrg = db.session.query(Organisation).filter_by(id=associatedOrgID).first()
                    print("associated org", associatedOrg)
                    orgName = associatedOrg.orgName
                    authorOrgInfo = AuthorOrgInfo(authorName, authorCitations, authorCitations5y, hIndex, hIndex5y, i10index,
                                                  i10index5y, citesPerYear, orgName)
                # authorOrgInfo = []
                # for author in associatedLinkedAuthors:
                #     associatedAuthorID = author.author_id                    
                #     print("associated author", associatedAuthorID)
                #     associatedAuthor = db.session.query(Author).filter_by(id=associatedAuthorID).first()
                #     print("associated author", associatedAuthor)
                #     authorName = associatedAuthor.authorName
                #     authorCitations = associatedAuthor.authorCitations
                #     associatedOrgID = associatedAuthor.organisation_id
                #     associatedOrg = db.session.query(Organisation).filter_by(id=associatedOrgID).first()
                #     print("associated org", associatedOrg)
                #     orgName = associatedOrg.orgName
                #     authorInfo = {
                #          'authorName': authorName,
                #          'authorCitations': authorCitations,
                #          'orgName': orgName
                #     }
                #     authorOrgInfo.append(authorInfo)

                government_id = fetchedStudy.government_id
                associatedGovernment = db.session.query(Government).filter_by(id=government_id).first()
                government = associatedGovernment.government

            print("title", title)
            print("abstract", abstract)
            print("citations", numCitations)
            print("pub year", pubYear)
            print("publisher", publisher)
            print("gs rank", gsRank)
            print('levelofaffiliation', levelOfAffiliation)
            print("search depth", searchIterations)
            print("journal", journal)
            print("authors", authors)
            print("authorOrgInfo", authorOrgInfo)
            print("government", government)
            #adding information about the study to searchedStudies list after it has been gathered via scraping or database
            newStudy = SearchResponse(title, abstract, pubYear, numCitations, publisher, gsRank, levelOfAffiliation, 
                                      searchIterations, journal, authors, authorOrgInfo, government, peerReviewed=True, 
                                      noConflictInterest=True, conflictDisclosed=True, conflictEvidence="", publisherRating=0)
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

class AttributeHandler():
    def __init__(self):
        pass
    #handling government affiliation, only considered fully affiliated with .gov in domain
    #it is 50/50 with .ac and .edu as some education facilities are private
    def governmentAffiliator(self, domain):
        suffix = tldextract.extract(domain).suffix
        suffix = '.' + suffix
        print('suffix', suffix)
        countryToFind = Government.query.filter(Government.correspondingDomain == suffix).one()
        government = countryToFind.government
        if 'edu' in suffix or 'ac' in suffix:
            return GovernmentAffiliationResponse(50, government, False, "Educational institute", countryToFind.id)
        elif '.gov' in suffix:
            return GovernmentAffiliationResponse(100, government, True, "Government sponsored" countryToFind.id)
        else:
            return GovernmentAffiliationResponse(0, government, False, "Private company", countryToFind.id)

    def citationAttributes(citesPerYear, attributeToCalculate):
        if attributeToCalculate == "yearsSinceCite":
            currentYear = getCurrentYear()
            lastYearCited = citesPerYear.keys()[-1]
            yearsSinceCite = currentYear - lastYearCited
            return yearsSinceCite
        elif attributeToCalculate == "careerLength":
            careerLength = len(citesPerYear)
            return careerLength

    def authorOrgUpdater(self, authorScholarIDs, authorList):
        #comparing corresponding author and authorID lists, can only search with authors with AuthorID, think  I'll 
        #implement negative reward for no author id in scoring
        authorOrgInfo = []
        for correspondingID in authorScholarIDs:
            print(correspondingID)
            #if the author has a scholar id, then the scraping of author/org information can commence
            if correspondingID:
                #condition to add author information if the author name isn't already in the database
                i = authorScholarIDs.index(correspondingID)
                if not authorExists(authorList[i]):  
                    author_query = scholarly.search_author_id(correspondingID)
                    author = scholarly.fill(author_query, sections=['basics', 'indices', 'counts']) 
                    #author = dummyAuthors[i]
                    print(author)
                    authorName = author.get('name') 
                    authorCitations = author.get('citedby') 
                    authorCitations5y = author.get('citedby5y')
                    hIndex = author.get('hindex')
                    hIndex5y = author.get('hindex5y')
                    i10index = author.get('i10index')
                    i10index5y = author.get('i10index5y')
                    citesPerYear = author.get('cites_per_year')
                    #inside AttributeHandler so functions can be referred to as self.
                    yearsSinceCite = self.citationAttributes(citesPerYear, "yearsSinceCite")
                    careerLength = self.citationAttributes(citesPerYear, "careerLength")

                    #adding information about each author's main organisation to the organisation entity, this effects an author's scoring
                    #first checks if it already exists within the database
                    orgName = author.get('affiliation')
                    print(orgName, "orgname")
                    if not organisationExists(orgName):
                        new_org = Organisation(orgName=orgName)
                        db.session.add(new_org)
                        db.session.commit()
                    organisation_id = db.session.query(Organisation.id).filter_by(orgName=orgName).first()
                    print("organisation id", organisation_id)
                    #new author entity record
                    new_author = Author(authorName=authorName, authorCitations=authorCitations, authorCitations5y=authorCitations5y, hIndex=hIndex,
                                        hIndex5y=hIndex5y, i10index=i10index, i10index5y=i10index5y, yearsSinceCite=yearsSinceCite, 
                                        careerLength=careerLength, organisation_id=organisation_id)
                    db.session.add(new_author)
                    db.session.commit()
                else:
                    authorToFind = Author.query.filter(Author.authorName == authorName).first()
                    authorName = authorToFind.authorName
                    authorCitations = authorToFind.authorCitations
                    organisation_id = authorToFind.organisation_id
                    orgToFind = Organisation.query.filter(Organisation.id == organisation_id).first()
                    orgName = orgToFind.orgName

                    #creation of AuthorOrgInfo object to store author/organisation information
                    newAuthorOrg = AuthorOrgInfo(authorName, authorCitations, authorCitations5y, hIndex, hIndex5y, i10index,
                                              i10index5y, citesPerYear, orgName)
                    authorOrgInfo.append(newAuthorOrg)
        return authorOrgInfo

#used to return two items for the governmentAffiliation method of AttributeHandler object
class GovernmentAffiliationResponse():
    def __init__(self, levelOfAffiliation, government, governmentAffiliation, affilationNature, government_id=None):
        self.levelOfAffiliation = levelOfAffiliation 
        self.government = government
        self.governmentAffiliation = governmentAffiliation
        self.affiliationNature = affilationNature
        self.government_id = government_id 

def studyExists(title):
    #need the try except statement for when the database doesn't exist yet so it can't check for it
    try:
        exists = Study.query.filter_by(title=title).first()
        return exists
    except sqlite3.OperationalError:
        return False
def authorExists(name):
    try:
        exists = Author.query.filter_by(authorName=name).first()
        return exists
    except sqlite3.OperationalError:
        return False
def organisationExists(orgName):
    try:
        exists = Organisation.query.filter_by(orgName=orgName).first()
        return exists
    except sqlite3.OperationalError:
        return False
def journalExists(journal):
    try:
        exists = Journal.query.filter_by(journalName=journal).first()
        return exists
    except sqlite3.OperationalError:
        return False
def checkExists(checkingVariable, relevantEntity, entityColumn):
        try:
            # exists = db.session.query(relevantEntity).filter_by(**{entityColumn:checkingVariable}).first()
            exists = relevantEntity.query.filter_by(**{entityColumn:checkingVariable}).first()
            return exists
        except sqlite3.OperationalError:
            return False

class SearchResponse():
    def __init__(self, title, abstract, pubYear, numCitations, publisher, gsRank, levelOfAffiliation, searchDepth, journal, authors, authorOrgInfo, government,
                 peerReviewed, noConflictInterest, conflictDisclosed, conflictEvidence, publisherRating):
        self.title = title
        self.abstract = abstract
        self.pubYear = pubYear
        self.numCitations = numCitations
        self.publisher = publisher
        self.publisherRating = publisherRating
        self.gsRank = gsRank
        self.levelOfAffiliation = levelOfAffiliation
        self.searchDepth = searchDepth
        self.journalInfo = journal
        self.authors = authors
        self.authorOrgInfo = authorOrgInfo
        self.government = government
        self.peerReviewed = peerReviewed
        self.noConflictInterest = noConflictInterest
        self.conflictDisclosed = conflictDisclosed
        self.conflictEvidence = conflictEvidence

class AuthorOrgInfo():
    def __init__(self, authorName, authorCitations, authorCitations5y, hIndex, hIndex5y, i10index,
                 i10index5y, yearsSinceCite, careerLength, orgName):
        self.authorName = authorName
        self.authorCitations = authorCitations
        self.authorCitations5y = authorCitations5y
        self.hIndex = hIndex
        self.hIndex5y = hIndex5y
        self.i10index = i10index
        self.i10index5y = i10index5y
        self.yearsSinceCite = yearsSinceCite
        self.careerLength = careerLength
        self.orgName = orgName

def getCurrentYear():
    currentYear = datetime.date.today().strftime("%Y")
    return int(currentYear)
