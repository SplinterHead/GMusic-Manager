import DB
import ImageHandler
from flask import Flask, render_template


app = Flask(__name__)
use_debugger = True
app.jinja_env.globals.update(
    lookup_album=DB.lookupAlbum,
    lookup_albumart=DB.lookupAlbumArt,
    lookup_artist=DB.lookupArtist,
    lookup_artclass=ImageHandler.setAlbumArtClass
)


@app.route('/')
def generateIndex():
    return render_template(
        'index.html',
        art_display_size='200',
        song_count=DB.count('songs'),
        artist_count=DB.count('artists'),
        album_count=DB.count('albums'),
        all_songs=DB.allSongs()
    )


def runFlask():
    Flask.run(app)
