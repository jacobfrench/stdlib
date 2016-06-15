import urllib2
import csv
import os
import sets

def writeToCsv(data, outFile, mode):
	with open(outFile, mode) as csvFile:
		writer = csv.writer(csvFile, delimiter='\t')
		writer.writerows(data)
	csvFile.close()

def isState(cityName, state):
	return (city == state)

def isCounty(cityName):
	return cityName.endswith('County') or cityName.endswith('county')

def isTown(cityName):
	return cityName.endswith('town')

def isCity(cityName):
	return cityName.endswith('city')

def isTownship(cityName):
	return cityName.endswith('township')

def isBorough(cityName):
	return cityName.endswith('borough') or cityName.endswith('Borough')\
	and not cityName.endswith('city and borough')

def isVillage(cityName):
	return cityName.endswith('village')

def isParish(cityName):
	return cityName.endswith('Parish')

def isMunicipality(cityName):
	return cityName.lower().endswith('municipality')

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

def removeDuplicates(arr):
	seen = set()
	cleanedList = []
	for item in arr:
		t = tuple(item)
		if t not in seen:
			cleanedList.append(item)
			seen.add(t)
	return cleanedList



if __name__ == "__main__":
	ROOTDIR = os.path.dirname(os.path.realpath(__file__))
	DATADIR = ROOTDIR + '/data/'
	url = 'http://www.census.gov/popest/data/cities/totals/2015/files/SUB-EST2015_ALL.csv'
	response = urllib2.urlopen(url)
	rows = csv.reader(response)


	data = []

	outCityData = []
	outStateData = []
	outCountyData = []
	outTownshipData = []
	outTownData = []
	outBoroughData = []
	outVillageData = []
	outOtherData = []

	cityHeaders = ['City', 'Incorporation', 'State', 'Year', 'Population']
	stateHeaders = ['State', 'Year', 'Est. Population']
	countyHeaders = ['State', 'County', 'Year', 'Population']

	outStateData.append(stateHeaders)
	outCountyData.append(countyHeaders)
	outOtherData.append(cityHeaders)


	for row in rows:
		city = row[8]
		state = row[9]
		pop2010 = row[12]
		pop2011 = row[13]
		pop2012 = row[14]
		pop2013 = row[15]
		pop2014 = row[16]
		pop2015 = row[17]
		data = [city,  		state, 	    pop2010, 	pop2011,
		 	    pop2012, 	pop2013, 	pop2014, 	pop2015]
		for i in range(2, 8):
			year = (2008+i)

			if(data[i] != '0' and not data[0].endswith('government')):			
				# strip junk text
				cityName = str(data[0])
				cityName = cityName.replace('Balance of ', '')
				cityName = cityName.replace('metro government', '')
				cityName = cityName.replace('metropolitan government', '')
				cityName = cityName.replace('city and', '')
				cityName = cityName.replace('City and', '')
				cityName = cityName.replace('city (balance) (pt.)', '')


				

				if(isCity(cityName)):
					outCityData.append([cityName.strip('city'), 'city', data[1], year, data[i]])
				elif(isCounty(cityName)):
					outCountyData.append([data[1], cityName, year, data[i]])
				elif(isState(cityName, data[1])):
					outStateData.append([data[1], year, data[i]])
				elif(isTownship(cityName)):
					outTownshipData.append([cityName.strip('township'), 'township', data[1], year, data[i]])
				elif(isTown(cityName)):
					outTownData.append([cityName.strip('town'), 'town', data[1], year, data[i]])
				elif(isBorough(cityName)):
					cityName = cityName.replace('Borough', '')
					outBoroughData.append([cityName.strip('borough'), 'borough', data[1], year, data[i]])
				elif(isVillage(cityName)):
					outVillageData.append([cityName.strip('village'), 'village', data[1], year, data[i]])
				elif(cityName.endswith('city and borough')):
					outBoroughData.append([cityName.replace('city and borough', ''), 'city and borough', data[1], year, data[i]])
				elif(isParish(cityName)):
					outBoroughData.append([cityName.replace('Parish', ''), 'parish', data[1], year, data[i]])
				elif(isMunicipality(cityName)):
					cityName = cityName.replace('municipality', '')
					outBoroughData.append([cityName.replace('Municipality', ''), 'municipality', data[1], year, data[i]])


				elif(cityName != 'NAME'):
					if(cityName.endswith(' city (pt.)')):
						outOtherData.append([cityName.strip(' city (pt.)'), 'city (pt.)', data[1], year, data[i]])
					elif(cityName.endswith(' town (pt.)')):
						outOtherData.append([cityName.strip(' town (pt.)'), 'town (pt.)', data[1], year, data[i]])
					elif(cityName.endswith('city (balance)')):
						outOtherData.append([cityName.strip('city (balance)'), 'city (balance)', data[1], year, data[i]])
					elif(cityName.endswith('(balance)')):
						outOtherData.append([cityName.strip(' (balance)'), 'balance', data[1], year, data[i]])
					elif(cityName.endswith(' village (pt.)')):
						outOtherData.append([cityName.strip(' village (pt.)'), 'village (pt.)', data[1], year, data[i]])
					else:
						cityName.strip('Balance of')
						cityName.strip('city (balance) (pt.)')
						cityName.strip('metro government')
						cityName.strip('metropolitan government')
						outOtherData.append([cityName, '<----', data[1], year, data[i]])



	print(str(len(outCityData)/6) + ' cities found.')
	print(str(len(outCountyData)/6) + ' counties found.')
	print(str(len(outStateData)/6) + ' states found.')
	print(str(len(outTownshipData)/6) + ' townships found.')
	print(str(len(outTownData)/6) + ' towns found.')
	print(str(len(outBoroughData)/6) + ' boroughs found.')
	print(str(len(outVillageData)/6) + ' villages found.')
	print(str(len(outOtherData)/6) + ' others found.')

				


	writeToCsv(outCityData, DATADIR+'uscitypop.tsv', 'w')
	writeToCsv(outStateData, DATADIR+'usstatepop.tsv', 'w')
	writeToCsv(outCountyData, DATADIR+'uscountypop.tsv', 'w')
	writeToCsv(outTownshipData, DATADIR+'ustownshippop.tsv', 'w')
	writeToCsv(outTownData, DATADIR+'ustownpop.tsv', 'w')
	writeToCsv(outBoroughData, DATADIR+'usboroughpop.tsv', 'w')
	writeToCsv(outVillageData, DATADIR+'usvillagepop.tsv', 'w')
	writeToCsv(outOtherData, DATADIR+'usotherpop.tsv', 'w')



	fileNames = ['usboroughpop.tsv',
				 'uscitypop.tsv',
				 'usotherpop.tsv',
				 'ustownpop.tsv',
				 'ustownshippop.tsv',
				 'usvillagepop.tsv'
				]

	
	smallCities = []
	medSmallCities = []
	medCities = []
	medlargeCities = []
	largeCities = []

	smallCities.append(cityHeaders)
	medSmallCities.append(cityHeaders)
	medCities.append(cityHeaders)
	medlargeCities.append(cityHeaders)
	largeCities.append(cityHeaders)

	# sort by population size
	for name in fileNames:
		print name
		with open(DATADIR+name, 'rb') as file:
			reader = csv.reader(file, delimiter='\t')

			for row in reader:
				size = checkPopulationSize(row)
				if(size == 'small'):
					smallCities.append(row)
				elif(size == 'medsmall'):
					medSmallCities.append(row)
				elif(size == 'med'):
					medCities.append(row)
				elif(size == 'medlarge'):
					medlargeCities.append(row)
				elif(size == 'large'):
					largeCities.append(row)



	writeToCsv(removeDuplicates(smallCities), DATADIR+'smallcitypop.tsv', 'w')
	writeToCsv(removeDuplicates(medSmallCities), DATADIR+'medsmallcitypop.tsv', 'w')
	writeToCsv(removeDuplicates(medCities), DATADIR+'medcitypop.tsv', 'w')
	writeToCsv(removeDuplicates(medlargeCities), DATADIR+'medlargecitypop.tsv', 'w')
	writeToCsv(removeDuplicates(largeCities), DATADIR+'largecitypop.tsv', 'w')


	# delete unwanted files
	for name in fileNames:
		if('usotherpop.tsv' not in name):
			os.remove(DATADIR+name)




