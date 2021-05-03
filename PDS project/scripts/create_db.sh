#!/bin/bash

#
# Create Fingerprints Database from CSV Files
# PDS 2021 - Identification of Mobile Traffic using TLS Fingerprinting
# Bc. Marian Kapisinsky, xkapis00
# 25.4.2021
#

db=fingerprints-db.csv

echo "Creating db..."

if [[ -f "$db" ]]; then
	rm $db
fi

echo "APP;JA3;SNI;JA3S" > $db

for file in "$@"; do
	echo "$file"
	sed 1d $file | while read -r line; do
		echo "${file%-*};$line" >> $db
	done
done

echo "Done."

