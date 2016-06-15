import urllib2
import csv
import os
import sets




def determineIndicator(name):
	indicators = ['city', 'town', 'township',
				  'municipality', 'county','balance',
				  'city (pt.)', 'city (balance)',
				  'borough', 'parish', 'village', 'village (pt.)',
				  'Municipality', 'town (pt.)', 'Borough',
				  'Census Area', 'County', '(balance)'
				  ]

	for indicator in indicators:
		if(name.endswith(indicator)):
			return indicator

	return ''


def isState(name, state):
	return state == name

def isCounty(name):
	return name.endswith('County')


def writeToCsv(data, outFile, mode):
	with open(outFile, mode) as csvFile:
		writer = csv.writer(csvFile, delimiter='\t')
		writer.writerows(data)
	csvFile.close()


def removeDuplicates(arr):
	seen = set()
	cleanedList = []
	for item in arr:
		t = tuple(item)
		if t not in seen:
			cleanedList.append(item)
			seen.add(t)
	return cleanedList

def checkPopulationSize(row):
	population = 0
	try:
		population = int(str(row[len(row)-1]))
	except:
		pass
	
	if(population < 5000):
		return 'small'
	elif(population >= 5000 and population < 50000):
		return 'medsmall'
	elif(population >= 50000 and population < 350000):
		return 'med'
	elif(population >= 350000 and population < 500000):
		return 'medlarge'
	elif(population >= 500000):
		return 'large'




if __name__ == "__main__":
	url = 'http://www.census.gov/popest/data/cities/totals/2015/files/SUB-EST2015_ALL.csv'
	response = urllib2.urlopen(url)
	entries = csv.DictReader(response)


	rows = []
	year = 2010
	print('Reading data.')
	for entry in entries:
		name = entry['NAME']
		state = entry['STNAME']
		indicator = determineIndicator(name)
		pop2010 = entry['POPESTIMATE2010']
		pop2011 = entry['POPESTIMATE2011']
		pop2012 = entry['POPESTIMATE2012']
		pop2013 = entry['POPESTIMATE2013']
		pop2014 = entry['POPESTIMATE2014']
		pop2015 = entry['POPESTIMATE2015']

		# if county
		if(isCounty(name)):
			rows.append([name, state, str(year), pop2010])
			rows.append([name, state, str(year+1), pop2011])
			rows.append([name, state, str(year+2), pop2012])
			rows.append([name, state, str(year+3), pop2013])
			rows.append([name, state, str(year+4), pop2014])
			rows.append([name, state, str(year+5), pop2015])
		# if state
		elif(isState(name, state)):
			rows.append([name, str(year), pop2010])
			rows.append([name, str(year+1), pop2011])
			rows.append([name, str(year+2), pop2012])
			rows.append([name, str(year+3), pop2013])
			rows.append([name, str(year+4), pop2014])
			rows.append([name, str(year+5), pop2015])
		# else city
		else:
			name = name.replace(determineIndicator(name), '')
			rows.append([name, state, indicator, str(year), pop2010])
			rows.append([name, state, indicator, str(year+1), pop2011])
			rows.append([name, state, indicator, str(year+2), pop2012])
			rows.append([name, state, indicator, str(year+3), pop2013])
			rows.append([name, state, indicator, str(year+4), pop2014])
			rows.append([name, state, indicator, str(year+5), pop2015])
		



	cityHeaders = ['City', 'State', 'Incorporation', 'Year', 'Population']
	stateHeaders = ['State', 'Year', 'Population']
	countyHeaders = ['County', 'State', 'Year', 'Population']

	states = []
	counties = []
	smallCities = []
	medSmallCities = []
	medCities = []
	medLargeCities = []
	largeCities = []

	states.append(stateHeaders)
	counties.append(countyHeaders)
	smallCities.append(cityHeaders)
	medSmallCities.append(cityHeaders)
	medCities.append(cityHeaders)
	medLargeCities.append(cityHeaders)
	largeCities.append(cityHeaders)

	print('Sorting data.')
	for row in rows:
		
		if(len(row) == 3):
			states.append(row)
		elif(len(row) == 4):
			counties.append(row)
		elif(len(row) == 5):
			if(checkPopulationSize(row) == 'small'):
				smallCities.append(row)
			elif(checkPopulationSize(row) == 'medsmall'):
				medSmallCities.append(row)
			elif(checkPopulationSize(row) == 'med'):
				medCities.append(row)
			elif(checkPopulationSize(row) == 'medlarge'):
				medLargeCities.append(row)
			elif(checkPopulationSize(row) == 'large'):
				largeCities.append(row)

	ROOTDIR = os.path.dirname(os.path.realpath(__file__)) + '/data/'
	
	writeToCsv(removeDuplicates(smallCities), ROOTDIR+'smallcitypop.csv', 'w')
	writeToCsv(removeDuplicates(medSmallCities), ROOTDIR+'medsmallcitypop.csv', 'w')
	writeToCsv(removeDuplicates(medCities), ROOTDIR+'medcitypop.csv', 'w')
	writeToCsv(removeDuplicates(medLargeCities), ROOTDIR+'medlargecitypop.csv', 'w')
	writeToCsv(removeDuplicates(largeCities), ROOTDIR+'largecitypop.csv', 'w')
	writeToCsv(removeDuplicates(states), ROOTDIR+'statepop.csv', 'w')
	writeToCsv(removeDuplicates(counties), ROOTDIR+'countiespop.csv', 'w')
	print('Data saved.')
		
