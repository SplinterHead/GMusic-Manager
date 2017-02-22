import DB
import GMusic
import ImageHandler
import DiscCombiner
from flask import Flask, render_template, redirect, url_for, request


def formatted_time(ms):
    x = ms / 1000
    seconds = x % 60
    x /= 60
    minutes = x % 60
    x /= 60
    hours = x % 24
    if hours == 0:
        return str(minutes) + ':' + str(seconds).zfill(2)
    else:
        return str(hours) + ':' + str(minutes) + ':' + str(seconds).zfill(2)

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
        if not DB.isLoaded():
            GMusic.load_database()
        return render_template(
            'albums.html',
            art_display_size='200',
            all_albums=DB.allData('albums')
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


@app.route('/songs')
def songs():
    if DB.isLoaded():
        return render_template(
            'songs.html',
            art_display_size=200,
            all_songs=DB.allData('songs')
        ), 200, {'Cache-Control': 'no-cache, no-store', 'Pragma': 'no-cache'}
    else:
        return redirect(url_for('home'))


@app.route('/artists')
def artists():
    if DB.isLoaded():
        return render_template(
            'artists.html',
            artist_width=512,
            artist_height=256,
            all_artists=DB.allData('artists')
        ), 200, {'Cache-Control': 'no-cache, no-store', 'Pragma': 'no-cache'}
    else:
        return redirect(url_for('home'))


@app.route('/info/artist')
def artist_info():
    artist_id = request.args['id']
    try:
        artist_data = DB.fetchDataById('artists', artist_id)
        #artist_albums = DB.getAlbums(artist_id)
        return render_template(
            'artist_info.html',
            artist_id=artist_id,
            artist_data=artist_data,
            all_albums_by_artist=DB.fetchArtistAlbums(artist_id)
        ), 200, {'Cache-Control': 'no-cache, no-store', 'Pragma': 'no-cache'}
    except:
        error = "Woops. No artist with that ID found in the database"
        return render_template('login.html', error=error)


@app.route('/info/album')
def album_info():
    album_id = request.args['id']
    try:
        album_data = DB.fetchDataById('albums', album_id)
        return render_template(
            'album_info.html',
            album_id=album_id,
            album_data=album_data,
            tracklist=DB.fetchAlbumTracklist(album_id)
        ), 200, {'Cache-Control': 'no-cache, no-store', 'Pragma': 'no-cache'}
    except:
        error = "Woops. No album with that ID found in the database"
        return render_template('login.html', error=error)


@app.route('/info/song')
def song_info():
    song_id = request.args['id']
    try:
        song_data = DB.fetchDataById('songs', song_id)
        return render_template(
            'song_info.html',
            song_id=song_data[0],
            song_track=song_data[2],
            song_title=song_data[3],
            album_id=song_data[4],
            artist_id=song_data[5],
            song_duration=formatted_time(song_data[6]),
            song_size=song_data[7]
        )
    except:
        error = "Woops. No song with that ID found in the database"
        return render_template('login.html', error=error)


def runFlask():
    Flask.run(app)
