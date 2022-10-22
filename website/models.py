from . import db    
#any reference to . indicates this package, will be in __init__.py file

class Study(db.Model):
    #creating study entity to store study data in once retrieved from a search
    id = db.Column(db.Integer, primary_key=True)
    credListed = db.Column(db.Boolean)
    domainSig = db.Column(db.String(10)) 

