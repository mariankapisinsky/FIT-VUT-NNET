#!/bin/sh

if [ `npm list -g | grep -c jsdoc` -eq 1 ]; then
    jsdoc -c ./jsdoc.json
else
    npx jsdoc -c ./jsdoc.json
fi
