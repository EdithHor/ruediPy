# Code for the VICI selector valve class

import serial
import time
from classes.misc	import misc

class selectorvalve:

	
	########################################################################################################
	

	def __init__(self,label,P):
		'''
		Initialize SELECTORVALVE object (VICI valve), configure serial port connection
		
		INPUT:
		label: label / name of the SELECTORVALVE object (string)
		P: device name of the serial port, e.g. P = '/dev/ttyUSB3'
		
		OUTPUT:
		(none)
		'''
	
		# open and configure serial port for communication with VICI valve (9600 baud, 8 data bits, no parity, 1 stop bit
		ser = serial.Serial(
			port     = P,
			baudrate = 9600,
			parity   = serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS,
			timeout  = 5.0
		)
		ser.flushInput() 	# make sure input is empty
		ser.flushOutput() 	# make sure output is empty
		
		self.ser = ser;

		self._label = label

	
	########################################################################################################
	

	def label(self):
		"""
		Return label / name of the SELECTORVALVE object
		
		INPUT:
		(none)
		
		OUTPUT:
		label: label / name (string)
		"""
		
		return self._label

	
	

	def warning(self,msg):
		# warn about issues related to operation of the valve
		# msg: warning message
		misc.warnmessage ('VICI VALVE',msg)

	
	########################################################################################################
	

	def setpos(self,val,f):
		''' Set valve position

		INPUT:
		val: new valve position (integer)
		f: datafile object for writing data (see datafile.py). If f = 'nofile', data is not written to any data file.

		OUTPUT:
		(none)
		'''
		
		val = int(val)
		curpos = self.getpos()
		if not curpos == val: # check if valve is already at desired position
			# send command to serial port:
			self.ser.write('GO' + str(val) + '\r\n')
		
		# write to datafile
		if not f == 'nofile':
			f.writeValvePos(self.label(),val,misc.nowUNIX())

	
	########################################################################################################
	

	def getpos(self):
		# get valve position
		
		# make sure serial port buffer is empty:
		self.ser.flushInput() 	# make sure input is empty
		self.ser.flushOutput() 	# make sure output is empty

		# send command to serial port:
		self.ser.write('CP\r\n')
		
		# wait for response
		t = 0
		dt = 0.1
		doWait = 1
		while doWait:
			if self.ser.inWaiting() == 0: # wait
				time.sleep(dt)
				t = t + dt
				if t > 5: # give up waiting
					doWait = 0
					self.warning('could not determine valve position (no response from valve)')
					ans = '-1'
			else:
				doWait = 0
				ans = ''
		
		# read back result:
		if (ans != '-1'):
			while self.ser.inWaiting() > 0: # while there's something in the buffer...
				ans = ans + self.ser.read() # read each byte
	    	ans = ans.split('=')[1] # split answer in the form 'Position is  = 1'
	    	ans = ans.strip() # strip away whitespace
	    	
	    # check result:
		if not ans.isdigit():
			self.warning('could not determine valve position (position = ' + ans + ')')
			ans = '-1'

		# return the result:
		return int(ans)
