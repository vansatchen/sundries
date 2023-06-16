#!/bin/bash

link="rtmp://3.livacha.com:1935/live/myr_128741_101820?vhost=live"

while true
do
  recDate=$(date +"%d%m%y_%H-%M")
  ffmpeg -hide_banner -loglevel 0 -y -rw_timeout 5000000 -i $link -c copy -f mp4 MYP_$recDate.mp4
  if [[ $? == "0" ]]; then
    echo "Recorded"
  fi
  sleep 5
done
