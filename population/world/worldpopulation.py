import json
import urllib2
import sys
import csv
import os



def getData(data, dataDir):
	tsvRow = []
	jsonFile = json.loads(data)
	rows = jsonFile[1]
	headers = ['Country', 'Year', 'Population']
	populationValues = []

	# append headers if file does not exist
	if(not os.path.exists(dataDir + 'worldtotalpopulation.tsv')):
		tsvRow.append(headers)

	try:
		for row in rows:
			country = rows[0]['country']['value'].encode('utf-8')
			year = row['date'].encode('utf-8')
			population = row['value'].encode('utf-8')
			populationValues = [country, year, population]
			tsvRow.append(populationValues)
	except:
		print('No data found.')
		
	return tsvRow


def writeToCsv(data, outFile, mode):
	with open(outFile, mode) as csvFile:
		writer = csv.writer(csvFile, delimiter='\t')
		writer.writerows(data)
	csvFile.close()


def getCountryCodes(codeDir):
	codes = []
	with open(codeDir, 'rb') as f:
		reader = csv.reader(f, delimiter=' ')
		for row in reader:
			codes.append(row[0])
	return codes



if __name__ == "__main__":
	ROOTDIR = os.path.dirname(os.path.realpath(__file__))
	DATADIR = ROOTDIR + '/data/'

	if(len(sys.argv) < 2):
		countryCodes = getCountryCodes(ROOTDIR + '/read_only/countrycodes.csv')
	else:
		countryCodes = [str(sys.argv[1])]


	for code in countryCodes:
		url = 'http://api.worldbank.org/countries/' + code.upper() +\
		 '/indicators/SP.POP.TOTL?per_page=100&date=1960:2014&format=json'

		webURL = urllib2.urlopen(url)
		if(webURL.getcode() == 200):
			data = webURL.read()
			writeToCsv(getData(str(data), DATADIR), DATADIR + 'worldtotalpopulation.tsv', 'a')
		else:
			print('Server error. Cannot retrieve results.')

