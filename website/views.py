from flask import Blueprint, render_template, request, flash
#Blueprint allows us to define the URLs across multiple files
#render template allows us to render externally written html templates
#request allows access to incoming web request data
from .search.search import search
from .search.searchCheck import searchCheck
from .scoreAndSort.scoreAndSort import scoreAndSort
from .models import Feedback
from datetime import datetime, date
from . import db


views = Blueprint("views", __name__)

#the python script for the main page, includes the search functionality
@views.route("/", methods=["POST", "GET"])
def scholarScan():
    if request.method == 'POST':
        
        searchQuery = request.form.get('searchQuery')

        #retrieving and determining the values of the checkbox filters
        checkBoxes = request.form.getlist('checkbox')

        #retrieving the values of the non-checkbox filters from the active web form search request
        #more effiicient/sensical solutions to storage and addage of filters
        filters = {
            'minCareerLength': request.form.get('minCareerLength'),
            'resultAmount': request.form.get('resultAmount'),
            'minCitations': request.form.get('minCitations'),
            'maxGsRank': request.form.get('maxGsRank'),
            'maxDaysSinceCite': request.form.get('daysSinceCite'),
            'minPubYear': request.form.get('minPubYear'),
            'minAuthCitations': request.form.get('minAuthCitations'),
            'peerReviewed': None,
            'governmentAffiliation': None, 
        }

        booleanFilters = ["peerReviewed", "governmentAffiliation"]
        for filter in booleanFilters:
            if filter in checkBoxes:
                filters[filter] = True
            else:
                filters[filter] = False

        #input validation
        validation = searchCheck(searchQuery, filters.get('minCitations'), filters.get('maxGsRank'), filters.get('maxDaysSinceCite'),
                                filters.get('minPubYear'), filters.get('minAuthCitations'), filters.get('resultAmount'),
                                filters.get('minCareerLength'))
        if validation:
            #search is intiated
            flash("Search completed", category="success")
            #changes to search function arguments
            print(datetime.now())
            searchedStudies = search(searchQuery, filters.get('maxGsRank')) 
            searchedAndSortedStudies = scoreAndSort(searchedStudies, filters, filters.get('resultAmount'))
            print(datetime.now())
            return render_template("main.html", searchedAndSortedStudies=searchedAndSortedStudies)
        
    return render_template("main.html", searchedandSortedStudies=[])

@views.route("/about", methods=["POST", "GET"])
def about():
    if request.method == 'POST':
        feedback = request.form.get("feedback")
        todaysDate = date.today()
        new_feedback = Feedback(text=feedback, dateOfAddition=todaysDate)
        db.session.add(new_feedback )
        db.session.commit()
        print(Feedback.query.all())
    return render_template("about.html")

