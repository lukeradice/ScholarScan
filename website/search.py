from scholarly import scholarly, ProxyGenerator
from flask import flash
from . import db
from .models import Study, Author, AuthorStudyLink, Government
import tldextract

def search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount):
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
    print(searchQuery)
    print(peerReviewed)
    print(governmentAffiliation)
    print(overNStudies)
    searchIterations = 50
    if resultAmount > searchIterations:
        searchIterations = resultAmount
    pg = ProxyGenerator()
    success = pg.FreeProxies()
    scholarly.use_proxy(pg)
    if success:
        print("success")
        studies = scholarly.search_pubs(str(searchQuery))
        count = 0
        for i in range (0, searchIterations):
            study = next(studies)
            if study:
                abstract = study.get('bib').get('abstract')
                title = study.get('bib').get('title')
                governmentAffiliation = attributeHandler.governmentAffiliation(study.get('pub_url'))
                levelOfAffiliation = governmentAffiliation.levelOfAffiliation
                government_id = governmentAffiliation.government_id
                new_study = Study(SearchDepth=searchIterations, governmentAffiliation=levelOfAffiliation, title=title, abstract=abstract, government_id=government_id)
                db.session.add(new_study)
                db.session.commit()
            i = i + 1

class attributeHandler():
    def __init__(self) -> None:
        pass
    #handling government affiliation, only considered fully affiliated with .gov in domain
    #it is 50/50 with .ac and .edu as some education facilities are private
    def governmentAffiliation(domain):
        suffix = tldextract.extract(domain).suffix
        #if suffix in Government(domain):
            #government_id = Government(id)
        print(db.session.execute(db.select(Government).filter_by(correspondingDomain=suffix)).scalars())
       # if 'edu' in suffix or 'ac' in suffix:
          #  return governmentAffiliationResponse(50, government_id)
     #   elif '.gov' in suffix:
      #      return governmentAffiliationResponse(100, government_id)
      #  else:
        #    return governmentAffiliationResponse(0, government_id)

#used to return two items for the governmentAffiliation method of attributeHandler object
class governmentAffiliationResponse():
    def __init__(self, levelOfAffiliation, government_id=None):
        self.levelOfAffiliation = levelOfAffiliation 
        self.government_id = government_id 


            #SELECT government.id FROM Government WHERE correspondingDomain = domain
            #db.session.execute(db.select(Government).filter_by(correspondingDomain=suffix)).scalars()
