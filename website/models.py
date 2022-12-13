from . import db    
#any reference to . indicates this package, will be in __init__.py file

class Study(db.Model):
    #creating study entity to store study data in once retrieved from a search
    id = db.Column(db.Integer, primary_key=True)
    searchDepth = db.Column(db.Integer)
    governmentAffiliation = db.Column(db.Integer)
    title = db.Column(db.String(50))
    abstract = db.Column(db.String(2000))
    pub_year = db.Column(db.Integer)
    publisher = db.Column(db.String(40))
    num_citations = db.Column(db.Integer)
    gs_rank = db.Column(db.Integer)
    government_id = db.Column(db.Integer, db.ForeignKey('government.id'))
    journal_id = db.Column(db.Integer, db.ForeignKey('journal.id'))
    authors = db.relationship('AuthorStudyLink')

    def __repr__(self):
        return f'<Study: {self.title, self.searchDepth, self.abstract, self.pub_year, self.publisher, self.num_citations, self.gs_rank, self.governmentAffiliation, self.government_id}>'

class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orgName = db.Column(db.String)
    #impactFactor = db.Column(db.Integer)
    scholar_id = db.Column(db.String)
    authors = db.relationship('Author')

    def __repr__(self):
        return f'<Organisation: {self.orgName}>'
    

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    journalName = db.Column(db.String)
    #peerReviewed = db.Column(db.Boolean)
    studies = db.relationship('Study')

    def __repr__(self):
        return f'<Journal: {self.journalName}>'
    
class Author(db.Model):
    #the same author will have multiple studies so a separate table must be made for them, also a useful place to store other 
    #information about them to determine their reputation
    id = db.Column(db.Integer, primary_key=True)
    authorName = db.Column(db.String(50))
    authorCitations = db.Column(db.Integer)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    studies = db.relationship('AuthorStudyLink')

    def __repr__(self):
        return f'<Author: {self.authorName, self.authorCitations, self.Organisation_id}>'

class AuthorStudyLink(db.Model):
    #link table for Study and Author entities as they have a many to many relationship
    #composite primary key of both the foreign keys and an id
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey('study.id'), primary_key = True)

    def __repr__(self):
        return f'<AuthorStudyLink: {self.author_id, self.study_id}>'


class Government(db.Model):
    #the same goverment will have multiple studies so a separate table must be made for them, also a useful place to store other 
    #information about them to determine their reputation
    id = db.Column(db.Integer, primary_key=True)
    government = db.Column(db.String(20))
    governmentReputation = db.Column(db.Integer)
    correspondingDomain = db.Column(db.String(5))

    def __repr__(self):
        return f'<Government: {self.government, self.correspondingDomain}>'
    


#&"C:\Users\luker\OneDrive\Documents\Software Tools\Sqllite\sqlite-tools-win32-x86-3390400\sqlite3.exe"
#database tool

