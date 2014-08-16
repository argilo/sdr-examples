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

from array import array
import math

COLOR_FREQ = 3579545.0
SAMPLES_PER_LINE = 858
SAMP_RATE = 13500000
RADIANS_PER_SAMPLE = 2 * math.pi * COLOR_FREQ / SAMP_RATE

SYNCH_LEVEL = -40.0
BLANKING_LEVEL = 0.0
BLACK_LEVEL = 7.5
WHITE_LEVEL = 100.0

EQUALIZING_PULSE = [SYNCH_LEVEL] * 31 + [BLANKING_LEVEL] * 398
SYNCHRONIZING_PULSE = [SYNCH_LEVEL] * 366 + [BLANKING_LEVEL] * 63
INTERVALS = EQUALIZING_PULSE * 6 + SYNCHRONIZING_PULSE * 6 + EQUALIZING_PULSE * 6
EXTRA_HALF_LINE = [BLANKING_LEVEL] * 429

FRONT_PORCH = [BLANKING_LEVEL] * 20
SYNCH_PULSE = [SYNCH_LEVEL] * 63

def addBackPorch():
  global ntsc_signal
  ntsc_signal += [BLANKING_LEVEL] * 14
  l = len(ntsc_signal)
  for x in range(l, l+35):
    ntsc_signal += [BLANKING_LEVEL + 20 * math.sin(math.pi + RADIANS_PER_SAMPLE * x)]
  ntsc_signal += [BLANKING_LEVEL] * 14

def addNonVisibleLine():
  global ntsc_signal
  ntsc_signal += SYNCH_PULSE
  addBackPorch()
  ntsc_signal += [BLANKING_LEVEL] * 732

def addFirstHalfFrame():
  global ntsc_signal
  ntsc_signal += SYNCH_PULSE
  addBackPorch()
  ntsc_signal += [BLACK_LEVEL] * 303

def addSecondHalfFrame():
  global ntsc_signal
  ntsc_signal += SYNCH_PULSE
  addBackPorch()
  ntsc_signal += [BLANKING_LEVEL] * 303 + [BLACK_LEVEL] * 409 + FRONT_PORCH

def addPixel(y, cb, cr):
  global ntsc_signal, BLACK_LEVEL, WHITE_LEVEL
  Ey = y / 255.
  Eq = cb / 255. - 0.5
  Ei = cr / 255. - 0.5

  phase = RADIANS_PER_SAMPLE * len(ntsc_signal) + (33.0 / 180 * math.pi)
  Em = Ey + Eq * math.sin(phase) + Ei * math.cos(phase)

  ntsc_signal += [BLACK_LEVEL + (WHITE_LEVEL - BLACK_LEVEL) * Em]

def interpolate(samples):
  # For now, just double up the samples
  result = []
  for s in samples:
    result.extend([s, s])
  return result

#with open("bars601.yuv", "rb") as fin:
with open("out.yuv", "rb") as fin:
  while True:
    ntsc_signal = []
    bb = fin.read(720 * 480 * 2)
    if bb == '': break

    # Generate even field
    ntsc_signal += INTERVALS
    for x in range(13):
      addNonVisibleLine()
    for line in range(0,480,2):
      ntsc_signal += SYNCH_PULSE
      addBackPorch()

      bytes = bb[line*720*2:(line+1)*720*2]
      Y = [ord(b) for b in bytes[1::2]]
      Cb = interpolate([ord(b) for b in bytes[0::4]])
      Cr = interpolate([ord(b) for b in bytes[2::4]])
      for x in range(4, 716):
        addPixel(Y[x], Cb[x], Cr[x])

      ntsc_signal += FRONT_PORCH
    addFirstHalfFrame()

    # Generate odd field
    ntsc_signal += INTERVALS + EXTRA_HALF_LINE
    for x in range(12):
      addNonVisibleLine()
    addSecondHalfFrame()
    for line in range(1,481,2):
      ntsc_signal += SYNCH_PULSE
      addBackPorch()

      bytes = bb[line*720*2:(line+1)*720*2]
      Y = [ord(b) for b in bytes[1::2]]
      Cb = interpolate([ord(b) for b in bytes[0::4]])
      Cr = interpolate([ord(b) for b in bytes[2::4]])
      for x in range(4, 716):
        addPixel(Y[x], Cb[x], Cr[x])

      ntsc_signal += FRONT_PORCH

    ntsc_signal = [0.75 - (0.25/40) * x for x in ntsc_signal]

    f = open('ve3irr-testing.dat', 'ab')
    ntsc_array = array('f', ntsc_signal)
    ntsc_array.tofile(f)
    f.close()
