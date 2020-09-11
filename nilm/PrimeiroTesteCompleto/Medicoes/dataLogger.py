#!/usr/bin/python

'''
by shivam chudasama - may 2013 
This program reads data coming from the serial port and saves that data to a text file. It expects data in the format:
"photocell_reading,thermistor_reading"

It assumes that the Arduino shows up in /dev/ttyACM0 on the Raspberry Pi which should happen if you're using Debian.
'''


import serial
ser = serial.Serial('COM11', 9600)
try:
	while 1:
		line = ser.readline().rstrip()
		temp2 = line
		print(temp2.decode('utf-8'))
		temp3 = temp2.decode('utf-8')
		temp4 = str(temp3)
		print(temp4)

		f_total = open('tempLog_total1.dat', 'a')
		#print(f, temp2)
		f_total.write("%s\n" % str(temp3))
		f_total.close()

		f_chn1 = open('channel_1.dat', 'a')
		# print(f, temp2)
		tempo_1= str(temp3)[:-19]
		potativa= str(temp3)[11:-13]
		string= "%s" %tempo_1 + " %s" %potativa
		f_chn1.write(" %s\n" %string)
		f_chn1.close()




except KeyboardInterrupt:
	print("done")
