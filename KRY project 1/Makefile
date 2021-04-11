CC=g++
CCFLAGS=-std=c++11 -Werror -Wall

all: kry

kry: kry.cpp kry.hpp
	$(CC) $(CCFLAGS) src/kry.cpp -o kry

tar:
	tar -cvf xkapis00.tar *

clean:
	rm -rf kry xkapis00.tar