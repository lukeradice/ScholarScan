import requests
from bs4 import BeautifulSoup


def GetJournalSearchAddress(journalName):
    journalNameWords = journalName.split(" ")
    journalSearchAddress = journalNameWords[0]
    for word in journalNameWords:
        if journalNameWords.index(word) == 0:
            pass
        else:
            if journalNameWords.index(word) == (len(journalNameWords) - 1):
                word = "%20" + word + "%20"
            else:
                word = "%20" + word
            journalSearchAddress = journalSearchAddress + word
    return journalSearchAddress

journalName = input("What is the journal name?")
journalSearchAddress = GetJournalSearchAddress(journalName)
print(journalSearchAddress)

url = "https://uh4jc3de5m.search.serialssolutions.com/ejp/?libHash=UH4JC3DE5M#/search/?searchControl=title&searchType=alternate_title_begins&criteria=" + journalSearchAddress + "&language=en-US"
html = requests.get(url)
s = BeautifulSoup(url.content, 'html.parser')
        

results = s.find()