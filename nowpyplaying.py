#!/usr/bin/python3
#MPD monitor for writing 'now playing' details to a file to be picked up by OBS

#figure out system to display license info for royalty free artists that require it

#call client.close() before any sleep commands (may not need with using idle)
#use client.idle('player') to delay cycling of main loop until there's a change in play status
#use client.status() "state" to check mpd is playing anything; blank file or write to file as appropriate
#use client.status() "songid" to check if same song is still playing before write to file
#figure out flow control to write to file after resuming from pause (set playlist song number back to zero on pause)

import sys
from mpd import MPDClient

outfile="/home/sithrazer/.config/mpd/nowplaying"

client = MPDClient()
client.timeout = 5
try:
    client.connect("localhost",6600)
    print(client.mpd_version)
    #print(client.status())
    #print(client.currentsong())
except:
    print("Could not connect to MPD")
    sys.exit(1)

#set up vars here to avoid reinitialising every loop
prevsong=0 #songid starts at index 1; 0 guarantees fresh read on load
outstr=""

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
        pass
        #same song still playing; no need to update file
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

#print(client.status())
#print(client.stats())
#client.close()
#client.disconnect()
sys.exit(0)

#function to handle writing to file

#function to handle building string
