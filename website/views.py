from flask import Blueprint, render_template, request, flash
#Blueprint allows us to define the URLs across multiple files
#render template allows us to render externally written html templates
#request allows access to incoming web request data
from .search.search import search
from .search.searchCheck import searchCheck
from .scoreAndSort.scoreAndSort import scoreAndSort

views = Blueprint("views", __name__)

#the python script for the main page, includes the search functionality
@views.route("/", methods=["POST", "GET"])
def scholarScan():
    if request.method == 'POST':
        #retrieving the values of the non-checkbox filters from the active web form search request
        searchQuery = request.form.get('searchQuery')
        # overNStudies = request.form.get('overNStudies')
        # resultAmount = request.form.get('resultAmount')
        # minCitations = request.form.get('minCitations')
        # maxGsRank = request.form.get('maxGsRank')
        # minVersions = request.form.get('minVersions')
        # daysSinceCite = request.form.get('daysSinceCite')
        # minPubYear = request.form.get('minPubYear')
        # minAuthCitations = request.form.get('minAuthCitations')

        #retrieving and determining the values of the checkbox filters
        checkBoxes = request.form.getlist('checkbox')
        # if "peerReviewed" in checkBoxes:
        #     peerReviewed = True
        # else:
        #     peerReviewed = False
        # if "governmentAffiliation" in checkBoxes:
        #     governmentAffiliation = True
        # else:
        #     governmentAffiliation = False
        
        #little for loop which determines boolean values based off its 
        # corresponding checkbox input

        #more effiicient/sensical solutions to storage and addage of filters
        filters = {
            'overNStudies': request.form.get('overNStudies'),
            'resultAmount': request.form.get('resultAmount'),
            'minCitations': request.form.get('minCitations'),
            'overNStudies': request.form.get('overNStudies'),
            'resultAmount': request.form.get('resultAmount'),
            'minCitations': request.form.get('minCitations'),
            'maxGsRank': request.form.get('maxGsRank'),
            'daysSinceCite': request.form.get('daysSinceCite'),
            'minPubYear': request.form.get('minPubYear'),
            'minAuthCitations': request.form.get('minAuthCitations'),
            'peerReviewed': None,
            'governmentAffiliation': None, 
            'conflictDisclosed': None,
            'conflictInterest': None,
            'fundingDisclosed': None,
            'notExternallyFunded': None
        }
        booleanFilters = ["peerReviewed", "governmentAffiliation", "conflictDisclosed", 
                          "conflictInterest", "fundingDisclosed", "notExternallyFunded"]
        for filter in booleanFilters:
            if filter in checkBoxes:
                filters[filter] = True
            else:
                filters[filter] = False

        #input validation
        validation = searchCheck(searchQuery, filters.get('minCitations'), filters.get('maxGsRank'), 
            filters.get('minVersions'), filters.get('daysSinceCite'), filters.get('minPubYear'), 
            filters.get('minAuthCitations'), filters.get('resultAmount'), filters.get('overNStudies'))
        if validation:
            #search is intiated
            flash("Search completed", category="success")
            #changes to search function arguments
            searchedStudies = search(searchQuery, filters.get('maxGsRank')) 
            searchedAndSortedStudies = scoreAndSort(searchedStudies, filters, filters.get('resultAmount'))
            return render_template("main.html", searchedAndSortedStudies=searchedAndSortedStudies)
            #some sort of reset needed, as you want the ability to reinput need understanding of decorator, flashing of error will occur in searchCheck module
        
    return render_template("main.html", searchedandSortedStudies=[])

@views.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")

