#!/usr/bin/python3

import sys, os
import subprocess

# Check that argument exists
if len(sys.argv) < 2:
    print("\033[31mNeed arguments like\033[0m   makeSplits.sh chembaby   \033[31mto split all of chembaby_*\033[0m")
    sys.exit(1)

correctArg = sys.argv[1]
fileList = []

for file in os.listdir("./"):
    if correctArg in file and file.endswith(".mp4"): fileList.append(file)

# Check that needed files exists
if len(fileList) == 0:
    print("\033[31mNo files like\033[0m " + correctArg)
    sys.exit(1)

# Make ts files for split
for file in fileList:
    p = subprocess.Popen(["ffmpeg", "-i", file, "-acodec", "copy", \
                          "-vcodec", "copy", "-vbsf", "h264_mp4toannexb", \
                          "-f", "mpegts", file[:-4] + ".ts"])
    p.communicate()

# Make split of all generated ts
fileList.clear()
for file in os.listdir("./"):
    if file.endswith(".ts"): fileList.append(file)

tsList = "concat:"
for file in fileList:
    tsList = tsList + file + "|"

tsList = tsList[:-1]
p = subprocess.Popen(["ffmpeg", "-i", tsList, "-c:v", "copy", correctArg + "date.mp4"])
p.communicate()
