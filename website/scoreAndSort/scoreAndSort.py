from website.search.search import getCurrentYear

#function which applies filter deductions
def filterCheck(obj, filters, score, filter, condition, concernedVariable, n , limiter=None):
	if condition == False: 
			if filters.get(filter) and getattr(obj, concernedVariable) == False:
				score = score - n
				print("filterCheck", -n)	
	elif condition == 'False': 
			if filters.get(filter) and getattr(obj, concernedVariable) == 'False':
				score = score - n
				print("filterCheck", -n)	
	elif condition == '>':
			if filters[filter] != "" and int(filters.get(filter)) > getattr(obj, concernedVariable):
				if limiter:
					score = score - n*(1/limiter)
					print("filterCheck", -n*(1/limiter))
				else:
					score = score - n	
					print("filterCheck", -n)
	elif condition == '<':
			if filters[filter] != "" and int(filters.get(filter)) < getattr(obj, concernedVariable):
				score = score - n
				print("filterCheck", -n)
				
	return score

#function which applies boolean value scoring 		
def booleanScoring(study, score, concernedVariable, condition, addage):
		if getattr(study, concernedVariable) == condition:
			score = score + addage
			print("booleanCheck", addage)
		#some values will have a None value, it's important no scoring is done then
		elif getattr(study, concernedVariable) != "Unknown" and getattr(study, concernedVariable) != None:
			score = score - addage
			print("booleanCheck", -addage)
		return score

#main function for this module
def scoreAndSort(searchedStudies, filters, numResults):
	print("SCORING TIME CHECK THE SHELL")
	currentYear = getCurrentYear()
	#block of code which assigns scores based on filters given and if they weren’t
	#the system for these attributes in terms of how much score they merit is
        #handled
    
	for study in searchedStudies:
		score = 0
		#variables that will be used in calculations
		studyAge = currentYear - study.pubYear

		#if statements that take away score for not meeting filters
		score = filterCheck(study, filters, score, 'peerReviewed', 'False', 'peerReviewed', 50)
		score = filterCheck(study, filters, score, 'governmentAffiliation', False, 'governmentAffiliation', 50)
		score = filterCheck(study, filters, score, 'minCitations', '>', 'numCitations', 50)
		score = filterCheck(study, filters, score, 'minPubYear', '>', 'pubYear', 50)
		score = filterCheck(study, filters, score, 'maxDaysSinceCite', '<', 'daysSinceCite', 50)
	
		#considering press freedom of the corresponding country will be calculation based on if govAff is true

		score = booleanScoring(study.journalInfo, score, 'peerReviewed', "True", 20)
		
		#or 0 checks is simple validation that ensures if retireval of a numerical value in scraping
		#was unsuccessful then 0 is used instead for the calculation, preventing an error occuring
		score = score + 0.1*(study.journalInfo.sjrScore or 0)
		print(searchedStudies.index(study), 0.1*(study.journalInfo.sjrScore or 0))
		score = score + 0.1*(study.journalInfo.journalHIndex or 0)
		print(searchedStudies.index(study), 0.1*(study.journalInfo.journalHIndex or 0))
		score = score + 0.02*(study.numCitations or 0)
		print(searchedStudies.index(study), 0.02*(study.numCitations or 0))
		score = score + 0.08*(study.citationsOfTopCiters or 0)
		print(searchedStudies.index(study), 0.08*(study.citationsOfTopCiters or 0))
		# score = score + 0.01*(study.reviewRefCount or 0)
		# score = score + 0.00001*(study.viewCount or 0)
		#can't find out number of versions, wasn't very meaningful anyway

		
		#adding scoring due to the author, limiter means that roughly the same possible score is possible
		#for every study so having a proportion of good authors is more important 
		print("AUTHOR SCORING SHOULD START NOW")
		limiter = len(study.authorOrgInfo)
		for author in study.authorOrgInfo:
			print("IF IT HAD AN AUTHOR ID WE SHOULD BE HERE")
			score = filterCheck(author, filters, score, 'minAuthCitations', '>', 'authorCitations', 5, limiter)
			score = filterCheck(author, filters, score, 'minCareerLength', '>', 'careerLength',5, limiter)
			score = score + 1.25*(author.hIndex or 0)*(1/limiter)
			print(searchedStudies.index(study), 1.25*(author.hIndex or 0)*(1/limiter))
			score = score + 4*(author.i10index or 0)*(1/limiter)
			print(searchedStudies.index(study), 4*(author.i10index or 0)*(1/limiter))
			score = score + (author.hIndex5y or 0)*(1/limiter)
			print(searchedStudies.index(study), (author.hIndex5y or 0)*(1/limiter))
			score = score + 3.2*(author.i10index5y or 0)*(1/limiter)
			print(searchedStudies.index(study), 3.2*(author.i10index5y or 0)*(1/limiter))
			score = score + 0.1*(author.authorCitations or 0)*(1/limiter)
			print(searchedStudies.index(study), 0.1*(author.authorCitations or 0)*(1/limiter))
			score = score + 0.08*(author.authorCitations5y or 0)*(1/limiter)
			print(searchedStudies.index(study), 0.08*(author.authorCitations5y or 0)*(1/limiter))
			score = score + 0.01*(author.careerLength or 0)*(1/limiter)
			print(searchedStudies.index(study), 0.01*(author.careerLength or 0)*(1/limiter))
			score = score + 0.1*(author.authorCitationsThisYear or 0)*(1/limiter)
			print(searchedStudies.index(study), 0.1*(author.authorCitationsThisYear or 0)*(1/limiter))
			score = score + 0.01*(author.authorYearsSinceCite or 0)*(1/limiter)
			print(searchedStudies.index(study), 0.01*(author.authorYearsSinceCite or 0)*(1/limiter))
			# score = score + 0.0005*(author.university.uniCitations or 0)*(author.university.uniResearch or 0)*(1/limiter)
			
		#rewards old, heavily cited studies
		if study.daysSinceCite and study.daysSinceCite < 1:
			study.daysSinceCite = 1
		score = score + 5*(studyAge or 0)*(study.numCitations or 0)*(1/(study.daysSinceCite or 1**10))/365
		print(searchedStudies.index(study), 5*(studyAge or 0)*(study.numCitations or 0)*(1/(study.daysSinceCite or 1**10))/365)
		score = score + (3000*(1/(study.daysSinceCite or 1**10)) - 0.05)/365
		print(searchedStudies.index(study), (3000*(1/(study.daysSinceCite or 1**10)) - 0.05)/365)
		
		if (studyAge) == 0:
			score = score + 15
			print(searchedStudies.index(study), 15)
		else:
			score = score + (1/(studyAge or 0))
			print(searchedStudies.index(study), (1/(studyAge or 0)))
		 		
		# if study.governmentAffiliation:
		# 		score = score + 0.05(study.government.pressFreedom - 70)
		# elif study.levelOfGovernmentAffiliation:
		# 		score = score + 0.0014(study.government.pressFreedom - 50)(study.levelOfGovernmentAffiliation)
		 
		#setting each searchResonse object's final score so it can be sorted
		study.score = score

	#sorting by score and chopping to required amount of studies for the result goes here
	searchedStudies.sort(key = lambda study : study.score, reverse=True)
	if numResults:
		numResults = int(numResults)
	else:
		numResults = 5
	searchedStudies = searchedStudies[0:numResults]
	return searchedStudies

	#note: I'm sure with the API and my own scrapings in the iterations where I test this
	#I will get None values for some of the variables from time to time, I will identify
	#each one and program a subsequent check for it, above I already do this for every
	#boolean score