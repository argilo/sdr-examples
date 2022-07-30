# Copyright 2014 Clayton Smith
#
# This file is part of sdr-examples
#
# sdr-examples is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# sdr-examples is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sdr-examples; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from PIL import Image
from array import array
import math

image = Image.open("ve3irr-testing.png")
# image = Image.open("smpte-bars.png")
pixels = list(image.getdata())

COLOR_FREQ = 3579545.0
SAMPLES_PER_LINE = 768
SAMP_RATE = SAMPLES_PER_LINE * 60 * .999 * 525 / 2
RADIANS_PER_SAMPLE = 2 * math.pi * COLOR_FREQ / SAMP_RATE

SYNCH_LEVEL = -40.0
BLANKING_LEVEL = 0.0
BLACK_LEVEL = 7.5
WHITE_LEVEL = 100.0

EQUALIZING_PULSE = [SYNCH_LEVEL] * 28 + [BLANKING_LEVEL] * 356
SYNCHRONIZING_PULSE = [SYNCH_LEVEL] * 327 + [BLANKING_LEVEL] * 57
INTERVALS = EQUALIZING_PULSE * 6 + SYNCHRONIZING_PULSE * 6 + EQUALIZING_PULSE * 6
EXTRA_HALF_LINE = [BLANKING_LEVEL] * 384

FRONT_PORCH = [BLANKING_LEVEL] * 18
SYNCH_PULSE = [SYNCH_LEVEL] * 57


def addBackPorch():
    global ntsc_signal
    ntsc_signal += [BLANKING_LEVEL] * 13
    l = len(ntsc_signal)
    for x in range(l, l+31):
        ntsc_signal += [BLANKING_LEVEL + 20 * math.sin(math.pi + RADIANS_PER_SAMPLE * x)]
    ntsc_signal += [BLANKING_LEVEL] * 13


def addNonVisibleLine():
    global ntsc_signal
    ntsc_signal += SYNCH_PULSE
    addBackPorch()
    ntsc_signal += [BLANKING_LEVEL] * 654


def addLine21(char_one, char_two):
    global ntsc_signal

    bits = []
    for char in (char_one, char_two):
        parity = 1
        for bit_num in range(7):
            bit = (char >> bit_num) & 1
            parity ^= bit
            bits.append(bit)
        bits.append(parity)

    ntsc_signal += SYNCH_PULSE
    addBackPorch()
    ntsc_signal += [BLANKING_LEVEL] * 7

    for x in range(7 * 24):
        ntsc_signal.append(25.0 + 25.0 * math.sin(2 * math.pi * (x-5.5) / 24))

    ntsc_signal += [0.0] * 18  # S1
    ntsc_signal += [0.0] * 24  # S2
    ntsc_signal += [50.0] * 24  # S3

    for bit in bits:
        ntsc_signal += [50.0 if bit else 0.0] * 24

    ntsc_signal += [BLANKING_LEVEL] * 29


def addFirstHalfFrame():
    global ntsc_signal
    ntsc_signal += SYNCH_PULSE
    addBackPorch()
    ntsc_signal += [BLACK_LEVEL] * 270


def addSecondHalfFrame():
    global ntsc_signal
    ntsc_signal += SYNCH_PULSE
    addBackPorch()
    ntsc_signal += [BLANKING_LEVEL] * 270 + [BLACK_LEVEL] * 366 + FRONT_PORCH


def addPixel(p):
    global ntsc_signal, BLACK_LEVEL, WHITE_LEVEL
    Er = float(p[0]) / 255
    Eg = float(p[1]) / 255
    Eb = float(p[2]) / 255

    Ey = 0.30 * Er + 0.59 * Eg + 0.11 * Eb
    Eq = 0.41 * (Eb - Ey) + 0.48 * (Er - Ey)
    Ei = -0.27 * (Eb - Ey) + 0.74 * (Er - Ey)

    phase = RADIANS_PER_SAMPLE * len(ntsc_signal) + (33.0 / 180 * math.pi)
    Em = Ey + Eq * math.sin(phase) + Ei * math.cos(phase)

    ntsc_signal += [BLACK_LEVEL + (WHITE_LEVEL - BLACK_LEVEL) * Em]


line21_codes = [
    (0x14, 0x25),
    (0x14, 0x25),
    (0x14, 0x2D),
    (0x14, 0x2D),
    (0x14, 0x70),
    (0x14, 0x70),
]
cc_text = "Test One Two Three Four Five"
for x in range(0, len(cc_text), 2):
    line21_codes.append((ord(cc_text[x]), ord(cc_text[x+1])))

ntsc_signal = []

for line21_code in line21_codes:
    # Generate even field
    ntsc_signal += INTERVALS
    for x in range(13):
        if x == 11:
            addLine21(line21_code[0], line21_code[1])
        else:
            addNonVisibleLine()
    for line in range(0, 480, 2):
        ntsc_signal += SYNCH_PULSE
        addBackPorch()
        for x in range(line * 640 + 2, (line+1) * 640 - 2):
            addPixel(pixels[x])
        ntsc_signal += FRONT_PORCH
    addFirstHalfFrame()

    # Generate odd field
    ntsc_signal += INTERVALS + EXTRA_HALF_LINE
    for x in range(12):
        addNonVisibleLine()
    addSecondHalfFrame()
    for line in range(1, 481, 2):
        ntsc_signal += SYNCH_PULSE
        addBackPorch()
        for x in range(line * 640 + 2, (line+1) * 640 - 2):
            addPixel(pixels[x])
        ntsc_signal += FRONT_PORCH

ntsc_signal = [0.75 - (0.25/40) * x for x in ntsc_signal]

f = open('ve3irr-testing.dat', 'wb')
ntsc_array = array('f', ntsc_signal)
ntsc_array.tofile(f)
f.close()
