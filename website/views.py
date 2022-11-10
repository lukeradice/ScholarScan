from flask import Blueprint, render_template, request
#Blueprint allows us to define the URLs across multiple files
#render template allows us to render externally written html templates
#request allows access to incoming web request data
from . import search, searchCheck

views = Blueprint("views", __name__)

@views.route("/", methods=["POST", "GET"])
def scholarScan():
    if request.method == 'POST':
        searchQuery = request.form.get('searchQuery')
        peerReviewed = request.form.get('peerReviewed')
        governmentAffiliation = request.form.get('governmentAffiliation')
        overNStudies = request.form.get('overNStudies')
        resultAmount = request.form.get('resultAmount')
        if searchCheck.searchCheck(searchQuery, overNStudies, resultAmount):
            if resultAmount != None:
                search.search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount)
            else:
                search.search(searchQuery, peerReviewed, governmentAffiliation, overNStudies, resultAmount=50)
        else:
            None
            #some sort of reset needed, as you want the ability to reinput need understanding of decorator, flashing of error will occur in searchCheck module

    return render_template("main.html")

@views.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")
