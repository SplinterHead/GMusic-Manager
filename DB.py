__author__ = 'Lewis England'

import sqlite3

## Set up sqlite to return dictionaries
def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect(":memory:")
##conn.row_factory = dict_factory
db = conn.cursor()


def createTables():
    # Create the database tables
    ## Artists
    db.execute('''CREATE TABLE artists (
    ID INTEGER PRIMARY KEY,
    G_ID TEXT,
    NAME TEXT,
    ART_URL TEXT
    )''')

    ## Albums
    db.execute('''CREATE TABLE albums (
    ID INTEGER PRIMARY KEY,
    G_ID TEXT,
    TITLE TEXT,
    DISC_CNT INT,
    DISC_NO INTEGER,
    TRACK_CNT INTEGER,
    ARTIST_ID INTEGER,
    ART_URL TEXT
    )''')

    ## Songs
    db.execute('''CREATE TABLE songs (
    ID INTEGER PRIMARY KEY,
    G_ID TEXT,
    TRACK_NO INTEGER,
    TITLE TEXT,
    ALBUM_ID INTEGER,
    ARTIST_ID INTEGER,
    DURATION INTEGER,
    SIZE INTEGER
    )''')
    conn.commit()


def isLoaded():
    db.execute('SELECT * FROM songs')
    if len(db.fetchall()) == 0:
        return False
    else:
        return True


def findArtistId(artistName, gId, artworkUrl):
    db.execute("SELECT ID FROM artists WHERE NAME = ?",(artistName,))
    artist_id = db.fetchone()
    if artist_id is None:
        db.execute('INSERT INTO artists (G_ID, NAME, ART_URL) VALUES (?,?,?)',
                   (gId,artistName,artworkUrl,))
        conn.commit()
        db.execute('SELECT last_insert_rowid()')
        conn.commit()
        return db.fetchone()[0]
    else:
        return artist_id[0]


def findAlbumId(albumName, discNo, trackCount, artistId, gId, artworkUrl):
    db.execute("SELECT ID FROM albums WHERE TITLE = ?",(albumName,))
    album_id = db.fetchone()
    if album_id is None:
        db.execute('INSERT INTO albums (G_ID, TITLE, DISC_NO, TRACK_CNT, ARTIST_ID, ART_URL) VALUES (?,?,?,?,?,?)',
                   (gId,albumName,discNo,trackCount,artistId,artworkUrl,))
        conn.commit()
        db.execute('SELECT last_insert_rowid()')
        conn.commit()
        return db.fetchone()[0]
    else:
        return album_id[0]


def addSong(gId, trackNo, title, albumId, artistId, duration, size):
    db.execute('INSERT INTO songs (G_ID, TRACK_NO, TITLE, ALBUM_ID, ARTIST_ID, DURATION, SIZE) VALUES (?,?,?,?,?,?,?)',
               (gId,trackNo,title,albumId,artistId,duration,size))
    conn.commit()


def allData(table):
    db.execute("SELECT * FROM %s" % table)
    return db.fetchall()


def count(table):
    db.execute('SELECT Count(*) FROM ' + table)
    return str(db.fetchone()[0]) or None


def fetchDataById(table, table_id):
    db.execute('SELECT * FROM %s WHERE ID = %s' % (table, table_id))
    return db.fetchone() or None


def fetchAlbumTracklist(album_id):
    db.execute('SELECT * FROM songs WHERE album_id = ' + str(album_id) + ' ORDER BY TRACK_NO')
    return db.fetchall() or None


def fetchArtistAlbums(artist_id):
    db.execute('SELECT * FROM albums WHERE ARTIST_ID = ' + str(artist_id))
    return db.fetchall() or None


def lookupAlbum(album_id):
    db.execute('SELECT title FROM albums WHERE ID = ' + str(album_id))
    return db.fetchone()[0] or None


def lookupAlbumDiscNo(album_id):
    db.execute('SELECT disc_no FROM albums WHERE ID = ' + str(album_id))
    return db.fetchone()[0] or None


def lookupAlbumTrackCount(album_id):
    db.execute('SELECT track_cnt FROM albums WHERE ID = ' + str(album_id))
    return db.fetchone()[0] or None


def lookupAlbumArt(album_id):
    db.execute('SELECT art_url FROM albums WHERE ID = ' + str(album_id))
    return db.fetchone()[0] or None


def lookupArtist(artist_id):
    db.execute('SELECT name FROM artists WHERE ID = ' + str(artist_id))
    return db.fetchone()[0] or None


def lookupArtistArt(artist_id):
    db.execute('SELECT art_url FROM artists WHERE ID = ' + str(artist_id))
    return db.fetchone()[0] or None

# Create the database tabled when the app is initially run
createTables()
