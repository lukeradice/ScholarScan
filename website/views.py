from flask import Blueprint, render_template
#Blueprint allows us to define the URLs across multiple files
#redner template allows us to render externally written html templates

views = Blueprint("views", __name__)

@views.route("/", methods=["POST", "GET"])
def scholarScan():
    return render_template("main.html")

@views.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")
