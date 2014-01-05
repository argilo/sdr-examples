#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Multi Tx
# Generated: Sun Jan  5 11:26:54 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iqbalance
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class multi_tx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Multi Tx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.audio_rate = audio_rate = 48000
        self.wpm = wpm = 15
        self.samp_rate = samp_rate = audio_rate * 40
        self.phase = phase = 0
        self.magnitude = magnitude = 0
        self.gain = gain = 25
        self.center_freq = center_freq = 441000000

        ##################################################
        # Blocks
        ##################################################
        _phase_sizer = wx.BoxSizer(wx.VERTICAL)
        self._phase_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_phase_sizer,
        	value=self.phase,
        	callback=self.set_phase,
        	label='phase',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._phase_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_phase_sizer,
        	value=self.phase,
        	callback=self.set_phase,
        	minimum=-0.1,
        	maximum=0.1,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_phase_sizer)
        _magnitude_sizer = wx.BoxSizer(wx.VERTICAL)
        self._magnitude_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_magnitude_sizer,
        	value=self.magnitude,
        	callback=self.set_magnitude,
        	label='magnitude',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._magnitude_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_magnitude_sizer,
        	value=self.magnitude,
        	callback=self.set_magnitude,
        	minimum=-0.1,
        	maximum=0.1,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_magnitude_sizer)
        self.root_raised_cosine_filter_1 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, audio_rate, 5, 0.35, 200))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(1, firdes.root_raised_cosine(
        	1, audio_rate, 5, 0.35, 200))
        self.rational_resampler_xxx_3 = filter.rational_resampler_ccc(
                interpolation=192,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_2 = filter.rational_resampler_ccc(
                interpolation=samp_rate,
                decimation=audio_rate,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=samp_rate / audio_rate / 2,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=samp_rate / audio_rate / 4,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(gain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_1 = filter.interp_fir_filter_ccf(1, firdes.low_pass(
        	0.5, audio_rate, 5000, 400, firdes.WIN_HAMMING, 6.76))
        self.iqbalance_fix_cc_0 = iqbalance.fix_cc(magnitude, phase)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
          constellation_points=2,
          mod_code="none",
          differential=True,
          samples_per_symbol=8,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.digital_map_bb_0 = digital.map_bb(([1,0]))
        self.blocks_wavfile_source_0 = blocks.wavfile_source("multi_tx.wav", True)
        self.blocks_vector_source_x_2 = blocks.vector_source_b((0,0, 1,1,0,1,1,0,1, 0,0, 1,0,1,0,1,1, 0,0, 1,1,0,1, 0,0, 1,0,1,1,1, 0,0, 1, 0,0, 1,1,0,1, 0,0, 1,0,1,1,1, 0,0, 1, 0,0, 1,1,0,1,1,0,1,0,1, 0,0, 1,1,1,0,1,1,1, 0,0, 1,1,1,1,1,1,1,1, 0,0, 1,1,1,1,1,1,1, 0,0, 1,0,1,0,1,1,1,1, 0,0, 1,0,1,0,1,1,1,1, 0,0, 1, 0,0, 1,0,1, 0,0, 1,1, 0,0, 1,0,1,1,1, 0,0, 1,0,1, 0,0, 1,1,0,1, 0,0, 1,1,1,1, 0,0, 1,0,1,1,0,1,1, 0,0, 1,0,1,0,1,1,1, 0,0, 1,1,1,0,1), True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_c((1,0,1,0,1,0,1,1,1, 0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0,0,0,0,0, 1,1,1,0,1,0,1, 0,0,0, 1, 0,0,0,0,0,0,0, 1,0,1,0,1,0,1,1,1, 0,0,0, 1, 0,0,0, 1,0,1,0,1,0,1,1,1,0,1,1,1, 0,0,0, 1,0,1, 0,0,0, 1,0,1,1,1,0,1, 0,0,0, 1,0,1,1,1,0,1, 0,0,0,0,0,0,0, 1,1,1, 0,0,0, 1, 0,0,0, 1,0,1,0,1, 0,0,0, 1,1,1, 0,0,0, 1,0,1, 0,0,0, 1,1,1,0,1, 0,0,0, 1,1,1,0,1,1,1,0,1, 0,0,0,0,0,0,0), True, 1, [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, int(1.2 * audio_rate / wpm))
        self.blocks_multiply_xx_6 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_5 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_4 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_3_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_3 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vcc((0.5, ))
        self.band_pass_filter_0_0 = filter.interp_fir_filter_ccc(1, firdes.complex_band_pass(
        	1, audio_rate, -2800, -200, 200, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.interp_fir_filter_ccc(1, firdes.complex_band_pass(
        	1, audio_rate, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=audio_rate,
        	quad_rate=audio_rate * 4,
        	tau=75e-6,
        	max_dev=75e3,
        )
        self.analog_sig_source_x_6 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 22000, 1, 0)
        self.analog_sig_source_x_5 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 20000, 1, 0)
        self.analog_sig_source_x_4 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 120000, 1.0 / 7, 0)
        self.analog_sig_source_x_3_0 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 11000, 1.8, 0)
        self.analog_sig_source_x_3 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 14000, 1.8, 0)
        self.analog_sig_source_x_2 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 0, 1, 0)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1.0 / 7, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -100000, 1.0 / 7, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=audio_rate,
        	quad_rate=audio_rate * 2,
        	tau=75e-6,
        	max_dev=5e3,
        )
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.analog_nbfm_tx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.rational_resampler_xxx_2, 0))
        self.connect((self.blocks_multiply_xx_4, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.analog_sig_source_x_4, 0), (self.blocks_multiply_xx_4, 1))
        self.connect((self.rational_resampler_xxx_2, 0), (self.blocks_multiply_xx_4, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.analog_sig_source_x_3_0, 0), (self.blocks_multiply_xx_3_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_xx_3_0, 0))
        self.connect((self.blocks_multiply_xx_3_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_xx_3, 0))
        self.connect((self.analog_sig_source_x_3, 0), (self.blocks_multiply_xx_3, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_3, 0), (self.blocks_add_xx_1, 2))
        self.connect((self.blocks_add_xx_0, 0), (self.iqbalance_fix_cc_0, 0))
        self.connect((self.iqbalance_fix_cc_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_multiply_xx_5, 0), (self.blocks_add_xx_1, 3))
        self.connect((self.analog_sig_source_x_5, 0), (self.blocks_multiply_xx_5, 1))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_multiply_xx_5, 0))
        self.connect((self.analog_sig_source_x_6, 0), (self.blocks_multiply_xx_6, 1))
        self.connect((self.blocks_multiply_xx_6, 0), (self.blocks_add_xx_1, 4))
        self.connect((self.rational_resampler_xxx_3, 0), (self.blocks_multiply_xx_6, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.rational_resampler_xxx_3, 0))
        self.connect((self.blocks_vector_source_x_2, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.root_raised_cosine_filter_1, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.root_raised_cosine_filter_0, 0))


# QT sink close method reimplementation

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_samp_rate(self.audio_rate * 40)
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, -2800, -200, 200, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, 200, 2800, 200, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(0.5, self.audio_rate, 5000, 400, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_2.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_5.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_3.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_3_0.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_6.set_sampling_freq(self.audio_rate)
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.audio_rate, 5, 0.35, 200))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.audio_rate, 5, 0.35, 200))

    def get_wpm(self):
        return self.wpm

    def set_wpm(self, wpm):
        self.wpm = wpm

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_4.set_sampling_freq(self.samp_rate)

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        self.iqbalance_fix_cc_0.set_phase(self.phase)
        self._phase_slider.set_value(self.phase)
        self._phase_text_box.set_value(self.phase)

    def get_magnitude(self):
        return self.magnitude

    def set_magnitude(self, magnitude):
        self.magnitude = magnitude
        self.iqbalance_fix_cc_0.set_mag(self.magnitude)
        self._magnitude_slider.set_value(self.magnitude)
        self._magnitude_text_box.set_value(self.magnitude)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_sink_0.set_gain(self.gain, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)

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
    tb = multi_tx()
    tb.Start(True)
    tb.Wait()

