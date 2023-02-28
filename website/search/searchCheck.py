from scholarly import scholarly
#may use an an aid to validation
from flask import flash

#function checks of an item can be converted into an integer, for inputs which could be anything but are meant to be used in calculations      
def can_convert_to_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def searchCheck(searchQuery, minCitations, maxGsRank, daysSinceCite, minPubYear, 
                minAuthCitations, resultAmount, minCareerLength):
    #for the two categories of checks aside from the one on the search query, I’ve put them in 
    # lists to loop through the validation conditions
    zeroNegativeDecimalChecks = [minCitations, maxGsRank, daysSinceCite, minPubYear, 
                                minAuthCitations, resultAmount, minCareerLength]
    if searchQuery == "":
        #error messages are flashed when appropriate with message
            flash("Please enter a valid search", category="error")
            return False
    #had to alter this filter cos it won't take none and the number values will 
    # come in as strings
    for filter in zeroNegativeDecimalChecks:
        if filter !="" and can_convert_to_int(filter) == False:
            flash("Please make sure filter values are whole numbers where they should be", category="error")
            return False
        if not filter =="":
            filter = int(filter)
            if filter <= 0:
                flash("Please make sure filter values are positive", category="error")
                return False
                
    return True