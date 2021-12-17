# GAL 2021 - Longest Path Problem
This is the school project for the GAL course (Graph Algorithms).
The task was to implement an exact algorithm and two approximation/heuristic algorithms for the Longest Path Problem in general directed weighted graphs.

Usage:
```console
$ python graph.py -h -v -b -g <num> -s <num> -n <num> -d <num>

## Options

| Option | Description                        |
|--------|------------------------------------|
|  `-h`  | this text you see right here       |
|  `-v`  | print the randomly generated graph |
|  `-b`  | run brute force search             |
|  `-g`  | run k-lookahead greedy search      |
|  `-s`  | run k-step greedy lookahead        |
|  `-n`  | set number of nodes                |
|  `-d`  | set maximum node outdegree         |
