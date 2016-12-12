import urllib
from PIL import Image


def getDimensions(image):
    urllib.urlretrieve(image, 'tempimage')
    im = Image.open('tempimage')
    return im.size  # (width,height) tuple
#    imageFile = urllib.urlopen(image)
#    size = imageFile.headers.get("content-length")
#    if size: size = int(size)
#    p = ImageFile.Parser()
#    while 1:
#        data = imageFile.read(1024)
#        if not data:
#            break
#        p.feed(data)
#        if p.image:
#            return size, p.image.size
#    imageFile.close()
#    return size, None


def setAlbumArtClass(image):
    if image != 'NULL':
        artSize = getDimensions(image)
        ALBUM_ART_W = artSize[0]
        ALBUM_ART_H = artSize[1]
        if ALBUM_ART_H != ALBUM_ART_W:
            artClass = 'irregular_dimensions'
        elif ALBUM_ART_W < 200:
            artClass = 'low_quality'
        elif ALBUM_ART_W < 500:
            artClass = 'med_quality'
        else:
            artClass = 'hi_quality'
        return artClass