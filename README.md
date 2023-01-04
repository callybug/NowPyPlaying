# NowPyPlaying

Python script to monitor MPD and create a plain text file of info on currently playing media for ready access by other programs.

Requires python-mpd2

>pip3 install python-mpd2

# Config

Configuration defaults to "/home/*username*/.config/mpd/nowplaying.txt" for the output file and "localhost:6600" for the MPD server URL:port.

To change the default configs open nowpyplaying.py in a text editor and put your full path and filename in 'outfile'

>outfile="/path/to/file.txt"

and the MPD server details in 'mpdURL' and 'mpdPort'

>mpdURL=IPAddress/URL
>
>mpdPort=PortNumber