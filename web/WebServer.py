__author__ = 'Lewis England'

import DB
import urllib
import SocketServer
import SimpleHTTPServer
from PIL import ImageFile

PORT = 8000
REPORT_FILE = "index.html"


def stringify(input_string):
    try:
        output = input_string.encode('ascii')
    except UnicodeError:
        output = input_string.encode('utf-16')[2:]
    return output


def initialise():
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), handler)
    print "serving at port", PORT
    httpd.serve_forever()


def getDimensions(song_hash, image):
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


def generateReport():
    report = open(REPORT_FILE, 'w')
    report.write('<html><head><link rel="stylesheet" type="text/css" href="web/report.css"></head>'
                 '<body>' + "\n")
    report.write('<h1>You have ' + DB.count('songs') + ' songs by ' + DB.count('artists') + ' artists over ' + DB.count('albums') + ' albums.</h1><br/>' + "\n")
    report.write('<table border="1"><tr><th colspan="4">GMusic Manager Report</th></tr>' + "\n")
    report.write('<tr><td><b>Title</b></td><td><b>Artist</b></td><td><b>Album</b></td><td><b>Artwork</b></td></tr>' + "\n")
    for song in DB.allSongs():
        SONG_ID = song[0]
        SONG_GOOGLE_ID = stringify(song[1])
        SONG_TRACK_NO = song[2]
        SONG_TITLE = stringify(song[3])
        ALBUM_TITLE = stringify(DB.lookupAlbum(song[4]))
        ALBUM_DISC_NO = DB.lookupAlbumDiscNo(song[4])
        ALBUM_TRACK_COUNT = DB.lookupAlbumTrackCount(song[4])
        ALBUM_ART = stringify(DB.lookupAlbumArt(song[4]))
        if ALBUM_ART != 'NULL':
            ALBUM_ART_HW = getDimensions(SONG_GOOGLE_ID, ALBUM_ART)[1]
            ALBUM_ART_W = ALBUM_ART_HW[0]
            ALBUM_ART_H = ALBUM_ART_HW[1]
            if ALBUM_ART_H != ALBUM_ART_W:
                ALBUM_ART_CSS = 'irregular_dimensions'
            elif ALBUM_ART_W < 200:
                ALBUM_ART_CSS = 'low_quality'
            elif ALBUM_ART_W < 500:
                ALBUM_ART_CSS = 'med_quality'
            else:
                ALBUM_ART_CSS = 'hi_quality'
        ARTIST_NAME = stringify(DB.lookupArtist(song[5]))
        ARTIST_ART = stringify(DB.lookupArtistArt(song[5]))
        SONG_DURATION = song[6]
        x = SONG_DURATION / 1000
        seconds = x % 60
        x /= 60
        minutes = x % 60
        SONG_SIZE = float(song[7])
        converted_size = "{0:.2f}".format(round(SONG_SIZE / 1048576, 2))
        report.write('<tr><td>' + SONG_TITLE + '<br/>'
                     'Track ' + str(SONG_TRACK_NO) + '/' +str(ALBUM_TRACK_COUNT) + '<br/>' +
                     str(minutes) + ':' + str(seconds).zfill(2) + '<br/>' +
                     str(converted_size) + 'mb'
                     '</td>'
                     '<td>' + ARTIST_NAME + '</td>'
                     '<td>' + ALBUM_TITLE + '<br/>Disc ' + str(ALBUM_DISC_NO) + '</td>')
        if ALBUM_ART != 'NULL':
            report.write('<td class="' + ALBUM_ART_CSS + '"><a href="' + ALBUM_ART + '"><img src="' + ALBUM_ART + '" width="100px" height="100px">'
                         '<br/>' + str(ALBUM_ART_H) + 'x' + str(ALBUM_ART_W) + '</a></td></tr>' + "\n")
        else:
            report.write('<td>No Image</td><tr>' + "\n")
    report.write('</table></body></html>')
    report.close()
    initialise()
