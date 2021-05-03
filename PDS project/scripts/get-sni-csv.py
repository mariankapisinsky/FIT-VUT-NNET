#
# Get Unique ip.src;ip.dst;SNI Combination from CSV
# PDS 2021 - Identification of Mobile Traffic using TLS Fingerprinting
# Bc. Marian Kapisinsky, xkapis00
# 25.4.2021
#

import sys, getopt
import csv

def usage():
	print('get-sni-list.py --csv <csv> [{-k | --keywords} <keyword1,keyword2,...>]')

def main(argv):
	ifile = ''
	keywords = []
	
	try:
		opts, args = getopt.getopt(argv, "hk:", ["help", "csv=", "keywords="])
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
		elif opt == "-k" or opt == "--keywords":
			keywords = arg.split(',')	
				
	sniList = []
	with open(ifile, newline='') as csvfile:
		tlsreader = csv.reader(csvfile,delimiter=';')
		for row in tlsreader:
			sni = row[8]
			if keywords:
				for key in keywords:
					if key in sni:
						entry = row[0]+';'+row[1]+';'+sni
						if entry not in sniList:
							sniList.append(entry)
			elif sni:
				entry = row[0]+';'+row[1]+';'+sni
				if entry not in sniList:
					sniList.append(entry)
	
	tmp = ifile.split('-')
	if keywords:
		ofile = tmp[0] + "-sni-filtered.csv"
	else:
		ofile = tmp[0] + "-sni.csv"
	with open(ofile, 'w', newline='') as snifile:
		snifile.write("ip.src;ip.dst;SNI\n")
		for entry in sniList:
			snifile.write(entry + '\n')
	
if __name__ == "__main__":
	main(sys.argv[1:])
