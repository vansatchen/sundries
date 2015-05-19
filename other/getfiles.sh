#!/bin/bash

# This small script using for get all emails for user@example.com from archive

dirswithfiles=`ls -d */`
emailforsearch="user@example.com"
dirwithfoundedfiles="/path/to/backup/founded"

for dirwithfiles in $dirswithfiles; do
	filesindir=`ls $dirwithfiles`
		for fileindir in $filesindir; do
			grep -w $emailforsearch $dirwithfiles$fileindir > /dev/null
			if [ $? -eq 0 ]; then
				cp $dirwithfiles$fileindir $dirwithfoundedfiles/
				echo "Copy founded $dirwithfiles$fileindir to $dirwithfoundedfiles"
			fi
		done
done

echo "done!"

exit 0

