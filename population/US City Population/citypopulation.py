import urllib2
import csv
import os



def writeToCsv(data, outFile, mode):
	with open(outFile, mode) as csvFile:
		writer = csv.writer(csvFile, delimiter='\t')
		writer.writerows(data)
	csvFile.close()

def isState(cityName, state):
	return (city == state)

def isCounty(cityName):
	return cityName.endswith('County')

def isTown(cityName):
	return cityName.endswith('town')

def isCity(cityName):
	return cityName.endswith('city')

def isTownship(cityName):
	return cityName.endswith('township')

def isBorough(cityName):
	return cityName.endswith('borough')

def isVillage(cityName):
	return cityName.endswith('village')



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

	cityHeaders = ['City', 'State', 'Year', 'Est. Population']
	stateHeaders = ['State', 'Year', 'Est. Population']
	countyHeaders = ['State', 'County', 'Year', 'Est. Population']

	outCityData.append(cityHeaders)
	outStateData.append(stateHeaders)
	outCountyData.append(countyHeaders)
	outTownshipData.append(cityHeaders)
	outTownData.append(cityHeaders)
	outBoroughData.append(cityHeaders)
	outVillageData.append(cityHeaders)
	outOtherData.append(cityHeaders)

	for row in rows:
		city = row[8]
		state = row[9]
		popEst2010 = row[11]
		popEst2011 = row[12]
		popEst2012 = row[13]
		popEst2013 = row[14]
		popEst2014 = row[15]
		popEst2015 = row[16]
		data = [city,  		state, 	    popEst2010, popEst2011,
		 	    popEst2012, popEst2013, popEst2014, popEst2015,]
		for i in range(2, 8):
			year = (2008+i)

			if(data[i] != '0'):
				if(isCity(data[0])):
					outCityData.append([data[0], data[1], year, data[i]])
				elif(isCounty(data[0])):
					outCountyData.append([data[1], data[0], year, data[i]])
				elif(isState(data[0], data[1])):
					outStateData.append([data[1], year, data[i]])
				elif(isTownship(data[0])):
					outTownshipData.append([data[0], data[1], year, data[i]])
				elif(isTown(data[0])):
					outTownData.append([data[0], data[1], year, data[i]])
				elif(isBorough(data[0])):
					outBoroughData.append([data[0], data[1], year, data[i]])
				elif(isVillage(data[0])):
					outVillageData.append([data[0], data[1], year, data[i]])
				elif(data[0] != 'NAME'):
					outOtherData.append([data[0], data[1], year, data[i]])


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



