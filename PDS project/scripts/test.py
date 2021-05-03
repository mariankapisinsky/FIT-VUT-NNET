#
# Testing Script
# PDS 2021 - Identification of Mobile Traffic using TLS Fingerprinting
# Bc. Marian Kapisinsky, xkapis00
# 25.4.2021
#
# Inspired by:
# https://github.com/matousp/ja3s-fingerprinting
#

import sys, getopt
import csv
import hashlib
import re

GREASE = ["2570","6682","10794","14906","19018","23130","27242","31354","35466","39578","43690","47802","51914","56026","60138","64250","65281"]

def usage():
	print('test.py --csv <csv> --db <db> {-1|-2|-3|-4}')

def main(argv):
	ifile=''
	dbfile=''
	
	exp1 = False
	exp2 = False
	exp3 = False
	exp4 = False
	
	try:
		opts, args = getopt.getopt(argv, "h1234", ["help", "csv=", "db="])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)
		
	if not opts and not args:
		usage()
		sys.exit(2)
		
	for opt, arg in opts:
		if opt == "-h" or opt == "--help":
			usage()
			sys.exit(0)
		elif opt == "--csv":
			ifile = arg;
		elif opt == "--db":
			dbfile = arg
		elif opt == "-1":
			exp1 = True
		elif opt == "-2":
			exp1 = True
			exp2 = True
		elif opt == "-3":
			exp1 = True
			exp2 = True
			exp3 = True
		elif opt == "-4":
			exp1 = True
			exp4 = True
	
	if not ifile or not dbfile:
		print("Missing either input file or database file")
		usage()
		sys.exit(2)
		
	if not exp1 and not exp2 and not exp3 and not exp4:
		print("No experiment selected")
		usage()
		sys.exit(2)
	
	db = []
	with open(dbfile, newline='') as csvfile:
		dbreader = csv.DictReader(csvfile,delimiter=';')
		
		for row in dbreader:
			app = row['APP']
			ja3 = row['JA3']
			sni = row['SNI']
			ja3s = row['JA3S']
			fingerprint = ja3+';'+ja3s+';'+sni
			
			if not any(x['APP'] == app for x in db):
				entry = {'APP': app, 'FINGERPRINTS': [fingerprint]}
				db.append(entry)
			else:	
				entry = list(filter(lambda x: x['APP'] == app, db))[0]
				db.remove(entry)
				if entry not in entry['FINGERPRINTS']:
					entry['FINGERPRINTS'].append(fingerprint)
				db.append(entry)
	
	fingerprints = []
	with open(ifile, newline='') as csvfile:
		tlsreader = csv.reader(csvfile,delimiter=';')
		for row in tlsreader:
			
			version = int(row[5], 16)
			cs = row[6]
			ext = row[7]

			# only found in Client Hello
			if row[4] == '1':
				sni = row[8]
				sg = row[9]
				ecFormat = int(row[10], 16)
				
				sg = sg.split(',')
				
				supportedGroups = ""
				for i in sg:
					val = int(i, 16)
					if not val in GREASE:
						supportedGroups += str(val) + '-'
				supportedGroups = supportedGroups[:-1]
				
			cs = cs.split(',')
			ext = ext.split(',')
			
			cipherSuite = ""
			for val in cs:
				if not val in GREASE:
					cipherSuite += str(val) + '-'
			cipherSuite = cipherSuite[:-1]
			
			extensions = ""
			for val in ext:
				if not val in GREASE:
					extensions += str(val) + '-'
			extensions = extensions[:-1]
			
			# Client Hello
			if row[4] == '1':
				key = row[0]+':'+row[1]+':'+row[2]
				string2hash = str(version)+","+cipherSuite+","+extensions+","+supportedGroups+','+str(ecFormat)
				ja3 = hashlib.md5(string2hash.encode()).hexdigest()
				entry = {'KEY': key, 'JA3': ja3, 'SNI': sni}
				if entry not in fingerprints:
					fingerprints.append(entry)
			# Server Hello
			else:
				key = row[1]+':'+row[0]+':'+row[3]
				string2hash = str(version)+","+cipherSuite+","+extensions
				ja3s = hashlib.md5(string2hash.encode()).hexdigest()
				entry = list(filter(lambda fingerprint: fingerprint['KEY'] == key, fingerprints))[0]
				fingerprints.remove(entry)
				entry['JA3S'] = ja3s
				if entry not in fingerprints:
					fingerprints.append(entry)
	
	print("JA3;JA3S;SNI;APP")
	for f in fingerprints:
		ja3 = f['JA3']
		sni = f['SNI']
		
		if "JA3S" not in f:
			continue
		
		ja3s = f['JA3S']
		
		toPrint = ja3+';'+ja3s+';'+sni
		
		#JA3+JA3S+SNI
		fingerprint = ja3+';'+ja3s+';'+sni
		entry = list(set([i for i,app in enumerate(db) for f in app['FINGERPRINTS'] if fingerprint in f]))
		if exp1 and len(entry) == 1:
			index = entry[0]
			print(toPrint+';'+db[index]['APP'])
		else:
			#JA3+JA3S
			fingerprint = ja3+';'+ja3s
			entry = list(set([i for i,app in enumerate(db) for f in app['FINGERPRINTS'] if fingerprint in f]))
			if exp2 and len(entry) == 1:
				index = entry[0]
				print(toPrint+';'+db[index]['APP'])
			else:
				#JA3
				fingerprint = ja3
				entry = list(set([i for i,app in enumerate(db) for f in app['FINGERPRINTS'] if fingerprint in f]))
				if exp3 and len(entry) == 1:
					index = entry[0]
					print(toPrint+';'+db[index]['APP'])
				else:
					#JA3S+SNI
					fingerprint = ja3s+';'+sni
					entry = list(set([i for i,app in enumerate(db) for f in app['FINGERPRINTS'] if fingerprint in f]))
					if exp4 and len(entry) == 1:
						index = entry[0]
						print(toPrint+';'+db[index]['APP'])
					else:
						print(toPrint+";unknown")
			
if __name__ == "__main__":
	main(sys.argv[1:])
