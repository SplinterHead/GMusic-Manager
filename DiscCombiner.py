__author__ = 'Lewis England'

import re
import DB


def scan():
    multidisc_regex = ".*( )?[\[|\(]?(Dis(c|k)|CD)( )?[0-9]*[\]|\)]?"
    for album in DB.allData('albums'):
        match = re.search(multidisc_regex, album[1])
        #print match
