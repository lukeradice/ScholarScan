from scholarly import scholarly
from flask import flash

def search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount):
    results = []
    for i in range (0, resultAmount):
        search_query = scholarly.search_pubs(str(searchQuery))
        results.append(search_query)
        next(search_query)
    flash(results)
    
