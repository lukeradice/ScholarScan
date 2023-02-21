import datetime

#function which applies filter deductions
def filterCheck(study, filters, score, filter, condition, concernedVariable, limiter=None, n):
	if condition == 'False': 
			if filters.get(filter) and getattr(study, concernedVariable) == False:
				score = score - n	
	elif condition == '>':
			if filters.contains(filter) and filters.get(filter) > getattr(study, concernedVariable):
				if limiter:
					score = score - 5*(1/limiter)
				else:
					score = score - n	
	elif condition == '<':
			if filters.contains(filter) and filters.get(filter) < getattr(study, concernedVariable):
				score = score - n
				
	return score

#function which applies boolean value scoring 		
def booleanScoring(study, score, concernedVariable, condition, addage):
		if getattr(study, concernedVariable) == condition:
			score = score + addage
		#some values will have a None value, it's important no scoring is done then
		elif getattr(study, concernedVariable) != None:
			score = score - addage
		return score

#main function for this module
def scoreAndSort(searchedStudies, filters, numResults):
	score = 0
	currentYear = datetime.date.today().strftime("%Y")
	#block of code which assigns scores based on filters given and if they weren’t
	#the system for these attributes in terms of how much score they merit is
        #handled
    
	for study in searchedStudies:
		#variables that will be used in calculations
		studyAge = currentYear - study.pubYear

		#if statements that take away score for not meeting filters
		score = filterCheck(study, filters, score, 'peerReviewed', 'False', 'peerReviewed', 5)
		score = filterCheck(study, filters, score, 'minCitations', '>', 'numCitations', 5)
		score = filterCheck(study, filters, score, 'noConflictInterest', 'False', 'noConflictInterest', 5)
		score = filterCheck(study, filters, score, 'notExternallyFunded', 'False', 'notExternallyFunded', 5)				
		score = filterCheck(study, filters, score, 'conflictDisclosed', 'False', 'conflictDisclosed', 5)
		score = filterCheck(study, filters, score, 'fundingDisclosed', 'False', 'fundingDisclosed', 5) 
		score = filterCheck(study, filters, score, 'governmentAffiliation', 'False', 'governmentAffiliation', 5)		
		score = filterCheck(study, filters, score, 'minPubYear', '>', 'pubYear', 5)
		score = filterCheck(study, filters, score, 'maxYearsSinceCite', '<', 'yearsSinceCite', 5)
	
		#considering press freedom of the corresponding country
		# if study.government.pressFreedom >= 85:
		# 	score = 

		score = booleanScoring(study, score, 'peerReviewed', True, 10)
		score = booleanScoring(study, score, 'conflictDisclosed', True, 5)
		score = booleanScoring(study, score, 'conflictInterest', False, 5)
		score = booleanScoring(study, score, 'fundingDisclosed', False, 3)
		score = booleanScoring(study, score, 'externallyFunded', True, 4)
		
		#or 0 checks is simple validation that ensures if retireval of a numerical value in scraping
		#was unsuccessful then 0 is used instead for the calculation, preventing an error occuring
		score = score + (study.sjrValue or 0)
		score = score + 0.02*(study.numCitations or 0)
		score = score + 0.08*(study.citationsOfTopCiters or 0)
		score = score + 0.01*(study.reviewRefCount or 0)
		score = score + 0.00001*(study.viewCount or 0)
		#can't find out number of versions, wasn't very meaningful anyway

		
		#adding scoring due to the author, limiter means that roughly the same possible score is possible
		#for every study so having a proportion of good authors is more important 
		limiter = len(study.authorOrgInfo)
		for author in study.authorOrgInfo:
			score = filterCheck(author, filters, score, 'authMinCitations', '>', 'authCitations', limiter, 1)
			score = score + 0.125*(author.hIndex or 0)*(1/limiter)
			score = score + 0.4*(author.i10Index or 0)*(1/limiter)
			score = score + 0.1*(author.hIndex5y or 0)*(1/limiter)
			score = score + 0.32*(author.i10Index5y or 0)*(1/limiter)
			score = score + 0.01*(author.authorCitations or 0)*(1/limiter)
			score = score + 0.008*(author.authorCitations5y or 0)*(1/limiter)
			score = score + 0.001*(author.authorStudiesDone or 0)*(1/limiter)
			score = score + 0.0005*(author.university.uniCitations or 0)*(author.university.uniResearch or 0)*(1/limiter)
			
		#rewards old, heavily cited studies
		if study.yearsSinceCite and study.yearsSinceCite < 1:
			study.yearsSinceCite = 1
		score = score + 0.01*(studyAge or 0)*(study.numCitations or 0)*(1/(study.yearsSinceCite or 1**10))
		score = score + 3*(1/(study.yearsSinceCite or 1** 10)) - 0.5
		
		if (studyAge) == 0:
			score = score + 1
		else:
			score = score + (1/(studyAge or 0))
		 		
		if study.governmentAffiliation:
				score = score + 0.05(study.government.pressFreedom - 70)
		elif study.levelOfGovernmentAffiliation:
				score = score + 0.0014(study.government.pressFreedom - 50)(study.levelOfGovernmentAffiliation)
		 
		#setting each searchResonse object's final score so it can be sorted
		study.score = score

	#sorting by score and chopping to required amount of studies for the result goes here
	searchedStudies.sort(key = lambda study : study.score, reverse=True)
	searchedStudies = searchedStudies[0:numResults]
	return searchedStudies

	#note: I'm sure with the API and my own scrapings in the iterations where I test this
	#I will get None values for some of the variables from time to time, I will identify
	#each one and program a subsequent check for it, above I already do this for every
	#boolean score