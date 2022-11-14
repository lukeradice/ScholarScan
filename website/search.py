from scholarly import scholarly, ProxyGenerator
from flask import flash

def search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount):
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
        for i in range (0, searchIterations):
            study = next(studies)
            if study:
                abstract = study.get('bib')
                print(abstract)
            i = i + 1
    
    
