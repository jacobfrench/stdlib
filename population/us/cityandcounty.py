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
				  'Census Area', 'County', '(balance)', 'Parish',
				  '(balance) (pt.)'
				  ]

	for indicator in indicators:
		if(name.endswith(indicator)):
			return indicator

	return ''


def isState(name, state):
	return (state == name)


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

	# city sizes
	SMALL = 'small'
	MEDSMALL = 'medsmall'
	MED = 'med'
	MEDLARGE = 'medlarge'
	LARGE = 'large'

	print('Reading data.')
	url = 'http://www.census.gov/popest/data/cities/totals/2015/files/SUB-EST2015_ALL.csv'
	response = urllib2.urlopen(url)
	entries = csv.DictReader(response)


	rows = []
	
	print('Sorting data.')
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
			rows.append([name, state, '2010', pop2010])
			rows.append([name, state, '2011', pop2011])
			rows.append([name, state, '2012', pop2012])
			rows.append([name, state, '2013', pop2013])
			rows.append([name, state, '2014', pop2014])
			rows.append([name, state, '2015', pop2015])
		# if state
		elif(isState(name, state)):
			rows.append([name, '2010', pop2010])
			rows.append([name, '2011', pop2011])
			rows.append([name, '2012', pop2012])
			rows.append([name, '2013', pop2013])
			rows.append([name, '2014', pop2014])
			rows.append([name, '2015', pop2015])
		# else city
		else:
			name = name.replace(determineIndicator(name), '')
			rows.append([name, state, indicator, '2010', pop2010])
			rows.append([name, state, indicator, '2011', pop2011])
			rows.append([name, state, indicator, '2012', pop2012])
			rows.append([name, state, indicator, '2013', pop2013])
			rows.append([name, state, indicator, '2014', pop2014])
			rows.append([name, state, indicator, '2015', pop2015])



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

	for row in rows:
		
		if(len(row) == 3):
			states.append(row)
		elif(len(row) == 4):
			counties.append(row)
		elif(len(row) == 5):
			if(checkPopulationSize(row) == SMALL):
				smallCities.append(row)
			elif(checkPopulationSize(row) == MEDSMALL):
				medSmallCities.append(row)
			elif(checkPopulationSize(row) == MED):
				medCities.append(row)
			elif(checkPopulationSize(row) == MEDLARGE):
				medLargeCities.append(row)
			elif(checkPopulationSize(row) == LARGE):
				largeCities.append(row)

	ROOTDIR = os.path.dirname(os.path.realpath(__file__)) + '/data/'
	
	writeToCsv(removeDuplicates(smallCities), ROOTDIR+'smallcitypop.tsv', 'w')
	writeToCsv(removeDuplicates(medSmallCities), ROOTDIR+'medsmallcitypop.tsv', 'w')
	writeToCsv(removeDuplicates(medCities), ROOTDIR+'medcitypop.tsv', 'w')
	writeToCsv(removeDuplicates(medLargeCities), ROOTDIR+'medlargecitypop.tsv', 'w')
	writeToCsv(removeDuplicates(largeCities), ROOTDIR+'largecitypop.tsv', 'w')
	writeToCsv(removeDuplicates(states), ROOTDIR+'statepop.tsv', 'w')
	writeToCsv(removeDuplicates(counties), ROOTDIR+'countiespop.tsv', 'w')
	print('Data saved.')
		
