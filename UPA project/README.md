# UPA Project - COVID 19

# Datasets

	cumulative.csv - dataset
	--------------------------------------------------------------------------------------------------
	cumulative,status=infected count=<count> <timestamp>
	cumulative,status=recovered count=<count> <timestamp>
	cumulative,status=deceased count=<count> <timestamp>

	regional.csv - dataset
	--------------------------------------------------------------------------------------------------
	regional,nuts=<nuts> infected=<count>,recovered=<count>,deceased=<count> <timestamp>

	total_deaths.csv - dataset
	--------------------------------------------------------------------------------------------------
	total_deaths count=<count> <timestamp>

# Files

	glp.py - download and save all actual datasets (total_deaths.csv is fixed to 01/12/20 as the original file has a variable name),
						and generate covid_19_db.txt file that contains InfluxDB commands for creating the 'covid_19_db' database
						and the data in the line protocol

	query.py - connect to influxDB running at localhost:8086 and get data by sending query to the database,
							then plot graphs from the data and save them as svg files to the 'graphs' directory

# Usage

	Prerequisities: InfluxDB

		1. Run glp.py
		
		2. Import data to InfluxDB

			influx -import -path=covid_19_db.txt -precision=s -database=covid_19_db
			
		3. Run query.py

# Note

	To run the InfluxDB shell (not necessary):

		influx -precision rfc3339 -database=covid_19_db
