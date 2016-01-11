__author__ = 'Lewis England'

# Libraries
import os
import shutil
import gmusicapi
# Local Libraries
import DB
import DataFarmer
import web.WebServer as webServer

# Step 1: Log into GMusic
api = gmusicapi.Mobileclient()
api.login('xxxxx@gmail.com', '**********', gmusicapi.Mobileclient.FROM_MAC_ADDRESS)

# Step 2: Delete the previous covers folder to create a new one
if os.path.exists('covers'):
    shutil.rmtree('covers')
os.mkdir('covers')

# Step 3: Load the song data into the sqlite DB
## Collect list of songs with all the metadata
print "Downloading song library"
songs = api.get_all_songs()
print "done"

## Load all songs into the manager database
print "Storing song data in database"
for song in songs:
    DataFarmer.load(song)
print "complete"

print "Writing report"
webServer.generateReport()