from . import db    
#any reference to . indicates this package, will be in __init__.py file

class Study(db.Model):
    #creating study entity to store study data in once retrieved from a search
    id = db.Column(db.Integer, primary_key=True)
    searchDepth = db.Column(db.Integer)
    governmentAffiliation = db.Column(db.Boolean)
    title = db.Column(db.String(50))
    abstract = db.Column(db.String(2000))
    government_id = db.Column(db.Integer, db.ForeignKey('government.id'))
    
class Author(db.Model):
    #the same author will have multiple studies so a separate table must be made for them, also a useful place to store other 
    #information about them to determine their reputation
    id = db.Column(db.Integer, primary_key=True)
    authorName = db.Column(db.String(50))
    authorStudyCount = db.Column(db.Integer)
    journalOrganisation_id = db.Column(db.Integer, db.ForeignKey('journalorganisation.id'))


class AuthorStudyLink(db.Model):
    #link table for Study and Author entities as they have a many to many relationship
    #composite primary key of both the foreign keys and an id
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey('study.id'), primary_key = True)

class JournalOrganisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peerReviewed = db.Column(db.Boolean)
    impactFactor = db.Column(db.Integer)

class Government(db.Model):
    #the same goverment will have multiple studies so a separate table must be made for them, also a useful place to store other 
    #information about them to determine their reputation
    id = db.Column(db.Integer, primary_key=True)
    government = db.Column(db.String(20))
    governmentReputation = db.Column(db.Integer)
    correspondingDomain = db.Column(db.String(5))
    


