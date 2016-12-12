import GMusic
import web.WebServer as webServer

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-o", "--offline", action="store_true", dest="offline",
                  help="Runs in offline mode to use the cache file", default=False)
(options, args) = parser.parse_args()

GMusic.set_offline_mode(options.offline)

webServer.runFlask()