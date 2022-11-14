from scholarly import scholarly
#may use an an aid to validation
from flask import flash

def searchCheck(searchQuery, overNStudies, resultAmount):
    #search input validation on server side, ideally should be locally but I am more familiar with python and I can make use of flask here
    if searchQuery.strip() == None or searchQuery.strip() == "":
        flash("Please enter a valid search", category="error")
        return validationResponse(False)
    elif can_convert_to_int(overNStudies) == False:
        flash("Please enter an integer in the 'author has over n studies' field", category="error")
        return validationResponse(False)
    elif can_convert_to_int(resultAmount) == False and resultAmount.strip() != "":
        flash("Please enter an integer in the 'amount of search results' field", category="error")
        return validationResponse(False)
    else:
        if resultAmount.strip() == "":
            resultAmount = 11
        overNStudies = int(overNStudies)
        resultAmount = int(resultAmount)
        return validationResponse(True, overNStudies, resultAmount)

#function checks of an item can be converted into an integer, for inputs which could be anything but are meant to be used in calculations      
def can_convert_to_int(string):
    try:
        int(string)

        return True
    except ValueError:
        return False

#this class gives me a neater way to return the relevant values from a validation check
class validationResponse():
    def __init__(self, state, overNStudies=None, resultAmount=None):
        self.state = state
        self.overNStudies = overNStudies
        self.resultAmount = resultAmount
