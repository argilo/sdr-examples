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
from gnuradio.fft import window
import dvbt
import osmosdr
import sys
from optparse import OptionParser

# ======================================================================

# ----------------------------------------------------------------------
def getInputFromDict(input_dict, input_key):
# ----------------------------------------------------------------------
    if input_key in input_dict:
        return input_dict[input_key]
    else:
        return None

# ----------------------------------------------------------------------
def getInputOptions():
# ----------------------------------------------------------------------
    default_ts_file = "/tmp/in.fifo"
    default_freq = 437.5e6
    default_width = 1e6
    fft_sizes = {"2k": dvbt.T2k, "8k": dvbt.T8k}
    code_rates = {"1/2": dvbt.C1_2, "2/3": dvbt.C2_3}
    guard_intervals = {"1/4": dvbt.G1_4, "2/3": dvbt.G1_32}
    constellations = {"QPSK": dvbt.QPSK, "QAM16": dvbt.QAM16, "QAM64": dvbt.QAM64}
    default_txvga_gains_str = "-4,20"

    parser = OptionParser(usage="usage: %%prog -r <history file>  [-d <db file name> [-f] [-q]] [-a] [-H]\n\n%s")
    parser.add_option("-i", "--ts-file", dest="ts_file", help="Input transport stream file or FIFO (default %s)" % default_ts_file, metavar="DATA_FILE", type="string")   
    parser.add_option("-o", "--output-file", dest="out_file", help="Output complex samples file (default None)", metavar="OUTPUT_FILE", type="string")   
    parser.add_option("-f", "--frequency", dest="freq", help="Transmit center frequency in Hz (default %.3e)" % default_freq, metavar="FREQUENCY", type="float")   
    parser.add_option("-w", "--width", dest="width", help="Channel width in Hz (default %.3e)" % default_width, metavar="WIDTH", type="float")   
    parser.add_option("-F", "--fft-size", dest="fft_size_str", help="FFT size: %s (default 2k)" % fft_sizes.keys(), metavar="FFT_SIZE", type="string")   
    parser.add_option("-r", "--code-rate", dest="code_rate_str", help="FEC code rate: %s (default 1/2)" % code_rates.keys(), metavar="CODE_RATE", type="string")   
    parser.add_option("-g", "--guard-interval", dest="guard_interval_str", help="Guard interval: %s (default 1/4)" % guard_intervals.keys(), metavar="GUARD_INTERVAL", type="string")   
    parser.add_option("-c", "--constellation", dest="constellation_str", help="Constellations: %s (default QPSK)" % constellations.keys(), metavar="CONSTELLATION", type="string")   
    parser.add_option("-G", "--txvga-gains", dest="txvga_gains_str", help="Comma separated TX VGA gains 1 and 2 (default: %s)" % default_txvga_gains_str, metavar="GAINS", type="string")   
    parser.add_option("-R", "--repeat", dest="repeat", help="Loop on input file indefinitely (delfault No)", metavar="CANCEL_LOCAL", action="store_true", default=False)
    parser.add_option("-I", "--stdin", dest="stdin", help="Input from stdin (delfault No)", metavar="CANCEL_LOCAL", action="store_true", default=False)

    (options, args) = parser.parse_args()
    
    options.fft_size = None
    options.code_rate = None
    options.guard_interval = None
    options.constellation = None
    
    if options.ts_file == None:
        options.ts_file = default_ts_file
                
    if options.freq == None:
        options.freq = int(default_freq)
    else:
        options.freq = int(options.freq)
        
    if options.width == None:
        options.width = default_width

    if options.fft_size_str == None:
        options.fft_size = dvbt.T2k
    else:
        options.fft_size = getInputFromDict(fft_sizes, options.fft_size_str)
        if options.fft_size == None:
            raise InputError("Invalid FFT size specified")
        
    if options.code_rate_str == None:
        options.code_rate = dvbt.C1_2
    else:
        options.code_rate = getInputFromDict(code_rates, options.code_rate_str)
        if options.code_rate == None:
            raise InputError("Invalid code rate specified")
        
    if options.guard_interval_str == None:
        options.guard_interval = dvbt.G1_4
    else:
        options.guard_interval = getInputFromDict(guard_intervals, options.guard_interval_str)
        if options.code_rate == None:
            raise InputError("Invalid guard interval specified")

    if options.constellation_str == None:
        options.constellation = dvbt.QPSK
    else:
        options.constellation = getInputFromDict(constellations, options.constellation_str.upper())
        if options.constellation == None:
            raise InputError("Invalid constellation specified")
            
    if options.txvga_gains_str is None:
        options.txvga_gains_str = default_txvga_gains_str

    options.txvga_gains = []
    for gain_str in options.txvga_gains_str.split(","):
        options.txvga_gains.append(int(gain_str))

    return options

# ======================================================================

# ----------------------------------------------------------------------
def main():
# ----------------------------------------------------------------------
    try:
        options = getInputOptions()

        ##################################################
        # Variables
        ##################################################

        channel_mhz = options.width / 1e6
        symbol_rate = channel_mhz * 8000000.0 / 7
        center_freq = options.freq
        
        mode = options.fft_size
        code_rate = options.code_rate
        guard = options.guard_interval
        constellation = options.constellation
        
        txvga1_gain = options.txvga_gains[0]
        txvga2_gain = options.txvga_gains[1]

        if mode == dvbt.T2k:
            factor = 1
            carriers = 2048
        elif mode == dvbt.T8k:
            factor = 4
            carriers = 8192

        if channel_mhz >= 8:
            bandwidth = 8750000
        elif channel_mhz <= 7:
            bandwidth = 7000000
        elif channel_mhz <= 6:
            bandwidth = 6000000
        elif channel_mhz <= 5:
            bandwidth = 5000000
        elif channel_mhz <= 2:
            bandwidth = 2500000
        elif channel_mhz <= 1:
            bandwidth = 1500000
        else:
            bandwidth = 8750000

        ##################################################
        # Blocks
        ##################################################

        tb = gr.top_block()

        if options.stdin:
            src = blocks.file_descriptor_source(gr.sizeof_char, 0, False)
        else:
            src = blocks.file_source(gr.sizeof_char, options.ts_file, options.repeat)

        dvbt_energy_dispersal = dvbt.energy_dispersal(1 * factor)
        dvbt_reed_solomon_enc = dvbt.reed_solomon_enc(2, 8, 0x11d, 255, 239, 8, 51, (8 * factor))
        dvbt_convolutional_interleaver = dvbt.convolutional_interleaver((136 * factor), 12, 17)
        dvbt_inner_coder = dvbt.inner_coder(1, (1512 * factor), constellation, dvbt.NH, code_rate)
        dvbt_bit_inner_interleaver = dvbt.bit_inner_interleaver((1512 * factor), constellation, dvbt.NH, mode)
        dvbt_symbol_inner_interleaver = dvbt.symbol_inner_interleaver((1512 * factor), mode, 1)
        dvbt_dvbt_map = dvbt.dvbt_map((1512 * factor), constellation, dvbt.NH, mode, 1)
        dvbt_reference_signals = dvbt.reference_signals(gr.sizeof_gr_complex, (1512 * factor), carriers, constellation, dvbt.NH, code_rate, code_rate, guard, mode, 0, 0)
        fft_vxx = fft.fft_vcc(carriers, False, (window.rectangular(carriers)), True, 10)
        digital_ofdm_cyclic_prefixer = digital.ofdm_cyclic_prefixer(carriers, carriers+(64 * factor), 0, "")
        blocks_multiply_const_vxx = blocks.multiply_const_vcc((0.0022097087 * 2.5, ))

        out = osmosdr.sink(args="bladerf=0,buffers=128,buflen=32768")
        out.set_sample_rate(symbol_rate)
        out.set_center_freq(center_freq, 0)
        out.set_freq_corr(0, 0)
        out.set_gain(txvga2_gain, 0)
        out.set_bb_gain(txvga1_gain, 0)
        out.set_bandwidth(bandwidth, 0)

        ##################################################
        # Connections
        ##################################################

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

        if options.out_file:
            dst = blocks.file_sink(gr.sizeof_gr_complex, options.out_file)
            tb.connect(blocks_multiply_const_vxx, dst)

        tb.run()
        
    except KeyboardInterrupt:
        pass

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
