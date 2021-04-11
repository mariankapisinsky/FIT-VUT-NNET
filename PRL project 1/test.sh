#!/bin/bash

mpic++ -std=c++11 --prefix /usr/local/share/OpenMPI -o pms pms.cpp

dd if=/dev/random bs=1 count=16 of=numbers > /dev/null 2>&1

mpirun --prefix /usr/local/share/OpenMPI -np 5 pms

rm -f pms numbers
