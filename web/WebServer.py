import DB
import GMusic
import ImageHandler
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)
use_debugger = True
app.jinja_env.globals.update(
    lookup_album=DB.lookupAlbum,
    lookup_albumart=DB.lookupAlbumArt,
    lookup_artist=DB.lookupArtist,
    lookup_artclass=ImageHandler.setAlbumArtClass,
    lookup_trackcount=DB.lookupAlbumTrackCount
)


@app.route('/')
def home():
    try:
        GMusic.load_database()
        return render_template(
            'index.html',
            art_display_size='200',
            song_count=DB.count('songs'),
            artist_count=DB.count('artists'),
            album_count=DB.count('albums'),
            all_songs=DB.allSongs()
        ), 200, {'Cache-Control': 'no-cache, no-store', 'Pragma': 'no-cache'}
    except:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if GMusic.login_check(request.form['username'], request.form['password']):
            print "Credentials check out"
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


def runFlask():
    Flask.run(app)
