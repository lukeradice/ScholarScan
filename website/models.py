from . import db    
#any reference to . indicates this package, will be in __init__.py file

class Study(db.Model):
    #creating study entity to store study data in once retrieved from a search
    id = db.Column(db.Integer, primary_key=True)
    searchDepth = db.Column(db.Integer)
    peerReviewed = db.Column(db.Boolean)
    governmentAffiliation = db.Column(db.Boolean)
    governmentReputation = db.Column(db.String)
    authorStudyCount = db.Column(db.Integer)


