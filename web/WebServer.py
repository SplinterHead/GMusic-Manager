__author__ = 'Lewis England'

import DB
import SocketServer
import SimpleHTTPServer

PORT = 8000
REPORT_FILE = "index.html"

def initialise():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT
    httpd.serve_forever()

def generateReport():
    report = open(REPORT_FILE, 'w')
    report.write('<html><body><table border="1"><tr><th colwidth="3">GMusic Manager Report</th></tr>')
    report.write('<tr><td><b>Title</b></td><td><b>Artist</b></td><td><b>Album</b></td></tr>')
    for song in DB.allSongs():
        SONG_ID = song[0]
        SONG_TITLE = song[1].encode('utf-8').strip()
        ARTIST_NAME = DB.lookupArtist(song[2])
        ALBUM_TITLE = DB.lookupAlbum(song[3])
        report.write('<tr><td>' + SONG_TITLE + '</td><td>' + ARTIST_NAME + '</td><td>' + ALBUM_TITLE + '</td></tr>')
    report.write('</table></body></html>')
    report.close()
    initialise()
