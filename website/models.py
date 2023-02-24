from . import db    
#any reference to . indicates this package, will be in __init__.py file

class Study(db.Model):
    #creating study entity to store study data in once retrieved from a search
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    abstract = db.Column(db.String(2000))
    pubYear = db.Column(db.Integer)
    publisher = db.Column(db.String(40))
    numCitations = db.Column(db.Integer)
    gsRank = db.Column(db.Integer)
    authorStrings = db.Column(db.String(50))
    levelOfAffiliation = db.Column(db.Integer)
    governmentAffiliation = db.Column(db.Boolean)
    government = db.Column(db.String(30))
    affiliationNature = db.Column(db.String(50))
    peerReviewed = db.Column(db.Boolean)
    noConflictInterest = db.Column(db.Boolean)
    conflictDisclosed = db.Column(db.Boolean)
    notExternallyFunded = db.Column(db.Boolean)
    conflictEvidence = db.Column(db.String(100))
    publisherRating = db.Column(db.Integer)
    daysSinceCite = db.Column(db.Integer)
    citationsOfTopCiters = db.Column(db.Integer)
    government_id = db.Column(db.Integer, db.ForeignKey('government.id'))
    journal_id = db.Column(db.Integer, db.ForeignKey('journal.id'))
    authors = db.relationship('AuthorStudyLink')
    dateOfAddition = db.Column(db.Date)


    def __repr__(self):
        return f'<Study: {self.title}>'

class Author(db.Model):
    #the same author will have multiple studies so a separate table must be made for them, also a useful place to store other 
    #information about them to determine their reputation
    id = db.Column(db.Integer, primary_key=True)
    authorName = db.Column(db.String(50))
    authorCitations = db.Column(db.Integer)
    authorCitations5y = db.Column(db.Integer)
    hIndex = db.Column(db.Integer)
    hIndex5y = db.Column(db.Integer)
    i10index = db.Column(db.Integer)
    i10index5y = db.Column(db.Integer)
    authorYearsSinceCite = db.Column(db.Integer)
    careerLength = db.Column(db.Integer)
    authorCitationsThisYear = db.Column(db.Integer)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    studies = db.relationship('AuthorStudyLink')

    def __repr__(self):
        return f'<Author: {self.authorName, self.authorCitations, self.organisation_id}>'

class AuthorStudyLink(db.Model):
    #link table for Study and Author entities as they have a many to many relationship
    #composite primary key of both the foreign keys and an id
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey('study.id'), primary_key = True)

    def __repr__(self):
        return f'<AuthorStudyLink: {self.author_id, self.study_id}>'

class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orgName = db.Column(db.String)
    #impactFactor = db.Column(db.Integer)
    authors = db.relationship('Author')

    def __repr__(self):
        return f'<Organisation: {self.orgName}>'
    
class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journalName = db.Column(db.String(50))
    #peerReviewed = db.Column(db.Boolean)
    studies = db.relationship('Study')

    def __repr__(self):
        return f'<Journal: {self.journalName}>'
    
class Government(db.Model):
    #the same goverment will have multiple studies so a separate table must be made for them, also a useful place to store other 
    #information about them to determine their reputation
    id = db.Column(db.Integer, primary_key=True)
    government = db.Column(db.String(20))
    governmentReputation = db.Column(db.Integer)
    correspondingDomain = db.Column(db.String(5))

    def __repr__(self):
        return f'<Government: {self.government, self.correspondingDomain}>'
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    dateOfAddition = db.Column(db.Date)

    def __repr__(self):
        return f'<Government: {self.text, self.dateOfAddition}>'

class Journals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journalTitle = db.Column(db.String(30))
    issns = db.Column(db.String(30))
    sjrScore = db.Column(db.Float)
    journalHIndex = db.Column(db.Integer)
    publisherName = db.String(db.String(30))

    def __repr__(self):
        return f'<Journal: {self.journalTitle}>'

class lastUpdates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastJournalUpdate = db.Column(db.Date)

    def __repr__(self):
        return f'<Journal: {self.lastJournalUpdate}>'