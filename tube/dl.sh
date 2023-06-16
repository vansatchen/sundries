#!/bin/bash

if [ -z "$1" ]; then
  url=https://url.com/onlinehdclub
else
  url=$1
fi

while true
do
  /path/to/yt-dlp -S res:1080 $url -P home:/path/to/video/ > /dev/null 2>&1
  if [[ $? == "0" ]]; then
    echo "Recorded"
  fi
  sleep 5
done
