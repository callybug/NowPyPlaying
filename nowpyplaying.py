#!/usr/bin/python3
#MPD monitor for writing 'now playing' details to a file to be picked up by OBS
#Originally written by Sithrazer, modified by callybug
#Edited to show either "artist - filename" or "filename" (with path and extensions removed), when there are no other tags found. Otherwise it'd crash for the folks who are lazy with their tagging (like me).

#TODO
#figure out system to display license info for royalty free artists that require it
#figure out method for user friendly clean shutdown

import sys
import os.path as path
from mpd import MPDClient

### CONFIG ###
#Enter the complete path and filename for the file OBS will read the information from
outfile=path.expanduser("~/.config/mpd/nowplaying.txt")

#Enter MPD connection details
mpdURL="localhost"
mpdPort=6600
### END CONFIG ###

client = MPDClient()
client.timeout = 5
try:
    client.connect(mpdURL,mpdPort)
    print(client.mpd_version)
except:
    print("Could not connect to MPD")
    sys.exit(1)

#Sane variable defaults to ensure clean starts
prevsong=0
outstr=" "

while True:
    status=client.status()
    cursong=client.currentsong()
    audioextensions=[".flac",".ogg", ".opus",".mp3",".webm",".m4a",".wav",".wma", ".mp4", ".mkv"]
    print(status["state"])
    if status["state"] == "pause" or status["state"] == "stop":
        #no song playing; blank file
        outstr=" "
        #set prevsong to '0' so file will update when playback resumes
        prevsong=0
    elif status["songid"] == prevsong:
        #exists just to catch erronious exit from client.idle()
        print("same song still playing; no need to update file")
        #pass
    else:
        try:
            outstr=(f"""{cursong["albumartist"]} - {cursong["title"]}""")
            print(outstr)
        except KeyError:
              try:
                  outstr=(f"""{cursong["artist"]} - {cursong["title"]}""")
                  print(outstr)
              except KeyError:
                               try:
                                   outstr=(f"""{cursong["file"]}""")
                                   slashCount = 0
                                   for i in outstr:
                                         if i == '/':
                                             slashCount = slashCount + 1
                                   noPath = outstr.split('/')[slashCount]
                                   a=0
                                   for x in range(len(audioextensions)):
                                         formatcheck = audioextensions[a]
                                         a=a+1
                                         NoExt = noPath.replace(formatcheck,'')
                                         noPath=NoExt
                                   noPathExt=NoExt
                                   outstr=(f"""{cursong["artist"]} - {noPathExt}""")
                                   print(outstr)
                               except KeyError:
                                             try:
                                                       outstr=noPathExt
                                             finally:
                                                       print(outstr)
    #call write function here write(outstr)
    f=open(outfile,"w")
    f.write(outstr)
    f.close()
    client.idle('player')

sys.exit(0)
