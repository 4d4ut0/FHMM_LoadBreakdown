#!/usr/bin/python

'''
by shivam chudasama - may 2013
This program reads data coming from the serial port and saves that data to a text file. It expects data in the format:
"photocell_reading,thermistor_reading"

It assumes that the Arduino shows up in /dev/ttyACM0 on the Raspberry Pi which should happen if you're using Debian.
'''

import serial

ser = serial.Serial('COM6', 9600)
try:
    while 1:
        line = ser.readline().rstrip()
        temp2 = line
        print(temp2.decode('utf-8'))
        temp3 = temp2.decode('utf-8')
        temp4 = str(temp3)
        print(temp4)

        f_total = open('mains1.dat', 'a')
        tempo_1 = temp4[:-49]
        potativaM = temp4[:-23]
        stringM = "%s" % potativaM
        f_total.write(" %s\n" % stringM)
        f_total.close()

        '''
        f_chn1 = open('channel_11.dat', 'a')
        potativaT = temp4[:-41]
        stringT = " %s" % potativaT
        f_chn1.write(" %s\n" % stringT)
        f_chn1.close()

        f_chn2 = open('channel_22.dat', 'a')
        potativa1 = temp4[41:-11]
        string1 = "%s" % tempo_1 + " %s" % potativa1
        f_chn2.write(" %s\n" % string1)
        f_chn2.close()

        f_chn2 = open('channel_33.dat', 'a')
        potativa2 = temp4[51:]
        string2 = "%s" % tempo_1 + " %s" % potativa2
        f_chn2.write(" %s\n" % string2)
        f_chn2.close()
'''

except KeyboardInterrupt:
    print("done")
