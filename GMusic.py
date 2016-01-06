__author__ = 'Lewis England'

# Libraries
import os
import json
import shutil
import gmusicapi
# Local Libraries
import DB
import GImageSearcher

# Step 1: Log into GMusic
api = gmusicapi.Mobileclient()
api.login('xxxxxxxxx@gmail.com', 'password', gmusicapi.Mobileclient.FROM_MAC_ADDRESS)

# Step 2: Delete the previous covers folder to create a new one
if os.path.exists('covers'):
    shutil.rmtree('covers')
os.mkdir('covers')

# Step 3: Load the song data into the sqlite DB
## Have to use a list of songs and narrow it down from there

## Collect list of songs with all the metadata
songs = api.get_all_songs()

#################
Fancy DB stuff here
#################