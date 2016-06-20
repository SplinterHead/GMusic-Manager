import DB
from flask import Flask
from flask import render_template

app = Flask(__name__)
use_debugger = True

@app.route('/')
def hello_world():
    return render_template('index.html',
                           song_count=DB.count('songs'),
                           artist_count=DB.count('artists'),
                           album_count=DB.count('albums')
                           )
