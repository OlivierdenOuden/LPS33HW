#*******************************************************#
#														                            #
#		LPS33HW - ST Electronics Pressure sensor	        	#
#													                            	#
#		Simple Read-out script.			                				#
#												                            		#
#		Olivier den Ouden			                    					#
#		Royal Netherlands Meterological Institute		        #
#		RD Seismology and Acoustics				              		#
#		https://www.seabirdsound.org 			              		#
#												                            		#
#*******************************************************#

# Modules
import smbus
import time
import numpy as np

bus = smbus.SMBus(1)

#LPS33HW hex-adres
LPS33HW_ADDR             = 0x5C
LPS33HW_CHECK            = 0x0F
LPS33HW_CTRL_REG_1       = 0x10
LPS33HW_P_OUT_XL         = 0x28
LPS33HW_P_OUT_L          = 0x29
LPS33HW_P_OUT_H          = 0x2A
LPS33HW_T_OUT_L          = 0x2B
LPS33HW_T_OUT_H          = 0x2C

# MS to SL
bus.write_byte_data(LPS33HW_ADDR,LPS33HW_CTRL_REG_1,0b01011110)

# Read Pressure
p_out_xl = bus.read_byte_data(LPS33HW_ADDR,LPS33HW_P_OUT_XL)
p_out_l  = bus.read_byte_data(LPS33HW_ADDR,LPS33HW_P_OUT_L)
p_out_h  = bus.read_byte_data(LPS33HW_ADDR,LPS33HW_P_OUT_H)

p = [p_out_h, p_out_l, p_out_xl]
p_data = p[0] << 16 | p[1] << 8 | p[2]
Pressure = np.float(p_data)/4096.0

# Read Temperature
t_out_l  = bus.read_byte_data(LPS33HW_ADDR,LPS33HW_T_OUT_L)
t_out_h  = bus.read_byte_data(LPS33HW_ADDR,LPS33HW_T_OUT_H)

t = [t_out_h, t_out_l]
t_data = t[0] << 8 | t[1]
Temperature = np.float(t_data)/100.0

# Print Values
print("Temp: %0.2f C  P: %0.2f hPa ") % (Temperature,Pressure)
