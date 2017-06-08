# PyGaze demo: simple gaze guided shooter
# version 2 (09-08-2013)
# E.S. Dalmaijer (edwin.dalmaijer@gmail.com)


## This file is part of the shooting game example for PyGaze
##
##    PyGaze is a Python module for easily creating gaze contingent experiments
##    or other software (as well as non-gaze contingent experiments/software)
##    Copyright (C) 2012-2013  Edwin S. Dalmaijer
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>
#

# MAIN
DUMMYMODE = True # False for gaze contingent display, True for dummy mode (using mouse or joystick)
print("Please type your name between quotes (e.g. 'player1') and press Enter")
print("(do not use more than 8 letters!)\n")
LOGFILENAME = input("Player name: ") # logfilename, without path
LOGFILE = LOGFILENAME[:] # .txt; adding path before logfilename is optional; logs responses (NOT eye movements, these are stored in an EDF file!)
TRIALS = 1

# DISPLAY
SCREENNR = 0 # number of the screen used for displaying experiment
DISPTYPE = 'psychopy' # either 'psychopy' or 'pygame'
DISPSIZE = (1024,768) # canvas size
MOUSEVISIBLE = False # mouse visibility
BGC = (125,125,125) # backgroundcolour
FGC = (0,0,0) # foregroundcolour
FONTSIZE = 32 # font size

# INPUT
KEYLIST = ['space', 'escape'] # None for all keys; list of keynames for keys of choice (e.g. ['space','9',':'] for space, 9 and ; keys)
KEYTIMEOUT = 1 # None for no timeout, or a value in milliseconds

# EYETRACKER
# general
TRACKERTYPE = 'eyelink' # either 'smi', 'eyelink' or 'dummy' (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
SACCVELTHRESH = 35 # degrees per second, saccade velocity threshold
SACCACCTHRESH = 9500 # degrees per second, saccade acceleration threshold
# EyeLink only
# SMI only
SMIIP = '127.0.0.1'
SMISENDPORT = 4444
SMIRECEIVEPORT = 5555

# STIMULUS
STIMSIZE = 100 # stimulus size (pixels)
STIMCOL = (255,255,0) # stimulus colour
STIMPOS = (DISPSIZE[0]/2,DISPSIZE[1]/2) # start position
STIMREFRESH = 2500 # ms; time before stimulus is set to new position

# GAME
PPH = 10 # points per hit
PPM = -30 # points per miss
GAMEDURATION = 30000 # ms

from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze.eyetracker import EyeTracker

import random

# # # # #
# prep

# create keyboard object
keyboard = Keyboard()

# display object
disp = Display()

# screen objects
screen = Screen()
blankscreen = Screen()
hitscreen = Screen()
hitscreen.clear(colour=(0,255,0))
misscreen = Screen()
misscreen.clear(colour=(255,0,0))

# create eyelink objecy
eyetracker = EyeTracker(disp)

# eyelink calibration
eyetracker.calibrate()

# display surface
disp.fill(screen=blankscreen)
disp.show()

# # # # #
# game

# run several rounds
for trialnr in range(0,TRIALS):
	
	# start eye tracking
	eyetracker.start_recording()
	eyetracker.log("start_trial %d" % trialnr)
	trialstart = libtime.get_time()

	# run game
	points = 0
	stimpos = STIMPOS
	t0 = libtime.get_time()
	tstim = libtime.get_time()
	while libtime.get_time() - t0 < GAMEDURATION:
		# get gaze position
		gazepos = eyetracker.sample()
		# get keypress
		key, presstime = keyboard.get_key()
		# handle input
		if key:
			if key == 'escape':
				break
			if ((gazepos[0]-stimpos[0])**2 + (gazepos[1]-stimpos[1])**2)**0.5 < STIMSIZE/2:
				screen.copy(hitscreen)
				points += PPH
			else:
				screen.copy(misscreen)
				points += PPM
		else:
			screen.copy(blankscreen)
		# draw stimulus
		screen.draw_circle(colour=STIMCOL, pos=stimpos, r=STIMSIZE/2, fill=True)
		# draw crosshair
		screen.draw_circle(colour=FGC, pos=gazepos, r=13, pw=2, fill=False)
		screen.draw_line(colour=FGC, spos=(gazepos[0]-15, gazepos[1]), epos=(gazepos[0]+15, gazepos[1]), pw=2)
		screen.draw_line(colour=FGC, spos=(gazepos[0], gazepos[1]-15), epos=(gazepos[0], gazepos[1]+15), pw=2)
		# draw point total
		screen.draw_text(text=str(points), colour=FGC, pos=(DISPSIZE[0]*0.9, DISPSIZE[1]*0.1), fontsize=FONTSIZE)
		# update display
		disp.fill(screen=screen)
		disp.show()
		# calculate new stimulus position
		if libtime.get_time() - tstim > STIMREFRESH:
			stimpos = (random.randint(int(DISPSIZE[0]*0.1),int(DISPSIZE[0]*0.9)), random.randint(int(DISPSIZE[1]*0.1),int(DISPSIZE[1]*0.9)))
			tstim = libtime.get_time()

	# stop eye tracking
	trialend = libtime.get_time()
	eyetracker.log("stop_trial %d" % trialnr)
	eyetracker.stop_recording()	


# # # # #
# end

# score display
screen.clear()
screen.draw_text(text="You have scored %d points!" % points, colour=FGC, pos=(DISPSIZE[0]/2, DISPSIZE[1]/2), fontsize=FONTSIZE)
disp.fill(screen=screen)
disp.show()

# wait for keypress
keyboard.get_key(keylist=None, timeout=None)

# highscore display
#scorestring = highscores.update(LOGFILENAME, points)
screen.clear()
#screen.draw_text(text=scorestring, colour=FGC, pos=(DISPSIZE[0]/2, DISPSIZE[1]/2), fontsize=FONTSIZE)
disp.fill(screen=screen)
disp.show()

# wait for keypress
keyboard.get_key(keylist=None, timeout=None)

# end connection to eye tracker
eyetracker.close()

# end timing and quit
libtime.expend()