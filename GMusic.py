__author__ = 'Lewis England'

# Libraries
import os
import json
import shutil
import urllib2
import gmusicapi

# Local Libraries
import DataFarmer
api = gmusicapi.Mobileclient()


def login_check(user, passw):
    api.login(user, passw, gmusicapi.Mobileclient().FROM_MAC_ADDRESS)
    if api.is_authenticated():
        return True
    else:
        return False


def load_database():
    songs = api.get_all_songs()
    for song in songs:
        DataFarmer.load(song)
    api.logout()

# Step 1: Delete the previous covers folder to create a new one
if os.path.exists('covers'):
    shutil.rmtree('covers')
os.mkdir('covers')

# Step 2a: Log into GMusic - only when internet connected
#if internet_on():
#api = gmusicapi.Mobileclient()
#api.login(username, password, gmusicapi.Mobileclient.FROM_MAC_ADDRESS)

    ## Will have to edit the gmusicapi to allow metadata changing for all keys
    #song = api.get_track_info(< some song['nid'] >)
    #song['rating'] = '1' # Set to thumbs down
    #api.change_song_metadata(song)

    ## Collect list of songs with all the metadata
#print "Downloading song library"
#songs = api.get_all_songs()

#cacheFile = open('library.json', 'w')
#cacheFile.write(str(songs))
#cacheFile.close()

# Step 2b: Read the backup file created last time there was internet
#    print "Reading library cache file"
#    cacheFile = open('library.json')
#    songs = json.loads(cacheFile.read())
#    cacheFile.close()

#print "done"

## Load all songs into the manager database
#print "Storing song data in database"
#for song in songs:
#    DataFarmer.load(song)
#print "complete"

## Log out of the MobileClient API
#api.logout()

#print "Writing report"
#webServer.runFlask()
