PROGRAM = bkg-2-cnf
FILES = src/*.hs test/* Makefile README
SRC = src/*.hs
FLAGS = --make -o

all: $(PROGRAM)

$(PROGRAM): $(SRC)
	ghc $(FLAGS) ${PROGRAM} $(SRC)

clean:
	rm src/*.o src/*.hi ${PROGRAM}

zip:
	zip flp-fun-xkapis00.zip ${FILES}