# from scholarly import scholarly, ProxyGenerator
# from scholarly.publication_parser import PublicationParser
# from datetime import datetime
# from website import db
from datetime import datetime, date
import requests
from bs4 import BeautifulSoup
 
# pg = ProxyGenerator()
# success = pg.ScraperAPI('d07eb644f66c41a5ebf97168156dc1d5')
# success = pg.FreeProxies()
# scholarly.use_proxy(pg)
# if success:
#     print("success")
    #print(datetime.now())
    #authorName_query = scholarly.search_author('Z Meng')
# searchQuery = scholarly.search_author("Daniel Kahneman")
#     # #author = next(authorName_query) 
# author = next(searchQuery)
#     # #scholarly.pprint(scholarly.fill(author, sections=['publications']))
# print(author)

    # search_query = scholarly.search_author('Steven A Cholewiak')
    # author = next(search_query)
    # scholarly.pprint(scholarly.fill(author, sections=['basics', 'indices', 'coauthors']))
    # for i in range (0, 2):
    #     study = next(studies)
    #     print(study)
    #     print(datetime.now())

# pg = ProxyGenerator()
# success = pg.ScraperAPI('0a5c362e42b4b14c12595210593f9724')
# scholarly.use_proxy(pg)
# if success:
#     print("success")
#     search_query = scholarly.search_pubs('vegan diet')
#     studyinfo = next(search_query)
#     pub = scholarly.fill(studyinfo)
#     parser = PublicationParser(pub)
#     print(pub)
#     # citationList = studyinfo.citedby()
#     x = parser.citedby(pub)
#     print(next(x))
#     # print(citationList)
#     # print(next(citationList))

# class Journals(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     issnOne = db.Column(db.String(30))
#       issnOne = db.Column(db.String(30))
#     sjrScore = db.Column(db.Float)
#     journalHIndex = db.Column(db.Integer)
#     publisherName = db.String(db.String(30))

# from .models import Journal
#         #allows the adding of the domains to the database outside of a view function, a flask sql_alchemy requirement
#         with app.app_context():
#             myfile = open("correspondingdomain.txt", "r")
#             myline = myfile.readline()
#             while myline:
#                 pair = myline.split(",")
#                 correspondingDomain = pair[0].strip()
#                 government = pair[1].strip()
#                 new_government = Government(government=government, correspondingDomain=correspondingDomain)
#                 db.session.add(new_government)
#                 db.session.commit()
#                 myline = myfile.readline()
                # myfile.close()  

#Title,Issn,SJR,H index,Country,Publisher

# myfile = open("sjrJournalData.txt", "r")
# myline = myfile.readline()
# while myline:
#     record = myline.split(",")
#     print(record)
#     print(len(record))
#     title = record[0]
#     i = 0
#     if len(record) == 7:
#         issnOne = record[1].replace('"', '')
#         i = 1
#     elif len(record) == 8:
#         issnOne = record[1].replace('"', '')
#     elif len(record) == 9:
#         try:
#             i = -1
#             title = title.replace('"', '') + record[1].replace('"', '')
#             issnOne = record[1 - i].replace('"', '')
#         except ValueError:

#     elif len(record) == 10:
#         i = -2
#         title = title.replace('"', '') + record[1] + record[2].replace('"', '')
#         issnOne = record[1 - i].replace('"', '')
#     elif len(record) == 11:
#         i = -3
#         title = title.replace('"', '') + record[1] + record[2] + record[3].replace('"', '')
#         issnOne = record[1 - i].replace('"', '')   
#     issnTwo = record[2 - i].replace('"', '')
#     print(title, "title")
#     print(issnOne, "issn")
#     print(issnTwo, "issn")
#     sjrScore = float(record[3 - i].replace('"', '') + "." + record[4 - i].replace('"', ''))
#     print(sjrScore, "sjr")
#     journalHIndex = record[5 - i].replace('"', '')
#     print(journalHIndex, "hIndex")
#     government = record[6 - i]
#     print(government, "government")
#     publisher = record[7 - i]
#     print(publisher, "publisher")
#     myline = myfile.readline()
# myfile.close()  

myProxies = {
"http": "http://scraperapi:d1318296d4d6fc658b1e373287da15fe@proxy-server.scraperapi.com:8001",
"https": "http://scraperapi:d1318296d4d6fc658b1e373287da15fe@proxy-server.scraperapi.com:8001"
}

# year = input("year")
# url = "https://www.scimagojr.com/journalrank.php?year=" + year
# html = requests.get(url, proxies=myProxies, verify=False)
# page = BeautifulSoup(html.content, 'html.parser')
# relevantId = page.find(class_='ranking_body')
# buttons = relevantId.find_all(class_='button')
# myButton = buttons[1]
# downloadUrl = myButton.attrs['href']

import csv

#url for the csv containing sjr data for scholarly journals
#this url should be the same every year so don't need to scrape it
url ="https://www.scimagojr.com/journalrank.php?out=xls"

#the url variable only stores the download link for the csv file so have to use requests to get the info
#requests.Session provides cookie persistence which is useful when scraping
with requests.Session() as s:
    #get request for the download url
    download = s.get(url, proxies=myProxies, verify=False)
    #defines the lines of the csv file as being character set utf-8 and puts them as a unique
    #item in the list
    lines = (line.decode('utf-8') for line in download.iter_lines())

#interpretation of csv data, delimiter is what separates each element and quotechar links elements
#that are only linked by speech marks
journalData = csv.reader(lines, delimiter=';', quotechar='"')
i = 0
# test = True
for row in journalData:
    #the use of variable is to ensure the top row isn't scraped as that is the headers
    #so will cause an error trying to convert those strings to integers
    if i != 0:
        #the extraction of the csv row values that I will store for each Journals record
        title = row[2]
        issns = row[4]
        sjrScore = int(row[5].replace(",","") or "0")
        journalHIndex = int(row[7])
        government = row[15]
        publisher = row[17]
 
        # print(title)
        # print(issns)
        # print(sjrScore)
        # print(journalHIndex)
        # print(government)
        # print(publisher)
        # print()
    # elif i == 5:
        # test = False
    i = i + 1
lastJournalUpdate = date.today()

#Rank;Sourceid;Title;Type;Issn;SJR;SJR Best Quartile;H index;Total Docs. (2021);Total Docs. (3years);Total Refs.;Total Cites (3years);Citable Docs. (3years);Cites / Doc. (2years);Ref. / Doc.;Country;Region;Publisher;Coverage;Categories
# 1;28773;"Ca-A Cancer Journal for Clinicians";journal;"15424863, 00079235";56,204;Q1;182;41;121;4006;17959;78;186,75;97,71;United States;Northern America;"Wiley-Blackwell";"1950-2021";"Hematology (Q1); Oncology (Q1)"

#float("2,5".replace(',', '.'))