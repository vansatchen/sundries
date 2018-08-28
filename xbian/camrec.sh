#!/bin/sh

# Some script for record from web-camera with mjpeg.
# Developed by Nikolay Pavlov aka rusatch. 2014.

#PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/sbin:/opt/bin:/opt/sbin
DIROUT=/mnt/nas/HD_b2/smb/raspi
OLDDIRHOUR=`/bin/date --date="1 days ago" +%d-%m-%H.%M`
#if [ -f "$DIROUT/$OLDDIRHOUR.mkv" ]; then
        rm -f $DIROUT/$OLDDIRHOUR.mkv
#fi

DIRHOUROUT=`/bin/date +%d-%m-%H.%M`
FFMETADATA="-metadata title=$DIRHOUROUT -metadata comment=hall@home"
/usr/local/bin/ffmpeg -i rtsp://127.0.0.1:8554/unicast -t 00:30:00 -vcodec copy -an $FFMETADATA $DIROUT/$DIRHOUROUT.mkv -y
#/usr/local/bin/ffmpeg -f v4l2 -i /dev/video0 -t 00:30:00 -vcodec copy -an $DIROUT/$DIRHOUROUT.mkv -y
#echo $FFMETADATA

# rm .nfsXXX files
rm -f /mnt/nas/HD_b2/smb/raspi/.nfs*

exit 0

