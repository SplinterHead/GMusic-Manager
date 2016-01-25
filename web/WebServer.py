__author__ = 'Lewis England'

import DB
import urllib
import SocketServer
import SimpleHTTPServer
from PIL import ImageFile

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

def getDimensions(song_hash, image):
    # get file size *and* image size (None if not known)
    imageFile = urllib.urlopen(image)
    size = imageFile.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = imageFile.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    imageFile.close()
    return size, None
    # (10965, (179, 188))

def generateReport():
    report = open(REPORT_FILE, 'w')
    report.write('<html><body>' + "\n")
    report.write('<h1>You have ' + DB.count('songs') + ' songs by ' + DB.count('artists') + ' artists over ' + DB.count('albums') + ' albums.</h1><br/>' + "\n")
    report.write('<table border="1"><tr><th colspan="4">GMusic Manager Report</th></tr>' + "\n")
    report.write('<tr><td><b>Title</b></td><td><b>Artist</b></td><td><b>Album</b></td><td><b>Artwork</b></td></tr>' + "\n")
    for song in DB.allSongs():
        SONG_ID = song[0]
        SONG_GOOGLE_ID = stringify(song[1])
        SONG_TITLE = stringify(song[2])
        ALBUM_TITLE = stringify(DB.lookupAlbum(song[3]))
        ALBUM_ART = stringify(DB.lookupAlbumArt(song[3]))
        if ALBUM_ART != 'NULL':
            ALBUM_ART_HW = getDimensions(SONG_GOOGLE_ID, ALBUM_ART)[1]
            ALBUM_ART_W = ALBUM_ART_HW[0]
            ALBUM_ART_H = ALBUM_ART_HW[1]
        ARTIST_NAME = stringify(DB.lookupArtist(song[4]))
        ARTIST_ART = stringify(DB.lookupArtistArt(song[4]))
        report.write('<tr><td>' + SONG_TITLE + '</td>'
                     '<td>' + ARTIST_NAME + '</td>'
                     '<td>' + ALBUM_TITLE + '</td>')
        if ALBUM_ART != 'NULL':
            report.write('<td><a href="' + ALBUM_ART + '"><img src="' + ALBUM_ART + '" width="200px" height="200px">'
                         '<br/>' + str(ALBUM_ART_H) + 'x' + str(ALBUM_ART_W) + '</a></td></tr>' + "\n")
        else:
            report.write('<td>No Image</td><tr>' + "\n")
    report.write('</table></body></html>')
    report.close()
    initialise()