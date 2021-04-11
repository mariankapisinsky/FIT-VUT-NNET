import os
import csv
from urllib.request import urlopen
from datetime import datetime, timezone

def download(url, file):
	
	if(os.path.exists(file)):
		os.remove(file)

	data = urlopen(url).read()
	
	with open(file, 'wb') as f:
		f.write(data)
		f.close()

def getDatasets():
	
	download('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv', 'cumulative.csv')
	
	download('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv', 'regional.csv')
	
	download('https://czso.cz/documents/62353418/138258873/130185-20data120120.csv', 'total_deaths.csv')

def makeTimestamp(date):
	date = datetime.fromisoformat(date)
	utc_date = date.replace(tzinfo=timezone.utc)
	return str(int(utc_date.timestamp()))

def generateCumulative(file):
	infected = []
	recovered = []
	deceased = []

	with open('cumulative.csv', newline='') as csvfile:
		dataset_reader = csv.reader(csvfile, delimiter=',')
		next(dataset_reader)
		for row in dataset_reader:
			timestamp = makeTimestamp(row[0])
			infected.append('cumulative,status=infected count=' + row[1] + ' ' + timestamp)
			recovered.append('cumulative,status=recovered count=' + row[2] + ' ' + timestamp)
			deceased.append('cumulative,status=deceased count=' + row[3] + ' ' + timestamp)

	for item in infected:
		file.write(item + '\n')
	for item in recovered:
		file.write(item + '\n')
	for item in deceased:
		file.write(item + '\n')
				
def generateRegional(file):
	nuts = ''
	infected = 0
	recovered = 0
	deceased = 0	
	
	with open('regional.csv', newline='') as csvfile:
		dataset_reader = csv.reader(csvfile, delimiter=',')
		next(dataset_reader)
		for row in dataset_reader:
			if (nuts == ''):
				nuts = row[1]
				timestamp = makeTimestamp(row[0])
			if (row[1] == nuts):
				infected += int(row[3])
				recovered += int(row[4])
				deceased += int(row[5])
			else:
				file.write('regional,nuts=' + nuts + ' infected=' + str(infected) + ',recovered=' + str(recovered) + ',deceased=' + str(deceased) + ' ' + timestamp + '\n')
				nuts = row[1]
				timestamp = makeTimestamp(row[0])
				infected = int(row[3])
				recovered = int(row[4])
				deceased = int(row[5])
	
	file.write('regional,nuts=' + nuts + ' infected=' + str(infected) + ',recovered=' + str(recovered) + ',deceased=' + str(deceased) + ' ' + timestamp + '\n')
				
def generateTotalDeaths(file):
	
	with open('total_deaths.csv', newline='') as csvfile:
		dataset_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		next(dataset_reader)
		for row in dataset_reader:
			if(int(row[7]) > 2015 and row[12] == 'celkem'):
				timestamp = makeTimestamp(row[11])
				file.write('total_deaths count=' + row[1] + ' ' + timestamp + '\n')

def main():
	
	if(os.path.exists('covid_19_db.txt')):
		os.remove('covid_19_db.txt')
	
	getDatasets()
	
	with open('covid_19_db.txt', 'w') as file:
		file.write('# DDL\n')
		file.write('CREATE DATABASE covid_19_db\n\n')
		file.write('# DML\n')
		file.write('# CONTEXT-DATABASE: covid_19_db\n\n')
		generateCumulative(file)
		generateRegional(file)
		generateTotalDeaths(file)

if __name__ == "__main__":
	main()
