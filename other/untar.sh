#!/bin/bash

# This small script untar multiple archive in current directory

targzs=`ls *.tar.gz`

for targz in $targzs; do
	tar xfz $targz && rm $targz
done

exit 0

