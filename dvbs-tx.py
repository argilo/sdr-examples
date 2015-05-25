#!/usr/bin/env /usr/bin/python

# Copyright 2015 Edouard Griffiths, F4EXB
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
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import trellis
from gnuradio.fft import window
import dvbs
import osmosdr
import sys
from optparse import OptionParser

half_bws = [750000, 875000, 1250000, 1375000, 1500000, 1920000, 2500000, 2750000, 3000000, 3500000, 4375000, 5000000, 6000000, 7000000, 10000000, 14000000]

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
    default_freq = 1.27e9
    symbol_rates = {"160k": 160000, "400k": 400000, "1M": 1000000, "1.5M": 1500000, "2M": 2000000}
    default_txvga_gains_str = "-4,20"

    parser = OptionParser(usage="usage: %%prog -r <history file>  [-d <db file name> [-f] [-q]] [-a] [-H]\n\n%s")
    parser.add_option("-i", "--ts-file", dest="ts_file", help="Input transport stream file or FIFO (default %s)" % default_ts_file, metavar="DATA_FILE", type="string")   
    parser.add_option("-o", "--output-file", dest="out_file", help="Output complex samples file (default None)", metavar="OUTPUT_FILE", type="string")   
    parser.add_option("-f", "--frequency", dest="freq", help="Transmit center frequency in Hz (default %.3e)" % default_freq, metavar="FREQUENCY", type="float")   
    parser.add_option("-s", "--symbol-rate", dest="symbol_rate_str", help="Symbol rate: %s (default 1M)" % symbol_rates.keys(), metavar="SYMBOL_RATE", type="string")   
    parser.add_option("-G", "--txvga-gains", dest="txvga_gains_str", help="Comma separated TX VGA gains 1 and 2 (default: %s)" % default_txvga_gains_str, metavar="GAINS", type="string")   
    parser.add_option("-r", "--repeat", dest="repeat", help="Loop on input file indefinitely (delfault No)", metavar="CANCEL_LOCAL", action="store_true", default=False)
    parser.add_option("-I", "--stdin", dest="stdin", help="Input from stdin (delfault No)", metavar="CANCEL_LOCAL", action="store_true", default=False)

    (options, args) = parser.parse_args()
        
    if options.ts_file == None:
        options.ts_file = default_ts_file
                
    if options.freq == None:
        options.freq = int(default_freq)
    else:
        options.freq = int(options.freq)
        
    if options.symbol_rate_str == None:
        options.symbol_rate = 1000000
    else:
        options.symbol_rate = getInputFromDict(symbol_rates, options.symbol_rate_str)
        if options.symbol_rate == None:
            raise InputError("Invalid symbol rate specified")        
            
    if options.txvga_gains_str is None:
        options.txvga_gains_str = default_txvga_gains_str

    options.txvga_gains = []
    for gain_str in options.txvga_gains_str.split(","):
        options.txvga_gains.append(int(gain_str))

    return options

# ----------------------------------------------------------------------
def getHalfBW(symbol_rate):
# ----------------------------------------------------------------------
    for half_bw in half_bws:
        if symbol_rate / 2 <= half_bw:
            return half_bw
    return half_bws[:-1]
    
# ======================================================================

# ----------------------------------------------------------------------
def main():
# ----------------------------------------------------------------------
    try:
        options = getInputOptions()

        ##################################################
        # Variables
        ##################################################

        center_freq = options.freq
        txvga1_gain = options.txvga_gains[0]
        txvga2_gain = options.txvga_gains[1]

        samp_rate = 2*options.symbol_rate
        half_bw = getHalfBW(options.symbol_rate)

        rrc_taps = 20

        ##################################################
        # Blocks
        ##################################################

        tb = gr.top_block()

        if options.stdin:
            blocks_file_source_0 = blocks.file_descriptor_source(gr.sizeof_char, 0, options.repeat)
        else:
            blocks_file_source_0 = blocks.file_source(gr.sizeof_char, options.ts_file, options.repeat)

        fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes.root_raised_cosine(1.79, samp_rate, samp_rate/2, 0.35, rrc_taps)), 1)
        fft_filter_xxx_0.declare_sample_delay(0)
        dvbs_reed_solomon_enc_bb_0 = dvbs.reed_solomon_enc_bb()
        dvbs_randomizer_bb_0 = dvbs.randomizer_bb()
        dvbs_puncture_bb_0 = dvbs.puncture_bb(dvbs.C1_2)
        dvbs_modulator_bc_0 = dvbs.modulator_bc()
        dvbs_interleaver_bb_0 = dvbs.interleaver_bb()
        blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(2)
        trellis_encoder_xx_0 =  trellis.encoder_bb(trellis.fsm(1, 2, (0171, 0133)), 0, 0) if False else trellis.encoder_bb(trellis.fsm(1, 2, (0171, 0133)), 0) 
        
        osmosdr_sink_0 = osmosdr.sink( args="bladerf=0,buffers=128,buflen=32768," +"numchan=" + str(1))
        osmosdr_sink_0.set_sample_rate(samp_rate)
        osmosdr_sink_0.set_center_freq(center_freq, 0)
        osmosdr_sink_0.set_freq_corr(0, 0)
        osmosdr_sink_0.set_gain(txvga2_gain, 0)
        osmosdr_sink_0.set_if_gain(0, 0)
        osmosdr_sink_0.set_bb_gain(txvga1_gain, 0)
        osmosdr_sink_0.set_antenna("", 0)
        osmosdr_sink_0.set_bandwidth(half_bw * 2, 0)


        ##################################################
        # Connections
        ##################################################

        tb.connect((blocks_file_source_0, 0), (dvbs_randomizer_bb_0, 0))    
        tb.connect((blocks_pack_k_bits_bb_0, 0), (dvbs_modulator_bc_0, 0))    
        tb.connect((blocks_packed_to_unpacked_xx_0, 0), (trellis_encoder_xx_0, 0))    
        tb.connect((blocks_unpack_k_bits_bb_0, 0), (dvbs_puncture_bb_0, 0))    
        tb.connect((dvbs_interleaver_bb_0, 0), (blocks_packed_to_unpacked_xx_0, 0))    
        tb.connect((dvbs_modulator_bc_0, 0), (fft_filter_xxx_0, 0))    
        tb.connect((dvbs_puncture_bb_0, 0), (blocks_pack_k_bits_bb_0, 0))    
        tb.connect((dvbs_randomizer_bb_0, 0), (dvbs_reed_solomon_enc_bb_0, 0))    
        tb.connect((dvbs_reed_solomon_enc_bb_0, 0), (dvbs_interleaver_bb_0, 0))    
        tb.connect((fft_filter_xxx_0, 0), (osmosdr_sink_0, 0))    
        tb.connect((trellis_encoder_xx_0, 0), (blocks_unpack_k_bits_bb_0, 0))    

        if options.out_file:
            dst = blocks.file_sink(gr.sizeof_gr_complex, options.out_file)
            tb.connect(fft_filter_xxx_0, dst)

        tb.run()
        
    except KeyboardInterrupt:
        pass

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
