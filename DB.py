__author__ = 'Lewis England'

import sqlite3
conn = sqlite3.connect(":memory:")
db = conn.cursor()

def createTables():
    # Create the database tables
    ## Artists
    db.execute ('''CREATE TABLE artists (
    ID INTEGER PRIMARY KEY,
    G_ID TEXT,
    NAME TEXT,
    ART_URL TEXT
    )''')

    ## Albums
    db.execute ('''CREATE TABLE albums (
    ID INTEGER PRIMARY KEY,
    G_ID TEXT,
    TITLE TEXT,
    ARTIST_ID INTEGER,
    ART_URL TEXT,
    DISC_CNT INT,
    TRACK_CNT INT
    )''') #, cover_url, cover_width, cover_height, discs int)''' )

    ## Songs
    db.execute ('''CREATE TABLE songs (
    ID INTEGER PRIMARY KEY,
    G_ID TEXT,
    TITLE TEXT,
    ALBUM_ID INTEGER,
    ARTIST_ID INTEGER
    )''')
    conn.commit()

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

def findAlbumId(albumName, artistId, gId, artworkUrl):
    db.execute("SELECT ID FROM albums WHERE TITLE = ?",(albumName,))
    album_id = db.fetchone()
    if album_id is None:
        db.execute('INSERT INTO albums (G_ID, TITLE, ARTIST_ID, ART_URL) VALUES (?,?,?,?)',
                   (gId,albumName,artistId,artworkUrl,))
        conn.commit()
        db.execute('SELECT last_insert_rowid()')
        conn.commit()
        return db.fetchone()[0]
    else:
        return album_id[0]

def addSong(gId, title, albumId, artistId):
    db.execute('INSERT INTO songs (G_ID, TITLE, ALBUM_ID, ARTIST_ID) VALUES (?,?,?,?)',
               (gId,title,albumId,artistId))
    conn.commit()

def allSongs():
    db.execute('SELECT * FROM songs')
    return db.fetchall()

def lookupAlbum(album_id):
    db.execute('SELECT title FROM albums WHERE ID = ' + str(album_id))
    if db.rowcount > 0:
        return db.fetchone()[0]
    else:
        return str(db.fetchone())

def lookupAlbumArt(album_id):
    db.execute('SELECT art_url FROM albums WHERE ID = ' + str(album_id))
    if db.rowcount > 0:
        return db.fetchone()[0]
    else:
        return str(db.fetchone())

def lookupArtist(artist_id):
    db.execute('SELECT name FROM artists WHERE ID = ' + str(artist_id))
    if db.rowcount > 0:
        return db.fetchone()[0]
    else:
        return str(db.fetchone())

def lookupArtistArt(artist_id):
    db.execute('SELECT art_url FROM artists WHERE ID = ' + str(artist_id))
    if db.rowcount > 0:
        return db.fetchone()[0]
    else:
        return str(db.fetchone())

# Create the database tabled when the app is initially run
createTables()