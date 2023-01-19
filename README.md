# NowPyPlaying

Python script to monitor MPD and create a plain text file of info on currently playing media for ready access by other programs.

In OBS create a text source, set it to 'Read from file' and select 'nowplaying.txt' as the file to read.

# Requirements

Intended for Linux as written but should work on any platform MPD supports by setting the configuration variables to reflect your OS and setup.
Windows users: change line 63 so that / is replaced with \ 

Requires python3 and python-mpd2

>pip3 install python-mpd2

# Config

Configuration defaults to "/home/*username*/.config/mpd/nowplaying.txt" for the output file and "localhost:6600" for the MPD server URL:port.

To change the default configs open nowpyplaying.py in a text editor and put your full path and filename in 'outfile'

>outfile="/path/to/file.txt"

and the MPD server details in 'mpdURL' and 'mpdPort'

>mpdURL=IPAddress/URL
>
>mpdPort=PortNumber
