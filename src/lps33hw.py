#*****************************************************************************#
#														
#		LPS33HW - ST Electronics Pressure sensor		
#														
#		Read-out script.								
#													
#		Olivier den Ouden								
#		Royal Netherlands Meterological Institute		
#		RD Seismology and Acoustics						
#		https://www.seabirdsound.org 					
#														
#*******************************************************************************#

# Modules
import lps33hw_main
import time
from datetime import datetime
import numpy as np 
import argparse
from argparse import RawTextHelpFormatter

print('')
print('LPS33HW ST Electronics Pressure sensor Read-out')
print('')
print('Olivier den Ouden')
print('Royal Netherlands Meteorological Institute, KNMI')
print('Dec. 2018')
print('')

# Parser arguments
parser = argparse.ArgumentParser(prog='LPS33HW ST Electronics Pressure sensor Read-out',
    description=('Read-out of the LPS33HW ST Electronics Pressure sensor\n'
    ), formatter_class=RawTextHelpFormatter
)

parser.add_argument(
    '-t', action='store', default=100, type=float,
    help='Time of recording, [sec].\n', metavar='-time')

parser.add_argument(
    '-fs', action='store', default=1, type=float,
    help='Sample rate, [Hz].\n', metavar='-SamplFreq')

args = parser.parse_args()

# Check if MS can comunicate with SL
if lps33hw_main.init() == False:
	print "Sensor LPS33HW could not be initialized"
	exit(1)
else:
	print "Sensor LPS33HW initialized"

# Time knowledge
st = datetime.utcnow()
fs = args.fs
record_t = args.t
n_samples = record_t*fs

# Save data
Time_array = np.linspace(0,record_t,n_samples)
Temp = np.zeros((n_samples,2))
Pres = np.zeros((n_samples,2))
Temp[:,0] = Time_array[:]
Pres[:,0] = Time_array[:]

# Loop 
i = 0
while i < n_samples:
	t_data,p_data = lps33hw_main.read()
	Temp[i,1] = t_data
	Pres[i,1] = p_data
	i = i+1

	# Print converted data
	read_Temp = lps33hw_main.temperature(t_data)
	read_Pres = lps33hw_main.pressure(p_data)
	print("Temp: %0.2f C  P: %0.2f hPa ") % (read_Temp,read_Pres)

	# Sampling rate
	time.sleep(1/fs)
