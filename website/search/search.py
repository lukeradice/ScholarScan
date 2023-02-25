from website import db
from website.models import Study, Author, AuthorStudyLink, Government, Organisation, Journals
import tldextract
import sqlite3
from scholarly import scholarly
from datetime import datetime, date
from bs4 import BeautifulSoup
import requests
from website import myProxies
import json

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
    searchedStudies = []
    searchIterations = 2
    if studiesAnalysed:
        studiesAnalysed = int(studiesAnalysed)
    else: 
        studiesAnalysed = 2
    #increases search iteratrion to studiesAnalysed if above the planned iterations to meet the requirement
    if studiesAnalysed > searchIterations:
         searchIterations = studiesAnalysed      
    studies = scholarly.search_pubs(str(searchQuery))
    for i in range (0, searchIterations):
        print("iteration", i)
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
            #getting results as a list to avoid doing a try except statement here
            fetchedStudies = db.session.query(Study).filter_by(title=title).all()
            #alternative to StudyExists, takes into account when the dynamic information that is being
            #added to my databases has been there a year
            outOfDate = False
            if len(fetchedStudies) > 0:
                fetchedStudy = fetchedStudies[0]
                print("fetchedStudy", fetchedStudy)
                dateAdded = fetchedStudy.dateOfAddition
                print("dateAdded", dateAdded)
                dateDifference = date.today() - dateAdded
                print("dateDifference", dateDifference)
                if dateDifference.days > 365:
                    outOfDate = True
                    print("OUT OF DATE")
            else:
                fetchedStudy = None
                print("DIDNT EXIST")
            #should run this if if the study is out of date so needs to get attributes again or its not stored 
            #in the database at all
            if outOfDate == True or not fetchedStudy: 
                abstract = study.get('bib').get('abstract')
                pubYear = int(study.get('bib').get('pub_year'))
                pubUrl = study.get('pub_url')
                numCitations = study.get('num_citations')
                publisher = study.get('bib').get('publisher')
                if not publisher:
                    publisher = "Unknown"
                gsRank = study.get('gsrank')
                citedByUrl = study.get('citedby_url')

                #attribute handling object, the interface to do processing of attributes that aren't just fetching
                #from the publication objectc
                attributeHandling = AttributeHandler()

                governmentAffiliation = attributeHandling.governmentAffiliator(study.get('pub_url'))
                levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                government = governmentAffiliation.government
                affiliationNature = governmentAffiliation.affiliationNature
                government_id = governmentAffiliation.government_id
                governmentAffiliation = governmentAffiliation.governmentAffiliation

                #adding the details of the journal and checking to see if info on it is already stored in the database
                #processing of the peer reviewed attribute of the publication, tries two issn queries, a unique id for a journal
                #if those don't work it tries search by name
                journalName = study.get('bib').get('venue')
                print('journal', journalName)
                journalInDatabase = db.session.query(Journals).filter_by(journalTitle=journalName.upper()).first() 
                #to check if the journal is even in the database, before processing can begin
                if journalInDatabase:
                    journal_id = journalInDatabase.id
                    journalName = journalInDatabase.journalTitle
                    journalHIndex = journalInDatabase.journalHIndex
                    sjrScore = journalInDatabase.sjrScore
                    journalUnscrapableName = None
                    if not journalInDatabase.peerReviewed:
                        issns = journalInDatabase.issns
                        journalIssnLinks = attributeHandling.peerReviewLinkCheckIssn(issns)
                        journalNameLink = attributeHandling.peerReviewLinkCheckName(journalName)
                        peerReviewed = attributeHandling.checkJournalPeerReview(journalIssnLinks[0])
                        if peerReviewed == "Unknown":
                            #these condition are made more complex as some journals only have one issn, most have two
                            if len(journalIssnLinks) > 1: 
                                peerReviewed = attributeHandling.checkJournalPeerReview(journalIssnLinks[1])
                        if peerReviewed == "Unknown":
                            peerReviewed = attributeHandling.checkJournalPeerReview(journalNameLink)
                        print("peer reviewed (not journalInDatabase.peerReviewed)", peerReviewed)
                        #definiton of journalInfo object which will be in the response object, holding all journal information grouped together
                        journalInfo = JournalInfo(journalName=journalName, journalHIndex=journalHIndex, sjrScore=sjrScore, peerReviewed=peerReviewed)
                        #updating journal in journal table about whether it is peer reviewed or not so this info doesn't have to be scraped again
                        journalInDatabase.peerReviewed = peerReviewed
                        db.session.commit()
                    else:
                        peerReviewed = journalInDatabase.peerReviewed
                        journalInfo = JournalInfo(journalName=journalName, journalHIndex=journalHIndex, sjrScore=sjrScore, peerReviewed=peerReviewed)
                        print("peer reviewed was stored", peerReviewed)
                else:
                    peerReviewed = "Unknown"
                    print("journal couldn't be found in database so peer reviewed isn't known")
                    journalUnscrapableName = journalName.upper()
                    journal_id = None
                    #if no journal information can be gathered except its name, its name will be the only info presented to the website
                    journalInfo = JournalInfo(journalUnscrapableName=journalUnscrapableName)

                #adding information for author entity
                #first checks if it already exists within the database
                print(study.get('bib').get('author'))
                authorScholarIDs = study.get('author_id')
                authorStrings = study.get('bib').get('author')
                authorList = authorStrings.split(" and ")
                print("list of author ids", authorScholarIDs)
                print("list of authors", authorList)
                #NEED TO CONSIDER WHEN THERE IS A BLANK SCRAPE AS PROCESSING IS INVOLVED
                authorOrgInfo = attributeHandling.authorOrgUpdater(authorScholarIDs, authorList)
                #authorOrgInfo = authorOrgUpdate.authorOrgUpdater(authorScholarIDs, authorList, i)

                citationUrl = 'https://scholar.google.com/' + citedByUrl
                html = requests.get(citationUrl, proxies=myProxies, verify=False)
                citationPage = BeautifulSoup(html.content, 'html.parser')

                #implementation to calculate the value for the citationsOfTopCiters attribute
                results = citationPage.find(id="gs_res_ccl_mid")
                if results:
                    citationNumbers = results.find_all('a')
                    mostRecentCiters = []
                    for num in citationNumbers:
                        aText = num.text
                        if aText.startswith('Cited by') and len(mostRecentCiters) <= 3:
                            citations = int(aText[8:len(aText)])
                            mostRecentCiters.append(citations)
                    citationsOfTopCiters = 0
                    for num in mostRecentCiters:
                        num = int(num)
                        citationsOfTopCiters = citationsOfTopCiters + num
                elif citationPage.title.text == "Access Denied":
                    print("MY SCRAPING GOT BLOCKED OR ")
                    citationsOfTopCiters = 0
                else:
                    print("ZERO CITATIONS OF TOP CITERS")
                    citationsOfTopCiters = 0

                #WORKING IMPLEMENTATION TO GET daysSinceCite, need a new URL to sort citations by date
                citedCode = citedByUrl[15:35]
                citesByDate_url = 'https://scholar.google.com/scholar?hl=en&as_sdt=5,33&sciodt=0,33&cites=' + citedCode + '&scipsc=&q=&scisbd=1'
                print(citesByDate_url)
                html = requests.get(citesByDate_url, proxies=myProxies, verify=False)
                citedByDatePage = BeautifulSoup(html.content, 'html.parser')
                results = citedByDatePage.find(id="gs_res_ccl_mid") 
                if results:
                    ageInfo = results.find_next('span', class_= 'gs_age')
                    #daysSinceCite applied value, if none in last 365 arbitrarily set to 1000
                    if ageInfo:
                        text = ageInfo.text
                        print("AGEINFO", text)
                        #turns 'x days ago' statement into int(x)
                        daysSinceCite = int(text[0:text.find(" ")])
                    else:
                        daysSinceCite = 1000
                elif citationPage.title.text == "Access Denied":
                    print("MY SCRAPING GOT BLOCKED")
                    daysSinceCite = 365
                else:
                    print("OVER 365 DAYS SINCE CITE")
                    daysSinceCite = 365

                if outOfDate == False:
                    #creating study entry in database
                    new_study = Study(levelOfAffiliation=levelOfAffiliation, title=title, abstract=abstract, pubYear=pubYear, numCitations=numCitations, 
                                    publisher=publisher, gsRank=gsRank, authorStrings=authorStrings, government_id=government_id, governmentAffiliation=governmentAffiliation, 
                                    affiliationNature=affiliationNature, journal_id=journal_id, journalUnscrapableName=journalUnscrapableName,  
                                    daysSinceCite=daysSinceCite, citationsOfTopCiters=citationsOfTopCiters, dateOfAddition=date.today(), pubUrl=pubUrl)
                    db.session.add(new_study)
                else:
                    #information of study is updated if it is out of date, must be updated rather than deleted to obey
                    #data integrity rules
                    fetchedStudy.levelOfAffiliation = levelOfAffiliation
                    fetchedStudy.title = title
                    fetchedStudy.abstract = abstract
                    fetchedStudy.pubYear = pubYear
                    fetchedStudy.numCitations = numCitations 
                    fetchedStudy.publisher = publisher
                    fetchedStudy.gsRank = gsRank
                    fetchedStudy.authorStrings = authorStrings
                    fetchedStudy.governmentAffiliation = governmentAffiliation 
                    fetchedStudy.affiliationNature = affiliationNature
                    fetchedStudy.daysSinceCite = daysSinceCite
                    fetchedStudy.citationsOfTopCiters = citationsOfTopCiters
                    fetchedStudy.dateOfAddition = date.today()
                db.session.commit()

                #setting up ID to establish link table relationship between Study and Author entries
                studyID = db.session.query(Study.id).filter_by(title=title).first()[0] 
                
                # submitting link table entry
                # may need a more reliable secondary index than author name, author names could be shared, alternatively I could just set more attributes in the criteria
                for author in authorOrgInfo:
                    authorScholarID = author.scholarID
                    authorID = db.session.query(Author.id).filter_by(scholarID=authorScholarID).first()[0]
                    print("authorId", authorID)
                    new_authorStudyLink = AuthorStudyLink(author_id=authorID, study_id=studyID)
                    db.session.add(new_authorStudyLink)
                    db.session.commit()

            else:
                print("ALREADY STORED IN DB, FETCHING INFO")

                #getting information about study from the database to input into the searchedStudies list
                title = fetchedStudy.title
                abstract = fetchedStudy.abstract
                pubYear = fetchedStudy.pubYear
                pubUrl = fetchedStudy.pubUrl
                numCitations = fetchedStudy.numCitations
                publisher = fetchedStudy.publisher
                gsRank = fetchedStudy.gsRank
                levelOfAffiliation = fetchedStudy.levelOfAffiliation
                daysSinceCite = fetchedStudy.daysSinceCite
                citationsOfTopCiters = fetchedStudy.citationsOfTopCiters
                authorStrings = fetchedStudy.authorStrings

                government = fetchedStudy.government
                governmentAffiliation = fetchedStudy.governmentAffiliation
                affiliationNature = fetchedStudy.affiliationNature
                government_id = fetchedStudy.government_id
                authorStrings = fetchedStudy.authors

                db.session.commit()

                #getting info about the journal by using the foreign key relationship between journal and study
                journal_id = fetchedStudy.journal_id
                if journal_id:
                    associatedJournal = db.session.query(Journals).filter_by(id=journal_id).first()
                    journalName = associatedJournal.journalTitle
                    journalHIndex = associatedJournal.journalHIndex
                    sjrScore = associatedJournal.sjrScore
                    peerReviewed = associatedJournal.peerReviewed
                    journalInfo = JournalInfo(journalName=journalName, journalHIndex=journalHIndex, sjrScore=sjrScore, 
                                              peerReviewed=peerReviewed)
                else:
                    journalUnscrapableName = fetchedStudy.journalUnscrapableName
                    journalInfo = JournalInfo(journalUnscrapableName=journalUnscrapableName)

                #getting info about the authors using the author link table
                study_id = fetchedStudy.id
                associatedLinkedAuthors = db.session.query(AuthorStudyLink).filter_by(study_id=study_id).all()
                print(associatedLinkedAuthors, "list of linked authors")
                authorOrgInfo = []
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
                    authorYearsSinceCite = associatedAuthor.authorYearsSinceCite
                    careerLength = associatedAuthor.careerLength
                    authorCitationsThisYear = associatedAuthor.authorCitationsThisYear
                    scholarID = associatedAuthor.scholarID
                    associatedOrgID = associatedAuthor.organisation_id
                    associatedOrg = db.session.query(Organisation).filter_by(id=associatedOrgID).first()
                    print("associated org", associatedOrg)
                    orgName = associatedOrg.orgName
                    newAuthorOrg = AuthorOrgInfo(authorName, authorCitations, authorCitations5y, hIndex, hIndex5y, i10index,
                                                  i10index5y, authorYearsSinceCite, careerLength, authorCitationsThisYear, orgName,
                                                  scholarID)
                    authorOrgInfo.append(newAuthorOrg)

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
            print("type(journal)", type(journalInfo))
            print("journal", journalInfo.journalName)
            print("authors", authorStrings)
            print("authorOrgInfo", authorOrgInfo)
            print("government", government)
            print("daysSinceCite", daysSinceCite)
            print("citationsOfTopCiters", citationsOfTopCiters)
            print("peerReviewed", peerReviewed)
            #adding information about the study to searchedStudies list after it has been gathered via scraping or database
            newStudy = SearchResponse(title, abstract, pubYear, numCitations, publisher, gsRank, levelOfAffiliation, journalInfo, authorStrings, authorOrgInfo, government, 
                                      governmentAffiliation, affiliationNature, daysSinceCite, citationsOfTopCiters, pubUrl)
            searchedStudies.append(newStudy)
            
            print(Study.query.all())
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
            return GovernmentAffiliationResponse(100, government, True, "Government sponsored", countryToFind.id)
        else:
            return GovernmentAffiliationResponse(0, government, False, "Private company", countryToFind.id)

    def authorCitationAttributes(self, citesPerYear, attributeToCalculate):
        currentYear = getCurrentYear()
        lastYearCited = list(citesPerYear)[-1]
        if attributeToCalculate == "authorYearsSinceCite":
            yearsSinceCite = currentYear - lastYearCited
            return yearsSinceCite
        elif attributeToCalculate == "careerLength":
            careerLength = len(citesPerYear)
            return careerLength
        elif attributeToCalculate == "authorCitationsThisYear":
            if currentYear == lastYearCited:
                authorCitationsThisYear = citesPerYear.get(lastYearCited)
            else:
                authorCitationsThisYear = 0
            return authorCitationsThisYear 

    def authorOrgUpdater(self, authorScholarIDs, authorList):
        #comparing corresponding author and authorID lists, can only search with authors with AuthorID, think  I'll 
        #implement negative reward for no author id in scoring
        authorOrgInfo = []
        print("ID LIST")
        print(authorScholarIDs)
        for correspondingID in authorScholarIDs:
            print(correspondingID)
            #if the author has a scholar id, then the scraping of author/org information can commence
            if correspondingID:
                #condition to add author information if the author name isn't already in the database
                i = authorScholarIDs.index(correspondingID)
                authorName = authorList[i]
                fetchedAuthors = db.session.query(Author).filter_by(scholarID=correspondingID).all()
                #alternative to StudyExists, takes into account when the dynamic information that is being
                #added to my databases has been there a year
                outOfDate = False
                if len(fetchedAuthors) > 0:
                    fetchedAuthor = fetchedAuthors[0]
                    print("fetchedAuthor", fetchedAuthor)
                    dateAdded = fetchedAuthor.dateOfAddition
                    print("dateAdded", dateAdded)
                    dateDifference = date.today() - dateAdded
                    print("dateDifference", dateDifference)
                    if dateDifference.days > 365:
                        outOfDate = True
                else:
                    fetchedAuthor = None
                #new author information is gathered if its information is out of date or hasnt been stored in the
                #database before
                if outOfDate == True or not fetchedAuthor:
                    author_query = scholarly.search_author_id(correspondingID)
                    author = scholarly.fill(author_query, sections=['basics', 'indices', 'counts']) 
                    #author = dummyAuthors[i]
                    print(author)
                    authorCitations = author.get('citedby') 
                    authorCitations5y = author.get('citedby5y')
                    hIndex = author.get('hindex')
                    hIndex5y = author.get('hindex5y')
                    i10index = author.get('i10index')
                    i10index5y = author.get('i10index5y')
                    citesPerYear = author.get('cites_per_year')
                    #inside AttributeHandler so functions can be referred to as self.
                    authorYearsSinceCite = self.authorCitationAttributes(citesPerYear, "authorYearsSinceCite")
                    careerLength = self.authorCitationAttributes(citesPerYear, "careerLength")
                    authorCitationsThisYear = self.authorCitationAttributes(citesPerYear, "authorCitationsThisYear")
                    dateOfAddition = date.today()

                    #adding information about each author's main organisation to the organisation entity, this effects an author's scoring
                    #first checks if it already exists within the database
                    orgName = author.get('affiliation')
                    print(orgName, "orgname")
                    if not organisationExists(orgName):
                        new_org = Organisation(orgName=orgName)
                        db.session.add(new_org)
                        db.session.commit()
                    organisation_id = db.session.query(Organisation.id).filter_by(orgName=orgName).first()[0]
                    print("organisation id", organisation_id)

                    if outOfDate == False:
                        #new author entity record
                        new_author = Author(authorName=authorName, authorCitations=authorCitations, authorCitations5y=authorCitations5y, hIndex=hIndex,
                                            hIndex5y=hIndex5y, i10index=i10index, i10index5y=i10index5y, authorYearsSinceCite=authorYearsSinceCite, 
                                            careerLength=careerLength, authorCitationsThisYear=authorCitationsThisYear, organisation_id=organisation_id,
                                            scholarID=correspondingID, dateOfAddition=dateOfAddition)
                        db.session.add(new_author)
                    else:
                        #updating author numerical information if its out of date, been in the database too long for these numbers to still 
                        #be reliable
                        fetchedAuthor.authorCitations=authorCitations
                        fetchedAuthor.authorCitations5y=authorCitations5y
                        fetchedAuthor.hIndex=hIndex
                        fetchedAuthor.hIndex5y=hIndex5y
                        fetchedAuthor.i10index=i10index
                        fetchedAuthor.i10index5y=i10index5y
                        fetchedAuthor.authorYearsSinceCite=authorYearsSinceCite 
                        fetchedAuthor.careerLength=careerLength
                        fetchedAuthor.authorCitationsThisYear=authorCitationsThisYear
                    db.session.commit()
                else:
                    authorToFind = Author.query.filter(Author.authorName == authorName).first()
                    authorName = authorToFind.authorName
                    authorCitations = authorToFind.authorCitations  
                    authorCitations5y = authorToFind.authorCitations5y
                    hIndex = authorToFind.hIndex
                    hIndex5y = authorToFind.hIndex5y
                    i10index = authorToFind.i10index
                    i10index5y = authorToFind.i10index5y
                    authorYearsSinceCite = authorToFind.authorYearsSinceCite
                    careerLength = authorToFind.careerLength
                    authorCitationsThisYear = authorToFind.authorCitationsThisYear
                    organisation_id = authorToFind.organisation_id
                    orgToFind = Organisation.query.filter(Organisation.id == organisation_id).first()
                    orgName = orgToFind.orgName

                #creation of AuthorOrgInfo object to store author/organisation information
                newAuthorOrg = AuthorOrgInfo(authorName, authorCitations, authorCitations5y, hIndex, hIndex5y, i10index,
                                            i10index5y, authorYearsSinceCite, careerLength, authorCitationsThisYear, orgName,
                                            correspondingID)        
                authorOrgInfo.append(newAuthorOrg)
        return authorOrgInfo
    
    def peerReviewLinkCheckName(self, journalName):
        journalNameWords = journalName.split(" ")
        journalSearchAddressName = journalNameWords[0]
        for word in journalNameWords:
            if journalNameWords.index(word) == 0:
                word = ""
            else:
                word = "%20" + word
            journalSearchAddressName = journalSearchAddressName + word
        journalSearchAddressName = "http://uh4jc3de5m.search.serialssolutions.com/ejp/api/1/libraries/UH4JC3DE5M/search/types/alternate_title_equals/"+journalSearchAddressName+"?titleType=JOURNALS&beginPage=0&language=en-US&filterBy=All"
        return journalSearchAddressName

    #function to get link to scrape from for issn of a journal
    def peerReviewLinkCheckIssn(self, issns):
        issns = issns.split(",")
        issnLinks = []   
        for issn in issns:
            #making issn whitespace for link
            issn = issn.replace(" ", "")
            journalSearchAddressIssn = "http://uh4jc3de5m.search.serialssolutions.com/ejp/api/1/libraries/UH4JC3DE5M/search/types/issn_equals/"+issn+"?titleType=JOURNALS&beginPage=0&language=en-US&filterBy=All"

            issnLinks.append(journalSearchAddressIssn)
        return issnLinks
    
    def checkJournalPeerReview(self, url):
        with requests.Session() as s:
            getJson = s.get(url, proxies=myProxies, verify=False)
            jsonPage = getJson.text
            # print(jsonPage)
            dataDict = json.loads(jsonPage)
            print(dataDict)
            #try excepts for if there are no search results for the journal therefore 
            #the info for whether its peer reviewed or not won't be available
            #if/elif is for 
            try:
                peerReviewCheck = dataDict.get('titles')
                peerReviewed = str(peerReviewCheck[0].get('peerReviewed'))
            except IndexError:
                peerReviewed = "Unknown"
                print("unknown if peer reviewed")
            return peerReviewed    

#used to return two items for the governmentAffiliation method of AttributeHandler object
class GovernmentAffiliationResponse():
    def __init__(self, levelOfAffiliation, government, governmentAffiliation, affilationNature, government_id=None):
        self.levelOfAffiliation = levelOfAffiliation 
        self.government = government
        self.governmentAffiliation = governmentAffiliation
        self.affiliationNature = affilationNature
        self.government_id = government_id 

# def studyExists(title):
#     return checkExists(title, Study, "title") 

# def authorExists(name):
#     return checkExists(name, Author, "authorName")

def organisationExists(orgName):
    return checkExists(orgName, Organisation, "orgName")

# def journalExists(journal):
#     return checkExists(journal, Journal, "journalName")

#check exists is the implementation for checking if an element is stored in the database,
# the reason the functions above  
def checkExists(checkingVariable, relevantEntity, entityColumn):
        #need the try except statement for if nothing is returned
        try:
            exists = relevantEntity.query.filter_by(**{entityColumn:checkingVariable}).first()
            return exists
        except sqlite3.OperationalError:
            return False

#class which defines all the data to go with a publication, be presented with it on the website and used to calculate its position
class SearchResponse():
    def __init__(self, title, abstract, pubYear, numCitations, publisher, gsRank, levelOfAffiliation, journalInfo, authorStrings, authorOrgInfo, government,
                 governmentAffiliation, affiliationNature, daysSinceCite, citationsOfTopCiters, pubUrl):
        self.title = title
        self.abstract = abstract
        self.pubYear = pubYear
        self.numCitations = numCitations
        self.publisher = publisher
        #self.publisherRating = publisherRating
        self.gsRank = gsRank
        self.levelOfAffiliation = levelOfAffiliation
        self.journalInfo = journalInfo
        self.authors = authorStrings
        self.authorOrgInfo = authorOrgInfo
        self.government = government
        self.governmentAffiliation = governmentAffiliation
        self.affiliationNature = affiliationNature
        self.daysSinceCite=daysSinceCite
        self.citationsOfTopCiters=citationsOfTopCiters
        self.pubUrl = pubUrl
        # self.noConflictInterest = noConflictInterest
        # self.conflictDisclosed = conflictDisclosed
        # self.notExternallyFunded = notExternallyFunded
        # self.conflictEvidence = conflictEvidence
        
#author object containing all the information that can be presented to the website and have an effect on scoring
class AuthorOrgInfo():
    def __init__(self, authorName, authorCitations, authorCitations5y, hIndex, hIndex5y, i10index,
                 i10index5y, authorYearsSinceCite, careerLength, authorCitationsThisYear, orgName,
                 scholarID):
        self.authorName = authorName
        self.authorCitations = authorCitations
        self.authorCitations5y = authorCitations5y
        self.hIndex = hIndex
        self.hIndex5y = hIndex5y
        self.i10index = i10index
        self.i10index5y = i10index5y
        self.authorYearsSinceCite = authorYearsSinceCite
        self.careerLength = careerLength
        self.authorCitationsThisYear = authorCitationsThisYear
        self.orgName = orgName
        self.scholarID = scholarID

class JournalInfo():
    def __init__(self, journalName=None, journalUnscrapableName=None ,issns=None, sjrScore=0, journalHIndex=0, publisherName=None, peerReviewed=None):
        self.journalName = journalName
        self.journalUnscrapableName = journalUnscrapableName
        self.issns = issns
        self.sjrScore = sjrScore
        self.journalHIndex = journalHIndex
        self.publisherName = publisherName
        self.peerReviewed = peerReviewed

def getCurrentYear():
    currentYear = date.today().strftime("%Y")
    currentYear = int(currentYear)
    return int(currentYear)
