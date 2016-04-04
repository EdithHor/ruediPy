# Python script for testing the ruediPy code
# 
#
# Copyright 2016, Matthias Brennwald (brennmat@gmail.com) and Yama Tomonaga
# 
# This file is part of ruediPy, a toolbox for operation of RUEDI mass spectrometer systems.
# 
# ruediPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ruediPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ruediPy.  If not, see <http://www.gnu.org/licenses/>.
# 
# ruediPy: toolbox for operation of RUEDI mass spectrometer systems
# Copyright (C) 2016  Matthias Brennwald
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# make shure Python knows where to look for the RUEDI Python code
# http://stackoverflow.com/questions/4580101/python-add-pythonpath-during-command-line-module-run
# Example (bash): export PYTHONPATH=~/ruedi/python

from classes.rgams		import rgams
from classes.selectorvalve	import selectorvalve
from classes.datafile	import datafile
from classes.plots	import plots

import time
from datetime import datetime


# initialize instrument objects:
#MS    = rgams('/dev/serial/by-id/pci-WuT_USB_Cable_2_WT2304837-if00-port0','RGA-MS')
#VALVE = selectorvalve('/dev/serial/by-id/pci-WuT_USB_Cable_2_WT2350938-if00-port0','INLETSELECTOR')

MS    = rgams('/dev/serial/by-id/pci-WuT_USB_Cable_2_WT2016234-if00-port0','MS_MINIRUEDI1')
VALVE = selectorvalve('/dev/serial/by-id/pci-WuT_USB_Cable_2_WT2304832-if00-port0','INLETSELECTOR')

DATAFILE  = datafile('~/ruedi_data') 						# init object for data files
DATAFILE.next() # start a new data file

PLOTS = plots(); # PLOTS object

# change valve positions:
VALVE.setpos(1,DATAFILE)
print 'Valve position is ' + str(VALVE.getpos())
VALVE.setpos(2,DATAFILE)
print 'Valve position is ' + str(VALVE.getpos())
VALVE.setpos(3,DATAFILE)
print 'Valve position is ' + str(VALVE.getpos())

# print some MS information:
print 'MS has electron multiplier: ' + MS.hasMultiplier()
print 'MS max m/z range: ' + MS.mzMax()

# change MS configuraton:
MS.setElectronEnergy(60)
print 'Ionizer electron energy: ' + MS.getElectronEnergy() + ' eV'
print 'Set ion beam to Faraday detector...'
MS.setDetector('F')
print MS.getDetector()
MS.filamentOn() # turn on with default current
print 'Filament current: ' + MS.getFilamentCurrent() + ' mA'

print 'Data output to ' + DATAFILE.name()


# get scan data:
print 'Scanning... '
MS.setGateTime(0.3) # set gate time for each reading
mz,intens,unit = MS.scan(38,42,15,0.5,DATAFILE,PLOTS)
print '...done.'

print 'Close plot window to continue...'
# plt.ion() # turn on interactive mode (so Python does not stop until plot window is closed)
# plt.show()

print 'Single mass measurements at mz = 32, 36, and 40...'
k = 0
while k < 30:
	peak,unit = MS.peak(32,0.1,DATAFILE,PLOTS)
	peak,unit = MS.peak(36,0.1,DATAFILE,PLOTS)
	peak,unit = MS.peak(40,0.1,DATAFILE,PLOTS)
	k = k + 1
	### print str(k) + ' mz = 40 peak: ' + str(peak) + ' ' + unit
print '...done.'

# turn off filament:
MS.filamentOff()
print 'Filament current: ' + MS.getFilamentCurrent() + ' mA'

print '...done.'

print 'Waiting a while before exiting...'
time.sleep(20)
