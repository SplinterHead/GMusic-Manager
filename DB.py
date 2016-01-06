__author__ = 'Lewis England'

import sqlite3
conn = sqlite3.connect(":memory:")
db = conn.cursor()

def createTables():
    # Create the database tables
    ## Artists
    db.execute ('''CREATE TABLE artists (
    ID INTEGER PRIMARY KEY,
    NAME TEXT
    )''')

    ## Albums
    db.execute ('''CREATE TABLE albums (
    ID INTEGER PRIMARY KEY,
    TITLE TEXT,
    ARTIST_ID INTEGER
    )''') #, cover_url, cover_width, cover_height, discs int)''' )

    ## Songs
    db.execute ('''CREATE TABLE songs (
    ID INTEGER PRIMARY KEY,
    TITLE TEXT,
    ALBUM_ID INTEGER,
    ARTIST_ID INTEGER
    )''')
    conn.commit()

def findArtistId(artistName):
    db.execute("SELECT ID FROM artists WHERE NAME = ?",(artistName,))
    artist_id = db.fetchone()
    if artist_id is None:
        db.execute('INSERT INTO artists (NAME) VALUES (?)',(artistName,))
        conn.commit()
        return db.lastrowid
    else:
        return artist_id[0]

def findAlbumId(albumName):
    db.execute("SELECT ID FROM albums WHERE TITLE = ?",(albumName,))
    album_id = db.fetchone()
    if album_id is None:
        db.execute('INSERT INTO albums (TITLE) VALUES (?)',(albumName,))
        conn.commit()
        return db.lastrowid
    else:
        return album_id[0]

def addSong(title, artist, album):
    db.execute('INSERT INTO songs (TITLE, ALBUM_ID, ARTIST_ID) VALUES (?,?,?)',
               (title,findAlbumId(album),findArtistId(artist),))
    conn.commit()

def findSong():
    db.execute('SELECT * FROM songs')
    return db.fetchall()

createTables()
addSong('Hello', 'Adele', '25')
library = findSong()
for song in library:
    print '|' + str(song[0]) + '|' + str(song[1]) + '|' + str(song[2]) + '|' + str(song[3]) + '|'

