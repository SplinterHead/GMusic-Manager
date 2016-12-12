__author__ = 'Lewis England'

import DB
import urllib
import SocketServer
import SimpleHTTPServer
from PIL import ImageFile
from flask import render_template


def stringify(input_string):
    try:
        output = input_string.encode('ascii')
    except UnicodeError:
        output = input_string.encode('utf-16')[2:]
    return output


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

def implementTemplate():
    return render_template('songs.html',
                           song_count=DB.count('songs'),
                           artist_count=DB.count('artists'),
                           album_count=DB.count('albums')
                          )


def generateReport():
    indexPage = '<h1>You have ' + DB.count('songs') + ' songs by ' + DB.count('artists') + ' artists over ' + DB.count('albums') + ' albums.</h1><br/>'
    indexPage += '<table border="1"><tr><th colspan="4">GMusic Manager Report</th></tr>'
    indexPage += '<tr><td><b>Title</b></td><td><b>Artist</b></td><td><b>Album</b></td><td><b>Artwork</b></td></tr>'
    for song in DB.allData('songs'):
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
        indexPage += '<tr><td>' + SONG_TITLE + '<br/>'
        indexPage += 'Track ' + str(SONG_TRACK_NO) + '/' +str(ALBUM_TRACK_COUNT) + '<br/>'
        indexPage += str(minutes) + ':' + str(seconds).zfill(2) + '<br/>'
        indexPage += str(converted_size) + 'mb'
        indexPage += '</td>'
        indexPage += '<td>' + ARTIST_NAME + '</td>'
        indexPage += '<td>' + ALBUM_TITLE + '<br/>Disc ' + str(ALBUM_DISC_NO) + '</td>'
        if ALBUM_ART != 'NULL':
            indexPage += '<td class="' + ALBUM_ART_CSS + '"><a href="' + ALBUM_ART + '"><img src="' + ALBUM_ART + '" width="100px" height="100px">'
            indexPage += '<br/>' + str(ALBUM_ART_H) + 'x' + str(ALBUM_ART_W) + '</a></td></tr>'
        else:
            indexPage += '<td>No Image</td><tr>'
    return indexPage
