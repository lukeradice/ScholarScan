import requests
from bs4 import BeautifulSoup

    #d1318296d4d6fc658b1e373287da15fe
#ffe4db9384d81641640ddb6976087dae
#57465d56ed88087e0fd9239e56ace84b
#d07eb644f66c41a5ebf97168156dc1d5
#f171d0c5dd2ec4eb81c87ab25875fdd9

myProxies = {
"http": "http://scraperapi:d1318296d4d6fc658b1e373287da15fe@proxy-server.scraperapi.com:8001",
"https": "http://scraperapi:d1318296d4d6fc658b1e373287da15fe@proxy-server.scraperapi.com:8001"
}




# citedby_url = '/scholar?cites=10898304115650535979&as_sdt=5,33&sciodt=0,33&hl=en'
# #peerCheckUrl = "https://uh4jc3de5m.search.serialssolutions.com/ejp/?libHash=UH4JC3DE5M#/search/?searchControl=title&searchType=alternate_title_begins&criteria=" + journalSearchAddress + "&language=en-US"
# citationUrl = 'https://scholar.google.com/' + citedby_url
# html = requests.get(citationUrl)
# #print(html.text)
# citationPage = BeautifulSoup(html.content, 'html.parser')

# # #implementation to calculate the value for the citationsOfTopCiters attribute
# results = citationPage.find(id="gs_res_ccl_mid")
# citationNumbers = results.find_all('a')
# mostRecentCiters = []
# for num in citationNumbers:
#     aText = num.text
#     if aText.startswith('Cited by') and len(mostRecentCiters) <= 3:
#         citations = int(aText[8:len(aText)])
#         mostRecentCiters.append(citations)
# print(mostRecentCiters)
# #need to make sure list index doesn't go out of range, could be few citations that have no number

# #WORKING IMPLEMENTATION TO GET daysSinceCite
# citedCode = citedby_url[15:35]
# citesByDate_url = 'https://scholar.google.com/scholar?hl=en&as_sdt=5,33&sciodt=0,33&cites=' + citedCode + '&scipsc=&q=&scisbd=1'
# print(citesByDate_url)
# html = requests.get(citesByDate_url)
# citedByDatePage = BeautifulSoup(html.content, 'html.parser')
# results = citedByDatePage.find(id="gs_res_ccl_mid") 
# ageInfo = results.find_next('span', class_= 'gs_age')
# #, class_='gs_age'
# if ageInfo:
#     daysSinceCite = ageInfo


# firstName = "David E"
# if len(firstName.split(" ")) > 1:
#     firstName = firstName.replace(" ", "+")
# surname = "Smith"
# #I want to make sure there's only one author result or less than a certain amount as I can't filter results so I don't want getting of this information to take too long
# # scopusUrlOne = "https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sid=4e66b492b7c83a2d124bbb9041894fb0&sot=al&sdt=al&sl=43&s=AUTHLASTNAME%28Viehman%29+AND+AUTHFIRST%28Greg+E%29&st1=Viehman&st2=Greg+E&orcidId=&selectionPageSearch=anl&reselectAuthor=false&activeFlag=true&showDocument=false&resultsPerPage=20&offset=1&jtp=false&currentPage=1&previousSelectionCount=0&tooManySelections=false&previousResultCount=0&authSubject=LFSC&authSubject=HLSC&authSubject=PHSC&authSubject=SOSC&exactAuthorSearch=false&showFullList=false&authorPreferredName=&origin=searchauthorfreelookup&affiliationId=&txGid=46ecbbaa461c6be184b3f77a92d3dfcf"
# # scopusUrlTwo = "https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sid=efc099b051e522c3e4a9de78db39906e&sot=al&sdt=al&sl=40&s=AUTHLASTNAME%28Smith%29+AND+AUTHFIRST%28David%29&st1=Smith&st2=David&orcidId=&selectionPageSearch=anl&reselectAuthor=false&activeFlag=true&showDocument=false&resultsPerPage=20&offset=1&jtp=false&currentPage=1&previousSelectionCount=0&tooManySelections=false&previousResultCount=0&authSubject=LFSC&authSubject=HLSC&authSubject=PHSC&authSubject=SOSC&exactAuthorSearch=false&showFullList=false&authorPreferredName=&origin=searchauthorfreelookup&affiliationId=&txGid=0f1c54fc4ec237a4107d1b503667b21e"
# scopusUrlOne = "https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sot=al&sdt=al&sl=40&s=AUTHLASTNAME%28"+surname+"%29+AND+AUTHFIRST%28"+firstName+"%29&st1="+surname+"&st2="+ firstName+"&orcidId=&selectionPageSearch=anl&reselectAuthor=false&activeFlag=true&showDocument=false&resultsPerPage=20&offset=1&jtp=false&currentPage=1&previousSelectionCount=0&tooManySelections=false&previousResultCount=0&authSubject=LFSC&authSubject=HLSC&authSubject=PHSC&authSubject=SOSC&exactAuthorSearch=false&showFullList=false&authorPreferredName=&origin=searchauthorfreelookup&affiliationId="
# scopusUrlTwo = "https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sot=al&sdt=al&sl=40&s=AUTHLASTNAME%28"+surname+"%29+AND+AUTHFIRST%28"+firstName+"%29&st1="+surname+"&st2="+ firstName+"&orcidId=&selectionPageSearch=anl&reselectAuthor=false&activeFlag=true&showDocument=false&resultsPerPage=20&offset=1&jtp=false&currentPage=1&previousSelectionCount=0&tooManySelections=false&previousResultCount=0&authSubject=LFSC&authSubject=HLSC&authSubject=PHSC&authSubject=SOSC&exactAuthorSearch=false&showFullList=false&authorPreferredName=&origin=searchauthorfreelookup&affiliationId="

# print(scopusUrlOne)


# def getAuthorNameList(authorList):
#     authorsTogether = ""
#     for author in authorList:
#         authorsTogether = authorsTogether + author
#     realAuthorsList = authorsTogether.split(" and ")
#     return realAuthorsList
# def scopusScrape(authorList):
#     for author in authorList:
#         surnameUpperBound = author.find(" ")
#         surname = author[0:surnameUpperBound]
#         print("surname", surname)
#         firstName = author[surnameUpperBound+1:]
#         if len(firstName.split(" ")) > 1:
#             firstName = firstName.replace(" ", "+")
#         print("first name", firstName)
#         scopusUrlOne = "https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sot=al&sdt=al&sl=40&s=AUTHLASTNAME%28"+surname+"%29+AND+AUTHFIRST%28"+firstName+"%29&st1="+surname+"&st2="+firstName+"&orcidId=&selectionPageSearch=anl&reselectAuthor=false&activeFlag=true&showDocument=false&resultsPerPage=20&offset=1&jtp=false&currentPage=1&previousSelectionCount=0&tooManySelections=false&previousResultCount=0&authSubject=LFSC&authSubject=HLSC&authSubject=PHSC&authSubject=SOSC&exactAuthorSearch=false&showFullList=false&authorPreferredName=&origin=searchauthorfreelookup&affiliationId="
#         print(scopusUrlOne)
#         html = requests.get(scopusUrlOne, proxies=myProxies, verify=False)
#         print(html.text)
#         searchAuthorPage = BeautifulSoup(html.content, 'html.parser')
#         print(searchAuthorPage.body)
#         numberSection = searchAuthorPage.find(id="container")
#         if numberSection:
#             numResults = numberSection.find_all('span', class_="resultsCount")
#             print(numResults)
#             authorResultOne = searchAuthorPage.find(id="resultDataRow1")
#             if authorResultOne:
#                 topResult = authorResultOne.find_all(class_="docTitle")
#                 topResultLink = topResult.attrs['href']
#                 print(topResultLink)
#             else:
#                 print("searched blocked, or no results")
#         else:
#             print("searched blocked")

# listAuthors = ['Flynn', ' Timothy Corcoran and Petros', ' James and Clark', ' Robert E and Viehman', ' Greg E']
# authorList = ['Glick-Bauer', ' Marian and Yeh', ' Ming-Chin']
# realAuthorstwo = ['Marian Glick-Bauer', 'Ming-Chin Yeh']

# authorList = getAuthorNameList(listAuthors)
# authorNames = scopusScrape(authorList)




#/scholar?cites=10898304115650535979&as_sdt=5,33&sciodt=0,33&hl=en
#/scholar?hl=en&as_sdt=5,33&sciodt=0,33&cites=10898304115650535979&scipsc=&q=&scisbd=1

#/scholar?cites=14704171677942009626&as_sdt=5,33&sciodt=0,33&hl=en
#/scholar?hl=en&as_sdt=5,33&sciodt=0,33&cites=14704171677942009626&scipsc=&q=&scisbd=1 

#dummyStudy1 = {'container_type': 'Publication', 'source': "<PublicationSource.PUBLICATION_SEARCH_SNIPPET: 'PUBLICATION_SEARCH_SNIPPET'>", 'bib': {'title': 'Nose picking and nasal carriage of Staphylococcus aureus', 'author': 'Wertheim, Heiman FL and Van Kleef, Menno and Vos, Margreet C and Ott, Alewijn and Verbrugh, Henri A and Fokkens, Wytske', 'pub_year': '2006', 'venue': 'Infection Control & …', 'abstract': 'part of the nose, we considered the habit of nose picking as a  a positive correlation between  nose picking and S. aureus  in a larger cohort with predefined criteria for nose picking.', 
# 'publisher': 'Cambridge University Press', 'pages': '863--867', 'number': '8', 'volume': '27', 'journal': 'Infection Control \\& Hospital Epidemiology', 
# 'pub_type': 'article', 'bib_id': 'wertheim2006nose'}, 'filled': True, 'gsrank': 1,
#  'pub_url': 'https://www.cambridge.org/core/journals/infection-control-and-hospital-epidemiology/article/nose-picking-and-nasal-carriage-of-staphylococcus-aureus/DC21FFA771693C772308530D2B1A1452', 
# 'author_id': ['JVFGW64AAAAJ', '', 'RAV-bbIAAAAJ', ''], 'url_scholarbib': '/scholar?hl=en&q=info:KyKH-9mNPpcJ:scholar.google.com/&output=cite&scirp=0&hl=en', 
# 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3Dnose%2Bpicking%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=KyKH-9mNPpcJ&ei=gQ2zY6CMLc6TywSl1LXoCA&json=', 
# 'num_citations': 90, 
# 'citedby_url': '/scholar?cites=10898304115650535979&as_sdt=5,33&sciodt=0,33&hl=en', 
# 'url_related_articles': '/scholar?q=related:KyKH-9mNPpcJ:scholar.google.com/&scioq=nose+picking&hl=en&as_sdt=0,33', 
# 'eprint_url': 'https://www.academia.edu/download/46395935/Nose_picking_and_nasal_carriage_of_Staph20160611-15499-1ngo5wz.pdf'}

#urlOne = http://uh4jc3de5m.search.serialssolutions.com/ejp/?libHash=UH4JC3DE5M#/search/?searchControl=title&searchType=alternate_title_equals&criteria=Journal%20OF%20VISION&titleType=JOURNALS&filterBy=All&beginPage=0&language=en-US
#urlTwo = http://uh4jc3de5m.search.serialssolutions.com/ejp/?libHash=UH4JC3DE5M#/search/?searchControl=title&searchType=alternate_title_equals&criteria=Nature&titleType=JOURNALS&filterBy=All&beginPage=0&language=en-US

#function to get link to find out if journal is peer reviewed by name
def peerReviewLinkCheckName(journalName):
    journalNameWords = journalName.split(" ")
    journalSearchAddressName = journalNameWords[0]
    for word in journalNameWords:
        if journalNameWords.index(word) == 0:
            word = ""
        else:
            word = "%20" + word
        journalSearchAddressName = journalSearchAddressName + word
    journalSearchAddressName = "http://uh4jc3de5m.search.serialssolutions.com/ejp/api/1/libraries/UH4JC3DE5M/search/types/alternate_title_equals/"+journalSearchAddressName+"?titleType=JOURNALS&beginPage=0&language=en-US&filterBy=All"
    return journalSearchAddressName

#function to get link to scrape from for issn of a journal
def peerReviewLinkCheckIssn(issns):
    issns = issns.split(",")
    issnLinks = []   
    for issn in issns:
        #making issn whitespace for link
        issn = issn.replace(" ", "")
        journalSearchAddressIssn = "http://uh4jc3de5m.search.serialssolutions.com/ejp/api/1/libraries/UH4JC3DE5M/search/types/issn_equals/"+issn+"?titleType=JOURNALS&beginPage=0&language=en-US&filterBy=All"

        issnLinks.append(journalSearchAddressIssn)
    return issnLinks

journalName = "journal of vision"
journalSearchAddressName = peerReviewLinkCheckName(journalName)
issns = "09717218A , 01622439"
issnList = peerReviewLinkCheckIssn(issns)

import json
def checkJournalPeerReview(url, checkType):
    with requests.Session() as s:
        getJson = s.get(url, proxies=myProxies, verify=False)
        jsonPage = getJson.text
        # print(jsonPage)
        dataDict = json.loads(jsonPage)
        print(dataDict)
        #try excepts for if there are no search results for the journal therefore 
        #the info for whether its peer reviewed or not won't be available
        #if/elif is for 
        if checkType == "issn":
            try:
                peerReviewCheck = dataDict.get('titles')
                peerReviewed = peerReviewCheck[0].get('peerReviewed')
            except IndexError:
                peerReviewed = "Unknown"
                print("unknown if peer reviewed")
        return peerReviewed    
    
        
# checkJournalPeerReview(issnList[1], "issn")
checkJournalPeerReview(journalSearchAddressName, "name")

# searchJournalPage = BeautifulSoup(html.content, "html.parser")
#         print(searchJournalPage.title.text)
#         if searchJournalPage.title.text == "Access Denied":
#             scrapingStatus = "Blocked"
#             return scrapingStatus
#         peerReviewBox = searchJournalPage.find(id="results-peer-reviewed_0")
#         print(peerReviewBox)
#         result = peerReviewBox.find_next("span", class_="ng-binding")
#         print(result.text)