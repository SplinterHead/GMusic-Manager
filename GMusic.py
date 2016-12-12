__author__ = 'Lewis England'

# Libraries
import os
import json
import shutil
import socket
import gmusicapi
import os.path

# Local Libraries
import DataFarmer
api = gmusicapi.Mobileclient()

# Local vars
REMOTE_SERVER = "www.google.com"
CACHE_FILE = '.gmusiccache'
OFFLINE_MODE = False


def set_offline_mode(mode):
    global OFFLINE_MODE
    OFFLINE_MODE = mode


def in_offline_mode():
    global OFFLINE_MODE
    return OFFLINE_MODE


def internet_connection():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def login_check(user, passw):
    if internet_connection():
        api.login(user, passw, gmusicapi.Mobileclient().FROM_MAC_ADDRESS)
        if api.is_authenticated():
            return True
        else:
            return False
    else:
        return True


def load_database():
    if internet_connection() and not in_offline_mode():
        songs = api.get_all_songs()
        if os.path.isfile(CACHE_FILE):
            os.remove(CACHE_FILE)
        cachefile = open(CACHE_FILE, 'w')
        cache_content = json.dumps(songs).encode('utf-8')
        cachefile.write(cache_content)
        cachefile.close()
        api.logout()
    else:
        ## In the case of no internet, we'll load the .cachefile
        cachefile = open(CACHE_FILE, 'r')
        cache_content = cachefile.read()
        songs = json.loads(cache_content)
        cachefile.close()
    for song in songs:
        DataFarmer.load(song)

if os.path.exists('covers'):
    shutil.rmtree('covers')
os.mkdir('covers')