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
from gnuradio import fft
from gnuradio import gr
from gnuradio import uhd
from gnuradio.fft import window
from grc_gnuradio import blks2 as grc_blks2
import dvbt
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
        sys.stderr.write("Usage: dvbt-blade.py port [output_file]\n");
        sys.exit(1)

    channel_mhz = 6
    mode = dvbt.T2k
    code_rate = dvbt.C1_2
    constellation = dvbt.QPSK
    guard_interval = dvbt.G1_32
    symbol_rate = channel_mhz * 8000000.0 / 7
    center_freq = 441000000
    tx_gain = 83 # max 89.5

    if mode == dvbt.T2k:
        factor = 1
        carriers = 2048
    elif mode == dvbt.T8k:
        factor = 4
        carriers = 8192

    if guard_interval == dvbt.G1_32:
        gi = carriers / 32
    elif guard_interval == dvbt.G1_16:
        gi = carriers / 16
    elif guard_interval == dvbt.G1_8:
        gi = carriers / 8
    elif guard_interval == dvbt.G1_4:
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

    out = uhd.usrp_sink(
        	device_addr="recv_frame_size=65536,num_recv_frames=128,send_frame_size=65536,num_send_frames=128,master_clock_rate=" + str(symbol_rate*4),
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		otw_format="sc16",
        		channels=range(1),
        	),
        )
    out.set_samp_rate(symbol_rate)
    out.set_center_freq(center_freq, 0)
    out.set_gain(tx_gain, 0)

    #src = blocks.udp_source(gr.sizeof_char*1, "127.0.0.1", port, 18800, True)
    src = grc_blks2.tcp_source(gr.sizeof_char*1, "127.0.0.1", port, True)

    dvbt_energy_dispersal = dvbt.energy_dispersal(1 * factor)
    dvbt_reed_solomon_enc = dvbt.reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, (8 * factor))
    dvbt_convolutional_interleaver = dvbt.convolutional_interleaver((136 * factor), 12, 17)
    dvbt_inner_coder = dvbt.inner_coder(1, (1512 * factor), constellation, dvbt.NH, code_rate)
    dvbt_bit_inner_interleaver = dvbt.bit_inner_interleaver((1512 * factor), constellation, dvbt.NH, mode)
    dvbt_symbol_inner_interleaver = dvbt.symbol_inner_interleaver((1512 * factor), mode, 1)
    dvbt_dvbt_map = dvbt.dvbt_map((1512 * factor), constellation, dvbt.NH, mode, 1)
    dvbt_reference_signals = dvbt.reference_signals(gr.sizeof_gr_complex, (1512 * factor), carriers, constellation, dvbt.NH, code_rate, code_rate, dvbt.G1_32, mode, 0, 0)
    fft_vxx = fft.fft_vcc(carriers, False, (window.rectangular(carriers)), True, 10)
    digital_ofdm_cyclic_prefixer = digital.ofdm_cyclic_prefixer(carriers, carriers+(gi), 0, "")
    blocks_multiply_const_vxx = blocks.multiply_const_vcc((0.0022097087 * 2.5, ))

    tb.connect(src, dvbt_energy_dispersal)
    tb.connect(dvbt_energy_dispersal, dvbt_reed_solomon_enc)
    tb.connect(dvbt_reed_solomon_enc, dvbt_convolutional_interleaver)
    tb.connect(dvbt_convolutional_interleaver, dvbt_inner_coder)
    tb.connect(dvbt_inner_coder, dvbt_bit_inner_interleaver)
    tb.connect(dvbt_bit_inner_interleaver, dvbt_symbol_inner_interleaver)
    tb.connect(dvbt_symbol_inner_interleaver, dvbt_dvbt_map)
    tb.connect(dvbt_dvbt_map, dvbt_reference_signals)
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
