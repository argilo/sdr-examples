#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: VA3ODG
# Generated: Mon Oct 24 21:56:12 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import dsd
import math
import osmosdr
import time
import wx


class va3odg(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="VA3ODG")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1920000
        self.offset = offset = 50000
        self.gain = gain = 40
        self.fsk_deviation_hz = fsk_deviation_hz = 8000
        self.freq = freq = 444850000
        self.corr = corr = 0

        ##################################################
        # Blocks
        ##################################################
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='RX gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=49.6,
        	num_steps=124,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        _corr_sizer = wx.BoxSizer(wx.VERTICAL)
        self._corr_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_corr_sizer,
        	value=self.corr,
        	callback=self.set_corr,
        	label='Freq. correction',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._corr_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_corr_sizer,
        	value=self.corr,
        	callback=self.set_corr,
        	minimum=-150,
        	maximum=150,
        	num_steps=300,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_corr_sizer)
        self.wxgui_waterfallsink2_1 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=50,
        	ref_level=-20,
        	ref_scale=2.0,
        	sample_rate=48000,
        	fft_size=512,
        	fft_rate=3,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.Add(self.wxgui_waterfallsink2_1.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=48000,
        	v_scale=0.25,
        	v_offset=0,
        	t_scale=0.001,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_fff(10, firdes.root_raised_cosine(
        	1, 48000, 4800, 0.35, 100))
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq - offset, 0)
        self.osmosdr_source_0.set_freq_corr(corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, 48000, 8000, 2000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(40, firdes.low_pass(
        	20, samp_rate, 3500, 2000, firdes.WIN_HAMMING, 6.76))
        self.dsd_block_ff_0 = dsd.dsd_block_ff(dsd.dsd_FRAME_DSTAR,dsd.dsd_MOD_AUTO_SELECT,3,True,2)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(10.0, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf(([-1,1]), 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.audio_sink_0 = audio.sink(8000, '', True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -offset, 1, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.root_raised_cosine_filter_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.dsd_block_ff_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_waterfallsink2_1, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.root_raised_cosine_filter_0, 0), (self.dsd_block_ff_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(20, self.samp_rate, 3500, 2000, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.osmosdr_source_0.set_center_freq(self.freq - self.offset, 0)
        self.analog_sig_source_x_0.set_frequency(-self.offset)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0.set_center_freq(self.freq - self.offset, 0)

    def get_corr(self):
        return self.corr

    def set_corr(self, corr):
        self.corr = corr
        self._corr_slider.set_value(self.corr)
        self._corr_text_box.set_value(self.corr)
        self.osmosdr_source_0.set_freq_corr(self.corr, 0)


def main(top_block_cls=va3odg, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
