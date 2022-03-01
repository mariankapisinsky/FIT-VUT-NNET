#!/bin/sh

if [ `npm list | grep -c fs` -eq 0 ]; then
    npm install fs
fi

node ./test.mjs tests/test1.in
node ./test.mjs tests/test2.in
node ./test.mjs tests/test3.in
node ./test.mjs tests/test4.in