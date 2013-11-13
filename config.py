# Device options 
#  (These will be automatically be set to 'False' if unavailable)
USE_INTERNET = True		# Download map/place data via internet connection
USE_GPS = False 		# Use GPS module, accessed via GPSD daemon
USE_SOUND = False		# Play sounds via RasPi's current sound-source
USE_CAMERA = False		# Use RasPi camera-module as V.A.T.S
USE_SERIAL = False		# Communicate with custom serial-port controller

QUICKLOAD = True		# If true, commandline-startup bits aren't rendered
FORCE_DOWNLOAD = False	# Don't use cached map-data, if online

# Render screen-objects at this size - smaller is faster
WIDTH = 320
HEIGHT = 240

# Address for map's default position: 
defaultPlace = "Washington DC"

# Player data:
PLAYERNAME = 'Niil'
PLAYERLEVEL = 33

FPS = 15

import pygame, os

# My Google-API key:
# (this is limited to only 2000 location requests a day, 
#    so please don't use this key if you're making your own project!)
gKey = 'AIzaSyB4umXdIUQX7Wu7rT_c4RdYLCKxfYKq5K0'


# Teensy USB serial: symbolic link set up by creating: 
#   /etc/udev/rules.d/99-usb-serial.rules
# With line:
#   SUBSYSTEM=="tty", ATTRS{manufacturer}=="Teensyduino", SYMLINK+="teensy"
SERIALPORT = '/dev/teensy'
# Pi GPIO serial:
#SERIALPORT = '/dev/ttyAMA0'


if USE_CAMERA:
	# Is there a camera module connected?
	def hasCamera():
		try:
			import picamera
			camera = picamera.PiCamera()
			camera.close()
			return True
		except:
			return False
	
	USE_CAMERA = hasCamera()
print ("CAMERA: %s" %(USE_CAMERA))

# Downloaded/auto-generated data will be put here:
CACHEPATH = 'cache'
if not os.path.exists(CACHEPATH):
	os.makedirs(CACHEPATH)

DRAWCOLOUR = pygame.Color (255, 255, 255)
TINTCOLOUR = pygame.Color (33, 255, 156)
SELBOXGREY = 50

EVENTS = {
	'SONG_END': pygame.USEREVENT + 1
}

print "Loading images..."
IMAGES = {
	"background":pygame.image.load('images/pipboy_back.png'),
	"scanline":pygame.image.load('images/pipboyscanlines.png'),
	"distort":pygame.image.load('images/pipboydistorteffectmap.png'),
	"statusboy":pygame.image.load('images/pipboy_statusboy.png'),
}

print "(done)"

# Test internet connection:
if USE_INTERNET:
	import urllib2
	
	def internet_on():
		try:
			# Can we access this Google address?
			response=urllib2.urlopen('http://74.125.228.100',timeout=1)
			return True
		except urllib2.URLError as err: pass
		return False
	
	USE_INTERNET = internet_on()
print ("INTERNET: %s" %(USE_INTERNET))

# Test and set up sounds::
MINHUMVOL = 0.7
MAXHUMVOL = 1.0
if USE_SOUND:
	try:
		print "Loading sounds..."
		pygame.mixer.init(44100, -16, 2, 2048)

		SOUNDS = {
			"start":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_up.wav'),
			"end":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_access_down.wav'),
			"hum":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_hum_lp.wav'),
			"scroll":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_scroll.wav'),
			"changetab":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_tab.wav'),
			"changemode":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_mode.wav'),
			"static":		pygame.mixer.Sound('sounds/radio/ui_radio_static_lp.wav'),
			"tapestart":	pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_start.wav'),
			"tapestop":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_holotape_stop.wav'),
			"lighton":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_on.wav'),
			"lightoff":		pygame.mixer.Sound('sounds/pipboy/ui_pipboy_light_off.wav'),
			"beacon":		pygame.mixer.Sound('sounds/radio/beacon/ui_radio_beacon_header.wav'),
			"camerastart":	pygame.mixer.Sound('sounds/vats/ui_vats_enter.wav'),
			#"cameraexit":	pygame.mixer.Sound('sounds/vats/ui_vats_exit.wav'),
		}
		SOUNDS["hum"].set_volume(MINHUMVOL)
		print "(done)"
	except:
		USE_SOUND = False
print ("SOUND: %s" %(USE_SOUND))

# Set up fonts:
pygame.font.init()
kernedFontName = 'fonts/monofonto-kerned.ttf'
monoFontName = 'fonts/monofonto.ttf'

# Scale font-sizes to chosen resolution:
FONT_SML = pygame.font.Font(kernedFontName, int (HEIGHT * (12.0 / 360)))
FONT_MED = pygame.font.Font(kernedFontName, int (HEIGHT * (16.0 / 360.0)))
FONT_LRG = pygame.font.Font(kernedFontName, int (HEIGHT * (18.0 / 360.0)))
MONOFONT = pygame.font.Font(monoFontName, int (HEIGHT * (16.0 / 360.0)))

# Find monofont's character-size:
tempImg = MONOFONT.render("X", True, DRAWCOLOUR, (0, 0, 0))
charHeight = tempImg.get_height()
charWidth = tempImg.get_width()
del tempImg