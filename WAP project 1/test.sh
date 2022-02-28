#!/bin/sh

if [ `npm list | grep -c fs` -eq 0 ]; then
    npm install fs
fi

node ./test.mjs tests/test1.in