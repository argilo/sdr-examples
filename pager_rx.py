#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Pager Rx
# Generated: Sun Dec 29 11:31:31 2013
##################################################

from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio import pager
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class pager_rx(grc_wxgui.top_block_gui):

    def __init__(self, options, queue):
        grc_wxgui.top_block_gui.__init__(self, title="Pager Rx")

        ##################################################
        # Variables
        ##################################################
        self.band = band = 929.5e6
        self.click_freq = click_freq = band - 500000 + 12500
        self.channel = channel = round((click_freq - (band - 500000 - 12500)) / 25000)
        self.samp_rate = samp_rate = 1200000
        self.freq = freq = band - 512500 + (channel * 25000)
        self.corr = corr = 0
        self.gain = gain = 40.0
        self.channel_rate = channel_rate = 25000

        ##################################################
        # Blocks
        ##################################################
        self._freq_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.freq,
        	callback=self.set_freq,
        	label="Frequency",
        	converter=forms.float_converter(),
        )
        self.GridAdd(self._freq_static_text, 1, 2, 1, 1)
        _corr_sizer = wx.BoxSizer(wx.VERTICAL)
        self._corr_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_corr_sizer,
        	value=self.corr,
        	callback=self.set_corr,
        	label="Frequency correction",
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
        self.GridAdd(_corr_sizer, 0, 2, 1, 1)
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label="Gain",
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
        self.GridAdd(_gain_sizer, 0, 0, 1, 2)
        self._band_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.band,
        	callback=self.set_band,
        	label='band',
        	choices=[929.5e6,931.5e6],
        	labels=["929-930","931-932"],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._band_chooser, 1, 0, 1, 1)
        self.wxgui_waterfallsink2_1 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=50,
        	ref_level=-20,
        	ref_scale=2.0,
        	sample_rate=channel_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Channel Waterfall",
        )
        self.Add(self.wxgui_waterfallsink2_1.win)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=band,
        	dynamic_range=50,
        	ref_level=-20,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Band Waterfall",
        )
        self.GridAdd(self.wxgui_waterfallsink2_0.win, 2, 0, 1, 3)
        def wxgui_waterfallsink2_0_callback(x, y):
        	self.set_click_freq(x)

        self.wxgui_waterfallsink2_0.set_callback(wxgui_waterfallsink2_0_callback)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(band, 0)
        self.osmosdr_source_0.set_freq_corr(corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(samp_rate / channel_rate, (filter.optfir.low_pass(1.0, samp_rate, 11000, 12500, 0.1, 60)), freq - band, samp_rate)
        _channel_sizer = wx.BoxSizer(wx.VERTICAL)
        self._channel_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_channel_sizer,
        	value=self.channel,
        	callback=self.set_channel,
        	label='channel',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._channel_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_channel_sizer,
        	value=self.channel,
        	callback=self.set_channel,
        	minimum=1,
        	maximum=40,
        	num_steps=39,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_channel_sizer, 1, 1, 1, 1)

        # FLEX protocol demodulator
        self.flex = pager.flex_demod(queue, 0, False, False) # options.verbose, options.log

        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_waterfallsink2_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.flex, 0))


# QT sink close method reimplementation

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self.set_click_freq(self.band - 500000 + 12500)
        self._band_chooser.set_value(self.band)
        self.set_freq(self.band - 512500 + (self.channel * 25000))
        self.set_channel(round((self.click_freq - (self.band - 500000 - 12500)) / 25000))
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.band)
        self.osmosdr_source_0.set_center_freq(self.band, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq - self.band)

    def get_click_freq(self):
        return self.click_freq

    def set_click_freq(self, click_freq):
        self.click_freq = click_freq
        self.set_channel(round((self.click_freq - (self.band - 500000 - 12500)) / 25000))

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.set_freq(self.band - 512500 + (self.channel * 25000))
        self._channel_slider.set_value(self.channel)
        self._channel_text_box.set_value(self.channel)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((filter.optfir.low_pass(1.0, self.samp_rate, 11000, 12500, 0.1, 60)))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_static_text.set_value(self.freq)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.freq - self.band)

    def get_corr(self):
        return self.corr

    def set_corr(self, corr):
        self.corr = corr
        self._corr_slider.set_value(self.corr)
        self._corr_text_box.set_value(self.corr)
        self.osmosdr_source_0.set_freq_corr(self.corr, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_channel_rate(self):
        return self.channel_rate

    def set_channel_rate(self, channel_rate):
        self.channel_rate = channel_rate
        self.wxgui_waterfallsink2_1.set_sample_rate(self.channel_rate)

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()

    # Flow graph emits pages into message queue
    queue = gr.msg_queue()
    tb = pager_rx(options, queue)
    runner = pager.queue_runner(queue)

    #tb = pager_rx()
    tb.Start(True)
    tb.Wait()
