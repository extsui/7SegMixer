#!/usr/bin/python
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
def to_armor_command(real_panel, finger_cmd):
	command = []
	for armor in range(6):
		for y in range(4):
			command.append(finger_cmd)
			for x in range(8):
				command.append(real_panel[armor][y][x])
	return command

# パネルからコマンドへの変換
def panel_to_command(panel, finger_cmd):
	real_panel = to_real_panel(panel)
	command = to_armor_command(real_panel, finger_cmd)
	return command

import spidev
import time

# LATCHピンの指定
# GPIO26(37番ピン)を使用する。
import RPi.GPIO as GPIO

# ピン番号ではなく、機能名(例:GPIO26)で指定できるようにする。
GPIO.setmode(GPIO.BCM)

# 出力設定
GPIO.setup(26, GPIO.OUT)


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

start_time = time.time()


# 輝度を下げる
#brightness = 255//8
brightness = 255//3
panel = [[brightness for x in range(24)] for y in range(8)]
xfer_data = panel_to_command(panel, 0x02)
xfer_data = map(reverse_bit_order, xfer_data)

for i in range(6):
	spi.writebytes(xfer_data[i*36:(i+1)*36])
	time.sleep(0.001)
	
time.sleep(0.006)

# 表示更新(LATCH=＿|￣|＿)
GPIO.output(26, GPIO.HIGH)
GPIO.output(26, GPIO.LOW)

print('Brightness = %d' % brightness)


num_to_pattern = [
	0xfc, # 0
	0x60, # 1
	0xda, # 2
	0xf2, # 3
	0x66, # 4
	0xb6, # 5
	0xbe, # 6
	0xe4, # 7
	0xfe, # 8
	0xf6, # 9
]

import csv

#f = open('kemono_60fps_32768pt.csv', 'rb')
#f = open('kemono_original.csv', 'rb')
#f = open('kemono_4096pt_30fps.csv', 'rb')
#f = open('kemono_4096pt_60fps.csv', 'rb')
#f = open('mtank_4096pt_60fps.csv', 'rb')
#f = open('mtank_4096pt_30fps.csv', 'rb')
#f = open('mtank_4096pt_20fps.csv', 'rb')
#f = open('mtank_8192pt_20fps.csv', 'rb')
#f = open('mtank_8192pt_30fps.csv', 'rb')
#f = open('mtank_8192pt_60fps.csv', 'rb')
f = open('mtank_16384pt_60fps.csv', 'rb')
reader = csv.reader(f)
print('CSV: [OK]')

count = 0

for row in reader:
	
	count += 1
	
	
	#print(spec)
	#continue
	
	# そのまま出す場合
	#spec = map(lambda x: int(x), row)
	
	# 出力を加工する場合
	#spec = map(lambda x: (int)((int(x) + 1) * 1.6), row)
	#spec = map(lambda x: (int)((int(x) + 1) * 2.2), row)
	#spec = map(lambda x: (int)((int(x) * 1.0 / 3.5)), row)
	
	spec = map(lambda x: (int)((int(x) * 1.0 / 1.5)), row)
	
	panel = [[0 for x in range(24)] for y in range(8)]
	
	limit = 24
	
	# '&0xFE'とすると*を落とすことになる
	# mask = 0xFE
	mask = 0xFF
	
	LEVEL0 = 0x00 & mask
	LEVEL1 = 0x11 & mask
	LEVEL2 = 0x2B & mask
	LEVEL3 = 0xED & mask
	LEVEL4 = 0x6D & mask
	
	for x in range(limit):
		"""
		if (spec[x] == 0):
			panel[0][x] = 0x01
			panel[1][x] = 0x01
			panel[2][x] = 0x01
			panel[3][x] = 0x01
			panel[4][x] = 0x01
			panel[5][x] = 0x01
			panel[6][x] = 0x01
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 1):
			panel[0][x] = 0x01
			panel[1][x] = 0x01
			panel[2][x] = 0x01
			panel[3][x] = 0x01
			panel[4][x] = 0x01
			panel[5][x] = 0x01
			panel[6][x] = 0x01
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 2):
			panel[0][x] = 0x01
			panel[1][x] = 0x01
			panel[2][x] = 0x01
			panel[3][x] = 0x01
			panel[4][x] = 0x01
			panel[5][x] = 0x01
			panel[6][x] = num_to_pattern[1]
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 3):
			panel[0][x] = 0x01
			panel[1][x] = 0x01
			panel[2][x] = 0x01
			panel[3][x] = 0x01
			panel[4][x] = 0x01
			panel[5][x] = num_to_pattern[2]
			panel[6][x] = num_to_pattern[1]
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 4):
			panel[0][x] = 0x01
			panel[1][x] = 0x01
			panel[2][x] = 0x01
			panel[3][x] = 0x01
			panel[4][x] = num_to_pattern[3]
			panel[5][x] = num_to_pattern[2]
			panel[6][x] = num_to_pattern[1]
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 5):
			panel[0][x] = 0x01
			panel[1][x] = 0x01
			panel[2][x] = 0x01
			panel[3][x] = num_to_pattern[4]
			panel[4][x] = num_to_pattern[3]
			panel[5][x] = num_to_pattern[2]
			panel[6][x] = num_to_pattern[1]
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 6):
			panel[0][x] = 0x01
			panel[1][x] = 0x01
			panel[2][x] = num_to_pattern[5]
			panel[3][x] = num_to_pattern[4]
			panel[4][x] = num_to_pattern[3]
			panel[5][x] = num_to_pattern[2]
			panel[6][x] = num_to_pattern[1]
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 7):
			panel[0][x] = 0x01
			panel[1][x] = num_to_pattern[6]
			panel[2][x] = num_to_pattern[5]
			panel[3][x] = num_to_pattern[4]
			panel[4][x] = num_to_pattern[3]
			panel[5][x] = num_to_pattern[2]
			panel[6][x] = num_to_pattern[1]
			panel[7][x] = num_to_pattern[0]
		elif (spec[x] == 8):
			panel[0][x] = num_to_pattern[7]
			panel[1][x] = num_to_pattern[6]
			panel[2][x] = num_to_pattern[5]
			panel[3][x] = num_to_pattern[4]
			panel[4][x] = num_to_pattern[3]
			panel[5][x] = num_to_pattern[2]
			panel[6][x] = num_to_pattern[1]
			panel[7][x] = num_to_pattern[0]
		#elif (spec[x] == 9):
		else:
			panel[0][x] = num_to_pattern[8]
			panel[1][x] = num_to_pattern[8]
			panel[2][x] = num_to_pattern[8]
			panel[3][x] = num_to_pattern[8]
			panel[4][x] = num_to_pattern[8]
			panel[5][x] = num_to_pattern[8]
			panel[6][x] = num_to_pattern[8]
			panel[7][x] = num_to_pattern[8]
		elif (spec[x] == 10):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 11):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 12):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 13):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 14):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 15):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 16):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 17):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 18):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 19):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 20):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 21):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 22):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		elif (spec[x] == 23):
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		else:
			panel[0][x] = 0
			panel[1][x] = 0
			panel[2][x] = 0
			panel[3][x] = 0
			panel[4][x] = 0
			panel[5][x] = 0
			panel[6][x] = 0
			panel[7][x] = 0
		"""
		if (spec[x] == 0):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL0
			panel[6][x] = LEVEL0
			panel[7][x] = LEVEL0
		elif (spec[x] == 1):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL0
			panel[6][x] = LEVEL0
			panel[7][x] = LEVEL1
		elif (spec[x] == 2):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL0
			panel[6][x] = LEVEL0
			panel[7][x] = LEVEL2
		elif (spec[x] == 3):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL0
			panel[6][x] = LEVEL0
			panel[7][x] = LEVEL3
		elif (spec[x] == 4):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL0
			panel[6][x] = LEVEL1
			panel[7][x] = LEVEL4
		elif (spec[x] == 5):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL0
			panel[6][x] = LEVEL2
			panel[7][x] = LEVEL4
		elif (spec[x] == 6):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL0
			panel[6][x] = LEVEL3
			panel[7][x] = LEVEL4
		elif (spec[x] == 7):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL1
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 8):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL2
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 9):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL0
			panel[5][x] = LEVEL3
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 10):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL1
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 11):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL2
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 12):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL0
			panel[4][x] = LEVEL3
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 13):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL1
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 14):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL2
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 15):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL0
			panel[3][x] = LEVEL3
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 16):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL1
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 17):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL2
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 18):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL0
			panel[2][x] = LEVEL3
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 19):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL1
			panel[2][x] = LEVEL4
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 20):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL2
			panel[2][x] = LEVEL4
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 21):
			panel[0][x] = LEVEL0
			panel[1][x] = LEVEL3
			panel[2][x] = LEVEL4
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 22):
			panel[0][x] = LEVEL1
			panel[1][x] = LEVEL4
			panel[2][x] = LEVEL4
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		elif (spec[x] == 23):
			panel[0][x] = LEVEL2
			panel[1][x] = LEVEL3
			panel[2][x] = LEVEL4
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		else:
			panel[0][x] = LEVEL3
			panel[1][x] = LEVEL4
			panel[2][x] = LEVEL4
			panel[3][x] = LEVEL4
			panel[4][x] = LEVEL4
			panel[5][x] = LEVEL4
			panel[6][x] = LEVEL4
			panel[7][x] = LEVEL4
		
		if (spec[x] / 3 >= 9):
			bottom_num = 9
		else:
			bottom_num = (spec[x] / 3)
		panel[7][x] = num_to_pattern[bottom_num]
	
	
	panel[0][23] = num_to_pattern[count / 1 % 10]
	panel[0][22] = num_to_pattern[count / 10 % 10]
	panel[0][21] = num_to_pattern[count / 100 % 10]
	panel[0][20] = num_to_pattern[count / 1000 % 10]
	panel[0][19] = num_to_pattern[count / 10000 % 10]
	
	xfer_data = panel_to_command(panel, 0x01)
	xfer_data = map(reverse_bit_order, xfer_data)
	
	for i in range(6):
		spi.writebytes(xfer_data[i*36:(i+1)*36])
		#time.sleep(0.001)
		
	#time.sleep(0.015)
	time.sleep(0.005)	# 60fps
	#time.sleep(0.025)	# 30fps
	#time.sleep(0.040)	# 20fps
	
	# 表示更新(LATCH=＿|￣|＿)
	GPIO.output(26, GPIO.HIGH)
	GPIO.output(26, GPIO.LOW)
	
	#time.sleep(0.100)
	
	
elapsed_time = time.time() - start_time

print('%f [s]' % elapsed_time)
print('fps = %f' % (count / elapsed_time))


# 表示消去
panel = [[0 for x in range(24)] for y in range(8)]
xfer_data = panel_to_command(panel, 0x01)
xfer_data = map(reverse_bit_order, xfer_data)
for i in range(6):
	spi.writebytes(xfer_data[i*36:(i+1)*36])
	time.sleep(0.001)
time.sleep(0.010)
GPIO.output(26, GPIO.HIGH)
GPIO.output(26, GPIO.LOW)


GPIO.cleanup()
print('Done.')

