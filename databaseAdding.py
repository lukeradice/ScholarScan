#from website import create_app, db
#from website.models import Government

#app = create_app()

#this condition is met if we run this file
#if __name__ == "__main__":

 #   f = open('correspondingdomain.txt', 'r')
  #  for line in f:
   #     x = (f.readline())
    #    pair = x.split(",")
       # correspondingDomain = pair[0].strip()
      #  government = pair[1].strip()
    #    new_government = Government(government=government, correspondingDomain=correspondingDomain)
     #   db.session.add(new_government)
      #  db.session.commit()
   # f.close()

# myfile = open("correspondingdomain.txt", "r")
# myline = myfile.readline()
# while myline:
#     pair = myline.split(",")
#     correspondingDomain = pair[0].strip()
#     government = pair[1].strip()
#     new_government = Government(government=government, correspondingDomain=correspondingDomain)
#     db.session.add(new_government)
#     db.session.commit()
#     myline = myfile.readline()
# myfile.close()   


#   print(db.session.execute(db.select(Government).filter_by(correspondingDomain='.ni')).first())
#     print("1")
#     print(db.session.execute(db.select(Government).filter_by(correspondingDomain='.ni')).scalars())
#     print("2")
#     print(db.session.execute(db.select(Government).filter_by(correspondingDomain='.ni')).all())
#     print("3")
#     print(db.session.execute(db.select(Government).filter_by(correspondingDomain='.ni')).one())
#     print("4")
#     print(Government.query.all())
#     print("5")
#     print(Government.query.filter_by(government="Nigeria").count())
#     print("6")
#     countryToFind = Government.query.filter(Government.correspondingDomain == '.ni').one()
#     print(countryToFind.government)

#     def __repr__(self):
#    # return f'<Government: {self.government}'