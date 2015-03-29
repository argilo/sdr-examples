::

 # Copyright 2013-2014 Clayton Smith
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

sdr-examples
============

Author: Clayton Smith (argilo@gmail.com)

This project is a collection of GNU Radio examples created for a
tutorial session given at the Ottawa Amateur Radio Club.


multi_tx.grc & multi_tx.py
--------------------------

This example transmits the following signals simultaneously:

1. Narrowband FM at 440.9 MHz
2. Wideband FM at 441.0 MHz
3. AM at 441.120 MHz
4. LSB at 441.131 MHz
5. USB at 441.134 MHz
6. CW at 441.140 MHz
7. PSK31 at 441.142 MHz

It is built for the BladeRF, but it should easily be adaptable to other
boards such as the USRP B200/210 or HackRF.

Output power is split approximately equally between the six signals,
with the gain set such that no clipping occurs.


pager_rx.py
-----------

This example allows the reception of the FLEX protocol used to send
messages to pagers.  It is intended for use with a RTL-SDR dongle
such as the NooElec TV28T.

To use it, first set the frequency correction slider to the correct
value to match your dongle's crystal.  The gain slider should be set to
the highest value which does not cause clipping.  (If it's too high,
you'll see spurious signals appearing.)

Choose a band (929-930 MHz or 931-932 MHz) by clicking the appropriate
radio button.  The band waterfall will display all signals in that
band.  Click on a signal to tune to its channel.  When transmitting,
you should see the channel's signal in the channel waterfall display.
When the frequency correction slider is set correctly, the signal
should be centered in the channel waterfall display.


pager_rx_929.py
---------------

This example demonstrates reception of multiple FLEX channels
simultaneously.  It tunes three Ottawa-area FLEX transmitters at
929.1875, 929.2875 and 929.6625 MHz.  As with the previous example,
for correct decoding the frequency correction slider must be set
so that the signals appear in the center of the channel waterfall.
The gain slider should be set as high as possible without causing
spurious signals to appear.


va3rft.grc & va3rft.py
----------------------

This example receives an Ottawa-area DMR digital voice repeater,
VA3RFT on 444.475 MHz.  It is intended for use with an RTL-SDR dongle
such as the NooElec TV28T.  It depends on my GNU Radio DSD block,
which can be downloaded at https://github.com/argilo/gr-dsd.

To use it, set the frequency correction slider to the correct value
to match your dongle's crystal.  If necessary, set the gain slider to
an appropriate value to prevent clipping.

If the frequency correction slider is set correctly, you should see
transmissions appearing in the center of the band in the middle of
the waterfall.  Even when nobody is using the repeater, it transmits
some packets about once every 80 seconds.


va3odg.grc & va3odg.py
----------------------

This example is very similar to the DMR receiver above, but instead it
receives D-STAR.  It is intended to receive the Ottawa-area D-STAR
repeater VA3ODG on 444.850 MHz.

Since the D-STAR receiver in DSD is not yet optimized for GMSK
reception, I have worked around this problem by doing the GMSK
demodulation in GNU Radio (with a Clock Recovery MM and a Binary
Slicer block), then re-modulating the signal before passing it on to
DSD.  This improves the bit error rate.


atsc-blade.py & atsc-blade-usb2.py
----------------------------------

These examples transmit an ATSC digital television signal using the
BladeRF.  An file containing an MPEG 2 transport stream must be
supplied as input.  MPEG 2 transport streams can be produced with
tools such as avconv and OpenCaster.  The first example, atsc-blade.py
requires USB 3.0 to work properly, while the second example,
atsc-blade-usb2.py reduces the output sample rate so as to run on a
USB 2.0 port.  Both examples transmit on 438-444 MHz, but this can be
changed by adjusting the center_freq variable.


Making Bootable USB Images for GNURadio
=======================================


Install Some Kind of Ubuntu/Debian
----------------------------------

Install Xubuntu 14.04 LTS 64-bit (or newer) onto a 8 GB or larger flash drive.
Force the root partition to be 7.5 GB so that it can be installed on
*approximately* 8 GB drives that may vary in size a bit.

Boot Xubuntu, install updates and restart.

In /etc/default/rcS, set "UTC=no" so it won't mess up the system clock on
Windows laptops.

Install a few essential pieces in order to make it easier for people to use
the system and work with these example flow graphs::

    sudo apt-get install linux-firmware-nonfree

    sudo apt-get install git
    git clone --recursive https://github.com/argilo/sdr-examples.git


Install GNURadio and Related Tools
----------------------------------

Install the core GNURadio packages::

    sudo add-apt-repository ppa:gqrx/releases
    sudo apt-get update
    sudo apt-get install gnuradio gnuradio-dev gnuradio-doc gqrx-sdr

Install drivers for some of the most common SDR dongles::

    sudo apt-get install rtl-sdr hackrf bladerf-host \
        gr-fcdproplus qthid-fcd-controller

Add GRC and gqrx to the favourites in the xfce menu.


Compress Bootable Image
-----------------------

Purge old kernels.

::

    sudo apt-get install localepurge
    sudo apt-get clean
    cat /dev/zero > zero.fill ; sync ; sleep 1 ; sync ; rm -rf zero.fill

Shut down.

::

    sudo dd if=/dev/sdb bs=1M count=7500 |\
        gzip --rsyncable > bootable_image.img.gz
