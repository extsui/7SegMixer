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
	command = []
	for armor in range(6):
		for y in range(4):
			command.append(0x01)
			for x in range(8):
				command.append(real_panel[armor][y][x])
	return command

# パネルからコマンドへの変換
def panel_to_command(panel):
	real_panel = to_real_panel(panel)
	command = to_armor_command(real_panel)
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
"""
for y in range(8):
	for x in range(24):
		panel[y][x] = 0xFF
		xfer_data = panel_to_command(panel)
		xfer_data = map(reverse_bit_order, xfer_data)
		
		for i in range(6):
			spi.writebytes(xfer_data[i*36:(i+1)*36])
			#time.sleep(0.001)
			
		time.sleep(0.006)
		
		# 表示更新(LATCH=＿|￣|＿)
		GPIO.output(26, GPIO.HIGH)
		GPIO.output(26, GPIO.LOW)
		
		print('%d' % (x + y*24))


for y in range(8):
	for x in range(24):
		panel[y][x] = 0x00
		xfer_data = panel_to_command(panel)
		xfer_data = map(reverse_bit_order, xfer_data)
		
		for i in range(6):
			spi.writebytes(xfer_data[i*36:(i+1)*36])
			#time.sleep(0.001)
			
		time.sleep(0.006)
		
		# 表示更新(LATCH=＿|￣|＿)
		GPIO.output(26, GPIO.HIGH)
		GPIO.output(26, GPIO.LOW)
		
		print('%d' % (x + y*24))
"""


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
	
while (True):
	for ptn in num_to_pattern:
		
		panel = [[ptn for x in range(24)] for y in range(8)]
		
		xfer_data = panel_to_command(panel)
		xfer_data = map(reverse_bit_order, xfer_data)
		
		for i in range(6):
			spi.writebytes(xfer_data[i*36:(i+1)*36])
			#time.sleep(0.010)
			
		time.sleep(0.010)
		
		# 表示更新(LATCH=＿|￣|＿)
		GPIO.output(26, GPIO.HIGH)
		GPIO.output(26, GPIO.LOW)
		
		time.sleep(0.0100)
		
elapsed_time = time.time() - start_time

print('%f [s]' % elapsed_time)
print('fps = %f' % (24*8. / elapsed_time))

GPIO.cleanup()
print('Done.')

