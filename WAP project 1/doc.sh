#!/bin/sh

if [ `npm list | grep -c jsdoc` -eq 0 ]; then
    npm install jsdoc
fi

jsdoc -c ./jsdoc.json