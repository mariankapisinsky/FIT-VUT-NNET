# PDS 2021 - Identification of Mobile Traffic using TLS Fingerprinting
This is the school project for the PDS course (Data Communications, Computer Networks and Protocols).
The assignment was Identification of Mobile Traffic using TLS Fingerprinting.

## Scripts

All scripts were written in either Bash or Python 3 on Kali Linux.
The stat.py python script requires numpy, matplotlib, and sklearn libs.

| Script            | Description
|-------------------|-----------------------
| `extract.sh`      | Extract TLS Infromation from PCAP Files
| `get-sni-csv.py`  | Get Unique ip.src;ip.dst;SNI Combination from CSV
| `tlss2ja3.py`     | Filter TLS Handshakes and Create All Unique JA3;SNI;JA3S Combinations
| `create_db.sh`    | Create Fingerprints Database from CSV Files
| `test.py`         | Testing Script
| `stat.py`         | Calculate Confusion Matrix and Other Statistics

Usage:

```console
$ ./extract.sh <PCAP files>
```

```console
$ get-sni-list.py --csv <csv> [{-k | --keywords} <keyword1,keyword2,...>]
```

```console
$ python3 tlss2ja3.py --csv <app>-tlss.csv --sni <app>-sni-filtered.csv
```

```console
$ ./create_db.sh <app1-db.csv, app2-db.csv, ...>
```

```console
$ test.py --csv <csv> --db <db> {-1|-2|-3|-4}
```

```console
$ stat.py predicted.csv real.txt
```