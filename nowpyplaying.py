#!/usr/bin/python3
#MPD monitor for writing 'now playing' details to a file to be picked up by OBS

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
    client.connect("localhost",6600)
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
            outstr=(f"""{cursong["title"]} by {cursong["albumartist"]}
{cursong["album"]}""")
            print("success")
        except KeyError:
            outstr=(f"""{cursong["title"]} by {cursong["artist"]}
{cursong["album"]}""")
            print("no albumartist tag")
        except:
            outstr="Error fetching track info"
            print("multiple errors")
            False
        finally:
            print(outstr)
    #call write function here write(outstr)
    f=open(outfile,"w")
    f.write(outstr)
    f.close()
    client.idle('player')

sys.exit(0)
