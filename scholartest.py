from scholarly import scholarly, ProxyGenerator
from datetime import datetime

 
pg = ProxyGenerator()
success = pg.ScraperAPI('d07eb644f66c41a5ebf97168156dc1d5')
# success = pg.FreeProxies()
scholarly.use_proxy(pg)
if success:
    print("success")
    #print(datetime.now())
    #authorName_query = scholarly.search_author('Z Meng')
    searchQuery = scholarly.search_pubs("vegan diet")
    # #author = next(authorName_query) 
    study = next(searchQuery)
    # #scholarly.pprint(scholarly.fill(author, sections=['publications']))
    scholarly.pprint(scholarly.fill(study, sections='basics'))

    # search_query = scholarly.search_author('Steven A Cholewiak')
    # author = next(search_query)
    # scholarly.pprint(scholarly.fill(author, sections=['basics', 'indices', 'coauthors']))
    # for i in range (0, 2):
    #     study = next(studies)
    #     print(study)
    #     print(datetime.now())
