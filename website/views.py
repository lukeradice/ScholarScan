from flask import Blueprint, render_template, request, flash
#Blueprint allows us to define the URLs across multiple files
#render template allows us to render externally written html templates
#request allows access to incoming web request data
from .search.search import search
from .search.searchCheck import searchCheck

views = Blueprint("views", __name__)

#the python script for the main page, includes the search functionality
@views.route("/", methods=["POST", "GET"])
def scholarScan():
    if request.method == 'POST':
        #retrieving the values of the non-checkbox filters from the active web form search request
        searchQuery = request.form.get('searchQuery')
        overNStudies = request.form.get('overNStudies')
        resultAmount = request.form.get('resultAmount')
        

        #retrieving and determining the values of the checkbox filters
        checkBoxes = request.form.getlist('checkbox')
        if "peerReviewed" in checkBoxes:
            peerReviewed = True
        else:
            peerReviewed = False
        if "governmentAffiliation" in checkBoxes:
            governmentAffiliation = True
        else:
            governmentAffiliation = False


        #input validation
        validation = searchCheck(searchQuery, overNStudies, resultAmount)
        if validation.state:
            #search is intiated
            flash("Search intiated", category="success")
            searchedStudies = search(searchQuery, peerReviewed, governmentAffiliation, validation.overNStudies, validation.resultAmount) 
            return render_template("main.html", searchedStudies=searchedStudies)
            #some sort of reset needed, as you want the ability to reinput need understanding of decorator, flashing of error will occur in searchCheck module
        
    return render_template("main.html", searchedStudies=[])

@views.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")

