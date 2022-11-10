from scholarly import scholarly
#may use an an aid to validation
from flask import flash

def searchCheck(searchQuery, overNStudies, resultAmount):
    if searchQuery.strip() == None:
        flash("Please enter a valid search")
        return False
    elif can_convert_to_int(overNStudies) and overNStudies != None:
        flash("Please enter an integer in the 'author has over n studies' field")
        return False
    elif can_convert_to_int(resultAmount) and resultAmount != None:
        flash("Please enter an integer in the 'amount of search results' field")
        return False
    else:
        searchQuery = int(searchQuery)
        overNStudies = int(overNStudies)
        resultAmount = int(resultAmount)
        return True
        
def can_convert_to_int(string):
    try:
        int(string)

        return True
    except ValueError:
        return False