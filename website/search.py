from scholarly import scholarly, ProxyGenerator
from flask import flash
from . import db
from .models import Study, Author, AuthorStudyLink, Government, __repr__, Organisation
import tldextract

def search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount):
    
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
    searchIterations = 50
    if resultAmount > searchIterations:
         searchIterations = resultAmount
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)
    if success:
        print("success")
        studies = scholarly.search_pubs(str(searchQuery))
        for i in range (0, searchIterations):
            study = next(studies)
            if study:
                title = study.get('bib').get('title')
                if weHaventStoredIt.study(title):
                    #adding information for study entity
                    abstract = study.get('bib').get('abstract')
                    governmentAffiliation = attributeHandler.governmentAffiliatior(study.get('pub_url'))
                    levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                    government_id = governmentAffiliation.government_id
                    new_study = Study(SearchDepth=searchIterations, governmentAffiliation=levelOfAffiliation, title=title, abstract=abstract, government_id=government_id)
                    db.session.add(new_study)
                    db.session.commit()

                    #adding information for author entity
                    authorIDs = study.get('author_id')
                    for i in authorIDs:
                        author_query = scholarly.search_author_id(i)
                        author = scholarly.fill(author_query, sections=['basics', 'indices', 'counts'])
                        authorName = author.get('name')
                        if weHaventStoredIt.author(authorName):  
                            authorStudyCount = author.get('citedby')

                            #adding information about each author's main organisation to the organisation entity, this effects an author's scoring
                            name = author.get('affiliation')
                            scholar_id = author.get('organization')
                            new_org = Organisation(scholar_id=, name=)
                            new_author = Author(authorName=, authorStudyCount=, Organisation_id=)

                    db.session.commit()
                    print("Study added, number ", i)
            i = i + 1

class attributeHandler():
    def __init__(self) -> None:
        pass
    #handling government affiliation, only considered fully affiliated with .gov in domain
    #it is 50/50 with .ac and .edu as some education facilities are private
    def governmentAffiliatior(domain):
        suffix = tldextract.extract(domain).suffix
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

class weHaventStoredIt():
    def __init__(self) -> None:
        pass
    def study(title):
        exists = db.session.query(Study.title).filter_by(title=title).first()
        if exists == None:
            return True
        else:
            return False
    def author(name):
        exists = db.session.query(Author.authorName).filter_by(authorName=name).first()
        if exists == None:
            return True
        else:
            return False
    def organisation(name):
        exists = db.session.query(Organisation.name).filter_by(name=name).first()
        if exists == None:
            return True
        else:
            return False

        

        