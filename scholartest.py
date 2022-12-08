from actualScholarly import scholarly, ProxyGenerator
from datetime import datetime

searchQuery = "vegan diet"
pg = ProxyGenerator()
success = pg.ScraperAPI('f171d0c5dd2ec4eb81c87ab25875fdd9')
#success = pg.FreeProxies()
scholarly.use_proxy(pg)
if success:
    print("success")
    print(datetime.now())
    studies = scholarly.search_pubs(str(searchQuery))
    print(datetime.now())
    for i in range (0, 2):
        study = next(studies)
        print(study)
        print(datetime.now())
