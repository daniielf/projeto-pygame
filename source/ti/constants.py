# Main
DUMMYMODE = True
LOGFILENAME = 'logs'
LOGFILE = LOGFILENAME[:]

# Display
SCREENNR = 0
DISPTYPE = 'pygame'
DISPSIZE = (1366, 768)
SCREENSIZE = (36.3, 23.8)
BGC = (255, 255, 255)
FGC = (0, 0, 0)
FULLSCREEN = True


# Sound
SOUNDOSCILLATOR = 'sine'
SOUNDFREQUENCY = 440
SOUNDLENGTH = 100
SOUNDATTACK = 0
SOUNDDECAY = 5
SOUNDBUFFERSIZE = 1024
SOUNDSAMPLINGFREQUENCY = 48000
SOUNDSAMPLESIZE = -16
SOUNDCHANNELS = 2

# Input
MOUSEBUTTONLIST = None
MOUSETIMEOUT = None
KEYLIST = ['space']
KEYTIMEOUT = None
JOYBUTTONLIST = None
JOYTIMEOUT = None

# FRL
FRLSIZE = 200
FRLDIST = 125
FRLTYPE = 'gauss'
FRLPOS = 'center'

# CURSOR
CURSORTYPE = 'cross'
CURSORSIZE = 20
CURSORCOLOUR = 'pink'
CURSORFILL = True
CURSORPENWIDTH = 3

# EyeTracker
TRACKERTYPE = 'smi'
SACCVELTHRESH = 35
SACCACCTHRESH = 9500
BLINKTHRESH = 150
EVENTDETECTION = 'native'

# SMI
SMIIP = '127.0.0.1'
SMISENDPORT = 4444
SMIRECEIVEPORT = 5555