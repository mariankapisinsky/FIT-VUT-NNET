# FLP 2021 - bkg-2-cnf
This the school project No. 1 for the FLP course (Functional and Logic Programming).
The assignment was to implement some algorithms for Context-Free Languages in Haskell.

Usage with stdin:
```console
$ ./bkg-2-cnf {-i|-1|-2}
```

Usage with a file:
```console
$ ./bkg-2-cnf {-i|-1|-2} FILE
```

## Options

| Option | Description         |
|--------|---------------------|
|  `-i`  | Print unchanged CFG |
|  `-1`  | Remove simple rules |
|  `-2`  | Chomsky Normal From |

## Source files (src/)

| Source file  | Description
|--------------|-----------------------
| `Main.hs`    | Parses the command line options and handles the program's operation
| `Parser.hs`  | Parses the given CFG and creates its intern representation
| `Types.hs`   | Data types and some useful functions
| `Simple.hs`  | Implements the removal of simple rules
| `Chomsky.hs` | Implements the creation of the Chomsky Normal Form

## Test files (test/)

Contains some input and output test files used for testing.
