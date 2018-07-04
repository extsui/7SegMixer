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

import spidev
import time
import sys

def reverse_bit_order(x):
	x_reversed = 0x00
	if (x & 0x80):
		x_reversed |= 0x01
	if (x & 0x40):
		x_reversed |= 0x02
	if (x & 0x20):
		x_reversed |= 0x04
	if (x & 0x10):
		x_reversed |= 0x08
	if (x & 0x08):
		x_reversed |= 0x10
	if (x & 0x04):
		x_reversed |= 0x20
	if (x & 0x02):
		x_reversed |= 0x40
	if (x & 0x01):
		x_reversed |= 0x80
	return x_reversed
	

spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 0
spi.max_speed_hz = 1000000	# 1MHz

xfer_data = map(reverse_bit_order, xfer_data)


