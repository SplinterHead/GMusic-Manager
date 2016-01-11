__author__ = 'Lewis England'

import DB

def load(song):
    # Available metadata:
# 'comment': '',
# 'rating': '0',
# 'albumArtRef': [
    # {'url': 'http://lh3.googleusercontent.com/p8U1RGRxD0ALYDIQn7i5FnQeqHRgwdK-nkfSZz8ZBlFoRlGELXyCnHlFNMu-pcE07N4RnzEJ'}
# ],
# 'artistId': ['Axoinbuvsvwmwg6ivw7zh4wrdgu'],
# 'composer': '',
# 'year': 2010,
# 'creationTimestamp': '1359063177192221',
# 'id': '818adcf0-8f46-34cd-bf06-15fae192537c',
# 'album': 'We Speak No Americano',
# 'totalDiscCount': 0,
# 'title': 'We No Speak Americano',
# 'recentTimestamp': '1377030153712000',
# 'albumArtist': 'Yolanda Be Cool',
# 'trackNumber': 1,
# 'discNumber': 0,
# 'deleted': False,
# 'storeId': 'Ta5h26qukyn6ak2vqbxhjwhlymu',
# 'nid': 'Ta5h26qukyn6ak2vqbxhjwhlymu',
# 'totalTrackCount': 0,
# 'estimatedSize': '27964108',
# 'albumId': 'Bndl5iegqwoofmnghpgn3scq4aa',
# 'beatsPerMinute': 0,
# 'genre': 'House',
# 'playCount': 1,
# 'artistArtRef': [
    # {'url': 'http://lh3.googleusercontent.com/1ENtGnKsVUBDUwC6SgVTpDCOQodlAjOadralURIVQ1kmc2UM-POSonmInfO8XR2OWmiafOic'}
# ],
# 'kind': 'sj#track',
# 'primaryVideo': {
    # 'kind': 'sj#video',
    # 'id': 'YKa0yM4ZisA',
    # 'thumbnails': [
    #   {'url': 'https://i.ytimg.com/vi/YKa0yM4ZisA/mqdefault.jpg',
    #    'width': 320,
    #    'height': 180}
    # ]
# },
# 'artist': 'DCUP/Yolanda Be Cool',
# 'lastModifiedTimestamp': '1452341253502000',
# 'clientId': 'KGuhQUzL9y/pYPgpeSNTxA',
# 'durationMillis': '270000'

    # Step 1: Add the artist / Find the artist in the DB and collect their ID
    songArtist = song['artist']
    songArtistId = song['artistId'][0]
    songArtistArt = song['artistArtRef'][0]
    artistPyId = DB.findArtistId(songArtist,songArtistId,songArtistArt)

    # Using this internal ID, assign the album (or find the current ID if already exists)
    songAlbum = song['album']
    songAlbumId = song['albumId'][0]
    songAlbumArt = song['albumArtRef'][0]
    albumPyId = DB.findAlbumId(songAlbum,artistPyId,songAlbumId,songAlbumArt)

    # Finally, add the song itself to the DB
    songTitle = song['title']
    songId = song['id']
    DB.addSong(songTitle,songId,artistPyId,albumPyId)

