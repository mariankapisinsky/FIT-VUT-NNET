#!/bin/bash

#
# Extract TLS Infromation from PCAP Files
# PDS 2021 - Identification of Mobile Traffic using TLS Fingerprinting
# Bc. Marian Kapisinsky, xkapis00
# 25.4.2021
#

echo "Extracting..."

for file in "$@"
do
echo $file
tshark -r $file -T fields -E separator=";" -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tls.handshake.type -e tls.handshake.version -e tls.handshake.ciphersuite -e tls.handshake.extension.type -e tls.handshake.extensions_server_name -e tls.handshake.extensions_supported_group -e tls.handshake.extensions_ec_point_format -R "tls.handshake.type==1 or tls.handshake.type==2" -2 > ${file%.*}-tlss.csv
done

echo "Done."
