__author__ = 'Lewis England'

import DB
import SocketServer
import SimpleHTTPServer

PORT = 8000
REPORT_FILE = "index.html"

def stringify(input):
    try:
        output = input.encode('ascii')
    except UnicodeError:
        output = input.encode('utf-16')[2:]
    return output

def initialise():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT
    httpd.serve_forever()

def generateReport():
    report = open(REPORT_FILE, 'w')
    report.write('<html><body><table border="1"><tr><th colspan="3">GMusic Manager Report</th></tr>')
    report.write('<tr><td><b>Title</b></td><td><b>Artist</b></td><td><b>Album</b></td></tr>')
    for song in DB.allSongs():
        SONG_ID = song[0]
        SONG_GOOGLE_ID = stringify(song[1])
        SONG_TITLE = stringify(song[2])
        ALBUM_TITLE = stringify(DB.lookupAlbum(song[3]))
        ARTIST_NAME = stringify(DB.lookupArtist(song[4]))
        report.write('<tr><td>' + SONG_TITLE + '</td><td>' + ARTIST_NAME + '</td><td>' + ALBUM_TITLE + '</td></tr>')
    report.write('</table></body></html>')
    report.close()
    initialise()