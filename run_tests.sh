#!/bin/bash

python3.9 -m unittest -v

ERR_CODE=$?

if [[ $ERR_CODE != 0 ]]
then
  exit 1
fi