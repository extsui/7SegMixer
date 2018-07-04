# -*- coding: utf-8 -*-

from __future__ import print_function

def display(d):
    print('#0', end='')
    for y in range(4):
        print('01', end='')
        for x in range(8):
            print('%02x' % d, end='')
    print('')

def brightness(b):
    print('#0', end='')
    for y in range(4):
        print('02', end='')
        for x in range(8):
            print('%02x' % b, end='')
    print('')

# 2次元配列[8][24]
panel = [[0 for x in range(24)] for y in range(8)]

# 2次元配列から7SegArmorの実配列への変換
def to_real_panel(panel):

	"""
	  <armor0>        <armor1>         <armor2>
	panel[0][0:8]   panel[0][8:16]   panel[0][16:24]
	panel[1][0:8]   panel[1][8:16]   panel[1][16:24]
	panel[2][0:8]   panel[2][8:16]   panel[2][16:24]
	panel[3][0:8]   panel[3][8:16]   panel[3][16:24]

	  <armor3>        <armor4>         <armor5>
	panel[4][0:8]   panel[4][8:16]   panel[4][16:24]
	panel[5][0:8]   panel[5][8:16]   panel[5][16:24]
	panel[6][0:8]   panel[6][8:16]   panel[6][16:24]
	panel[7][0:8]   panel[7][8:16]   panel[7][16:24]
	"""

	real_panel = [
		[
			panel[0][0:8],
			panel[1][0:8],
			panel[2][0:8],
			panel[3][0:8],
		],
		[
			panel[0][8:16],
			panel[1][8:16],
			panel[2][8:16],
			panel[3][8:16],
		],
		[
			panel[0][16:24],
			panel[1][16:24],
			panel[2][16:24],
			panel[3][16:24],
		],
		[
			panel[4][0:8],
			panel[5][0:8],
			panel[6][0:8],
			panel[7][0:8],
		],
		[
			panel[4][8:16],
			panel[5][8:16],
			panel[6][8:16],
			panel[7][8:16],
		],
		[
			panel[4][16:24],
			panel[5][16:24],
			panel[6][16:24],
			panel[7][16:24],
		],
	]
	
	return real_panel

# 7SegArmorの実配列からコマンドへの変換
def to_armor_command(real_panel):
	command = ''

	# コマンドはArmor5-->4-->...-->0の順に送信する必要がある

	#for armor in range(5, -1, -1):
	for armor in range(6):
		command += '#0'
		for y in range(4):
			command += '01'
			for x in range(8):
				command += ('%02x' % real_panel[armor][y][x])
		command += '\n'
	return command

# パネルからコマンドへの変換
def panel_to_command(panel):
	real_panel = to_real_panel(panel)
	command = to_armor_command(real_panel)
	command += '#1\n'
	return command

"""
for y in range(8):
	for x in range(24):
		panel[y][x] = 0xFF
		print(panel_to_command(panel))
"""

import serial
import time
import sys

f = open('a.txt', 'r')
ser = serial.Serial('COM46', 115200)

line_count = 0

start_time = time.time()

while True:
	
	line = f.readline()
	
	if not line:
		print('')
		break
	
	ser.write(line)
	
	if (line_count % 7 == 6):
		time.sleep(0.015)
		pass
	else:
		time.sleep(0.010)
		pass
	
	
	#print(line)
	sys.stderr.write('%d\r\r\r' % (line_count / 7))
	line_count += 1

elapsed_time = time.time() - start_time
print('%d [s]' % elapsed_time)
print('fps = %.1f' % ((line_count / 7.0) / elapsed_time))

ser.close()
