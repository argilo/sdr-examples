#!/usr/bin/env /usr/bin/python

# Copyright 2014 Ron Economos (w6rz@comcast.net)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gnuradio import blocks
from gnuradio import digital
from gnuradio import dtv
from gnuradio import fft
from gnuradio import gr
from gnuradio.fft import window
from grc_gnuradio import blks2 as grc_blks2
import osmosdr
import sys

def main(args):
    nargs = len(args)
    if nargs == 1:
        port    = int(args[0])
        outfile = None
    elif nargs == 2:
        port     = int(args[0])
        outfile  = args[1]
    else:
        sys.stderr.write("Usage: dvbt-hackrf.py port [output_file]\n");
        sys.exit(1)

    channel_mhz = 6
    mode = dtv.T2k
    code_rate = dtv.C1_2
    constellation = dtv.MOD_QPSK
    guard_interval = dtv.GI_1_32
    symbol_rate = channel_mhz * 8000000.0 / 7
    center_freq = 441000000
    rf_gain = 14
    if_gain = 40

    if mode == dtv.T2k:
        factor = 1
        carriers = 2048
    elif mode == dtv.T8k:
        factor = 4
        carriers = 8192

    if guard_interval == dtv.GI_1_32:
        gi = carriers / 32
    elif guard_interval == dtv.GI_1_16:
        gi = carriers / 16
    elif guard_interval == dtv.GI_1_8:
        gi = carriers / 8
    elif guard_interval == dtv.GI_1_4:
        gi = carriers / 4

    if channel_mhz == 8:
        bandwidth = 8750000
    elif channel_mhz == 7:
        bandwidth = 7000000
    elif channel_mhz == 6:
        bandwidth = 6000000
    elif channel_mhz == 5:
        bandwidth = 5000000
    else:
        bandwidth = 8750000

    tb = gr.top_block()

    src = grc_blks2.tcp_source(gr.sizeof_char*1, "127.0.0.1", port, True)

    dvbt_energy_dispersal = dtv.dvbt_energy_dispersal(1 * factor)
    dvbt_reed_solomon_enc = dtv.dvbt_reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, (8 * factor))
    dvbt_convolutional_interleaver = dtv.dvbt_convolutional_interleaver((136 * factor), 12, 17)
    dvbt_inner_coder = dtv.dvbt_inner_coder(1, (1512 * factor), constellation, dtv.NH, code_rate)
    dvbt_bit_inner_interleaver = dtv.dvbt_bit_inner_interleaver((1512 * factor), constellation, dtv.NH, mode)
    dvbt_symbol_inner_interleaver = dtv.dvbt_symbol_inner_interleaver((1512 * factor), mode, 1)
    dvbt_map = dtv.dvbt_map((1512 * factor), constellation, dtv.NH, mode, 1)
    dvbt_reference_signals = dtv.dvbt_reference_signals(gr.sizeof_gr_complex, (1512 * factor), carriers, constellation, dtv.NH, code_rate, code_rate, dtv.GI_1_32, mode, 0, 0)
    fft_vxx = fft.fft_vcc(carriers, False, (window.rectangular(carriers)), True, 10)
    digital_ofdm_cyclic_prefixer = digital.ofdm_cyclic_prefixer(carriers, carriers+(gi), 0, "")
    blocks_multiply_const_vxx = blocks.multiply_const_vcc((0.0022097087 * 2.5, ))

    out = osmosdr.sink()
    out.set_sample_rate(symbol_rate)
    out.set_center_freq(center_freq, 0)
    out.set_freq_corr(0, 0)
    out.set_gain(rf_gain, 0)
    out.set_if_gain(if_gain, 0)
    out.set_bandwidth(bandwidth, 0)

    tb.connect(src, dvbt_energy_dispersal)
    tb.connect(dvbt_energy_dispersal, dvbt_reed_solomon_enc)
    tb.connect(dvbt_reed_solomon_enc, dvbt_convolutional_interleaver)
    tb.connect(dvbt_convolutional_interleaver, dvbt_inner_coder)
    tb.connect(dvbt_inner_coder, dvbt_bit_inner_interleaver)
    tb.connect(dvbt_bit_inner_interleaver, dvbt_symbol_inner_interleaver)
    tb.connect(dvbt_symbol_inner_interleaver, dvbt_map)
    tb.connect(dvbt_map, dvbt_reference_signals)
    tb.connect(dvbt_reference_signals, fft_vxx)
    tb.connect(fft_vxx, digital_ofdm_cyclic_prefixer)
    tb.connect(digital_ofdm_cyclic_prefixer, blocks_multiply_const_vxx)
    tb.connect(blocks_multiply_const_vxx, out)


    if outfile:
        dst = blocks.file_sink(gr.sizeof_gr_complex, outfile)
        tb.connect(blocks_multiply_const_vxx, dst)

    tb.run()


if __name__ == '__main__':
    main(sys.argv[1:])
