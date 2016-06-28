import DB
from flask import Flask, render_template


app = Flask(__name__)
use_debugger = True
app.jinja_env.globals.update(lookup_album=DB.lookupAlbum)


@app.route('/')
def generateIndex():
    return render_template('index.html',
                           song_count=DB.count('songs'),
                           artist_count=DB.count('artists'),
                           album_count=DB.count('albums'),
                           all_songs=DB.allSongs()
                           )


def runFlask():
    Flask.run(app)
