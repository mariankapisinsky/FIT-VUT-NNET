#
# Filter TLS Handshakes and Create All Unique JA3;SNI;JA3S Combinations
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

GREASE = ["2570","6682","10794","14906","19018","23130","27242","31354","35466","39578","43690","47802","51914","56026","60138","64250","65281"]

def usage():
	print('tlss2ja3.py --csv <csv> --sni <sni>')
	
def main(argv):
	ifile = ''
	snifile = ''
	
	try:
		opts, args = getopt.getopt(argv, "h", ["help", "csv=", "sni="])
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
		elif opt == "--sni":
			snifile = arg
	
	if not ifile or not snifile:
		print("Missing either input file or SNI file")
		usage()
		sys.exit(2)
		
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
				entry = {'key': key, 'ja3': ja3, 'sni': sni}
				if entry not in fingerprints:
					fingerprints.append(entry)
			# Server Hello
			else:
				key = row[1]+':'+row[0]+':'+row[3]
				string2hash = str(version)+","+cipherSuite+","+extensions
				ja3s = hashlib.md5(string2hash.encode()).hexdigest()
				entry = list(filter(lambda fingerprint: fingerprint['key'] == key, fingerprints))[0]
				fingerprints.remove(entry)
				entry['ja3s'] = ja3s
				if entry not in fingerprints:
					fingerprints.append(entry)
		
		sniList = []
		with open(snifile, newline='') as csvfile:
			snireader = csv.DictReader(csvfile,delimiter=';')
			for row in snireader:
				sniList.append(row['SNI'])
		
		db = []
		for entry in fingerprints:
			ja3 = entry['ja3']
			sni = entry['sni']
			
			if "ja3s" in entry:
				ja3s = entry['ja3s']
			
			if sni in sniList:
				entry = ja3+";"+sni+";"+ja3s
				if entry not in db:
					db.append(entry)
		db.sort()
					
		tmp = ifile.split('-')
		ofile = tmp[0] + "-db.csv"
		with open(ofile, 'w', newline='') as csvfile:
			csvfile.write("JA3;SNI;JA3S\n")
			for entry in db:
				csvfile.write(entry + '\n')

if __name__ == "__main__":
	main(sys.argv[1:])
