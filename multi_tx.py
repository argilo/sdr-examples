#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Multi Tx
# GNU Radio version: 3.10.0.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iqbalance
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import osmosdr
import time



from gnuradio import qtgui

class multi_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Multi Tx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Multi Tx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "multi_tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.audio_rate = audio_rate = 48000
        self.wpm = wpm = 15
        self.wbfm_on = wbfm_on = False
        self.usb_on = usb_on = True
        self.samp_rate = samp_rate = audio_rate * 40
        self.q_offset = q_offset = 0
        self.psk_on = psk_on = True
        self.phase = phase = 0
        self.nbfm_on = nbfm_on = True
        self.magnitude = magnitude = 0
        self.lsb_on = lsb_on = True
        self.i_offset = i_offset = 0
        self.gain = gain = 25
        self.cw_on = cw_on = True
        self.center_freq = center_freq = 441000000
        self.am_on = am_on = True

        ##################################################
        # Blocks
        ##################################################
        _wbfm_on_check_box = Qt.QCheckBox("WBFM")
        self._wbfm_on_choices = {True: True, False: False}
        self._wbfm_on_choices_inv = dict((v,k) for k,v in self._wbfm_on_choices.items())
        self._wbfm_on_callback = lambda i: Qt.QMetaObject.invokeMethod(_wbfm_on_check_box, "setChecked", Qt.Q_ARG("bool", self._wbfm_on_choices_inv[i]))
        self._wbfm_on_callback(self.wbfm_on)
        _wbfm_on_check_box.stateChanged.connect(lambda i: self.set_wbfm_on(self._wbfm_on_choices[bool(i)]))
        self.top_grid_layout.addWidget(_wbfm_on_check_box, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _usb_on_check_box = Qt.QCheckBox("USB")
        self._usb_on_choices = {True: True, False: False}
        self._usb_on_choices_inv = dict((v,k) for k,v in self._usb_on_choices.items())
        self._usb_on_callback = lambda i: Qt.QMetaObject.invokeMethod(_usb_on_check_box, "setChecked", Qt.Q_ARG("bool", self._usb_on_choices_inv[i]))
        self._usb_on_callback(self.usb_on)
        _usb_on_check_box.stateChanged.connect(lambda i: self.set_usb_on(self._usb_on_choices[bool(i)]))
        self.top_grid_layout.addWidget(_usb_on_check_box, 4, 4, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._q_offset_range = Range(-0.1, 0.1, ((0.1) - (-0.1))/200, 0, 200)
        self._q_offset_win = RangeWidget(self._q_offset_range, self.set_q_offset, "DC offsett Q", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._q_offset_win, 3, 0, 1, 7)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        _psk_on_check_box = Qt.QCheckBox("PSK31")
        self._psk_on_choices = {True: True, False: False}
        self._psk_on_choices_inv = dict((v,k) for k,v in self._psk_on_choices.items())
        self._psk_on_callback = lambda i: Qt.QMetaObject.invokeMethod(_psk_on_check_box, "setChecked", Qt.Q_ARG("bool", self._psk_on_choices_inv[i]))
        self._psk_on_callback(self.psk_on)
        _psk_on_check_box.stateChanged.connect(lambda i: self.set_psk_on(self._psk_on_choices[bool(i)]))
        self.top_grid_layout.addWidget(_psk_on_check_box, 4, 6, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._phase_range = Range(-0.1, 0.1, (0.2)/200, 0, 200)
        self._phase_win = RangeWidget(self._phase_range, self.set_phase, "Phase Correction", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._phase_win, 0, 0, 1, 7)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        _nbfm_on_check_box = Qt.QCheckBox("NBFM")
        self._nbfm_on_choices = {True: True, False: False}
        self._nbfm_on_choices_inv = dict((v,k) for k,v in self._nbfm_on_choices.items())
        self._nbfm_on_callback = lambda i: Qt.QMetaObject.invokeMethod(_nbfm_on_check_box, "setChecked", Qt.Q_ARG("bool", self._nbfm_on_choices_inv[i]))
        self._nbfm_on_callback(self.nbfm_on)
        _nbfm_on_check_box.stateChanged.connect(lambda i: self.set_nbfm_on(self._nbfm_on_choices[bool(i)]))
        self.top_grid_layout.addWidget(_nbfm_on_check_box, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._magnitude_range = Range(-0.1, 0.1, 0.2/200, 0, 200)
        self._magnitude_win = RangeWidget(self._magnitude_range, self.set_magnitude, "Magnitude correction", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._magnitude_win, 1, 0, 1, 7)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        _lsb_on_check_box = Qt.QCheckBox("LSB")
        self._lsb_on_choices = {True: True, False: False}
        self._lsb_on_choices_inv = dict((v,k) for k,v in self._lsb_on_choices.items())
        self._lsb_on_callback = lambda i: Qt.QMetaObject.invokeMethod(_lsb_on_check_box, "setChecked", Qt.Q_ARG("bool", self._lsb_on_choices_inv[i]))
        self._lsb_on_callback(self.lsb_on)
        _lsb_on_check_box.stateChanged.connect(lambda i: self.set_lsb_on(self._lsb_on_choices[bool(i)]))
        self.top_grid_layout.addWidget(_lsb_on_check_box, 4, 3, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._i_offset_range = Range(-0.1, 0.1, ((0.1) - (-0.1))/200, 0, 200)
        self._i_offset_win = RangeWidget(self._i_offset_range, self.set_i_offset, "DC offsett I", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._i_offset_win, 2, 0, 1, 7)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        _cw_on_check_box = Qt.QCheckBox("CW")
        self._cw_on_choices = {True: True, False: False}
        self._cw_on_choices_inv = dict((v,k) for k,v in self._cw_on_choices.items())
        self._cw_on_callback = lambda i: Qt.QMetaObject.invokeMethod(_cw_on_check_box, "setChecked", Qt.Q_ARG("bool", self._cw_on_choices_inv[i]))
        self._cw_on_callback(self.cw_on)
        _cw_on_check_box.stateChanged.connect(lambda i: self.set_cw_on(self._cw_on_choices[bool(i)]))
        self.top_grid_layout.addWidget(_cw_on_check_box, 4, 5, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        _am_on_check_box = Qt.QCheckBox("AM")
        self._am_on_choices = {True: True, False: False}
        self._am_on_choices_inv = dict((v,k) for k,v in self._am_on_choices.items())
        self._am_on_callback = lambda i: Qt.QMetaObject.invokeMethod(_am_on_check_box, "setChecked", Qt.Q_ARG("bool", self._am_on_choices_inv[i]))
        self._am_on_callback(self.am_on)
        _am_on_check_box.stateChanged.connect(lambda i: self.set_am_on(self._am_on_choices[bool(i)]))
        self.top_grid_layout.addWidget(_am_on_check_box, 4, 2, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.root_raised_cosine_filter_1 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                audio_rate,
                5,
                0.35,
                200))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                audio_rate,
                5,
                0.35,
                200))
        self.rational_resampler_xxx_3 = filter.rational_resampler_ccc(
                interpolation=192,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_2 = filter.rational_resampler_ccc(
                interpolation=samp_rate,
                decimation=audio_rate,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate / audio_rate / 2),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate / audio_rate / 4),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Scope Plot', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'FFT Plot', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(gain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.low_pass_filter_1 = filter.interp_fir_filter_ccf(
            1,
            firdes.low_pass(
                0.5,
                audio_rate,
                5000,
                400,
                window.WIN_HAMMING,
                6.76))
        self.iqbalance_fix_cc_0 = iqbalance.fix_cc(magnitude, phase)
        self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=2,
            mod_code="none",
            differential=True,
            samples_per_symbol=8,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_map_bb_0 = digital.map_bb([1,0])
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/warnes/inoui/gnuradio/Audio_Files/multi_tx.wav', True)
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
        self.blocks_add_const_vxx_1 = blocks.add_const_cc(i_offset + 1j * q_offset)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(0.5)
        self.band_pass_filter_0_0 = filter.interp_fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                audio_rate,
                -2800,
                -200,
                200,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.interp_fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                audio_rate,
                200,
                2800,
                200,
                window.WIN_HAMMING,
                6.76))
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=audio_rate,
        	quad_rate=audio_rate * 4,
        	tau=75e-6,
        	max_dev=75e3,
        	fh=-1.0,
        )
        self.analog_sig_source_x_6 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 22000, 1 if psk_on else 0, 0, 0)
        self.analog_sig_source_x_5 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 20000, 1 if cw_on else 0, 0, 0)
        self.analog_sig_source_x_4 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 120000, 1.0 / 7, 0, 0)
        self.analog_sig_source_x_3_0 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 11000, 1.8 if lsb_on else 0, 0, 0)
        self.analog_sig_source_x_3 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 14000, 1.8 if usb_on else 0, 0, 0)
        self.analog_sig_source_x_2 = analog.sig_source_c(audio_rate, analog.GR_COS_WAVE, 0, 1 if am_on else 0, 0, 0)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 0, 1.0 / 7 if wbfm_on else 0, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -100000, 1.0 / 7 if nbfm_on else 0, 0, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=audio_rate,
        	quad_rate=audio_rate * 2,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_nbfm_tx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.analog_sig_source_x_3, 0), (self.blocks_multiply_xx_3, 1))
        self.connect((self.analog_sig_source_x_3_0, 0), (self.blocks_multiply_xx_3_0, 1))
        self.connect((self.analog_sig_source_x_4, 0), (self.blocks_multiply_xx_4, 1))
        self.connect((self.analog_sig_source_x_5, 0), (self.blocks_multiply_xx_5, 1))
        self.connect((self.analog_sig_source_x_6, 0), (self.blocks_multiply_xx_6, 1))
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_xx_3, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_xx_3_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.iqbalance_fix_cc_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.rational_resampler_xxx_2, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_multiply_xx_3, 0), (self.blocks_add_xx_1, 2))
        self.connect((self.blocks_multiply_xx_3_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_multiply_xx_4, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_xx_5, 0), (self.blocks_add_xx_1, 3))
        self.connect((self.blocks_multiply_xx_6, 0), (self.blocks_add_xx_1, 4))
        self.connect((self.blocks_repeat_0, 0), (self.root_raised_cosine_filter_1, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vector_source_x_2, 0), (self.digital_map_bb_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.rational_resampler_xxx_3, 0))
        self.connect((self.iqbalance_fix_cc_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_2, 0), (self.blocks_multiply_xx_4, 0))
        self.connect((self.rational_resampler_xxx_3, 0), (self.blocks_multiply_xx_6, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_multiply_xx_5, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.root_raised_cosine_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "multi_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_samp_rate(self.audio_rate * 40)
        self.analog_sig_source_x_2.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_3.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_3_0.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_5.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_6.set_sampling_freq(self.audio_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, 200, 2800, 200, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.audio_rate, -2800, -200, 200, window.WIN_HAMMING, 6.76))
        self.blocks_repeat_0.set_interpolation(int(1.2 * self.audio_rate / self.wpm))
        self.low_pass_filter_1.set_taps(firdes.low_pass(0.5, self.audio_rate, 5000, 400, window.WIN_HAMMING, 6.76))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.audio_rate, 5, 0.35, 200))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.audio_rate, 5, 0.35, 200))

    def get_wpm(self):
        return self.wpm

    def set_wpm(self, wpm):
        self.wpm = wpm
        self.blocks_repeat_0.set_interpolation(int(1.2 * self.audio_rate / self.wpm))

    def get_wbfm_on(self):
        return self.wbfm_on

    def set_wbfm_on(self, wbfm_on):
        self.wbfm_on = wbfm_on
        self._wbfm_on_callback(self.wbfm_on)
        self.analog_sig_source_x_1.set_amplitude(1.0 / 7 if self.wbfm_on else 0)

    def get_usb_on(self):
        return self.usb_on

    def set_usb_on(self, usb_on):
        self.usb_on = usb_on
        self._usb_on_callback(self.usb_on)
        self.analog_sig_source_x_3.set_amplitude(1.8 if self.usb_on else 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_4.set_sampling_freq(self.samp_rate)
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_q_offset(self):
        return self.q_offset

    def set_q_offset(self, q_offset):
        self.q_offset = q_offset
        self.blocks_add_const_vxx_1.set_k(self.i_offset + 1j * self.q_offset)

    def get_psk_on(self):
        return self.psk_on

    def set_psk_on(self, psk_on):
        self.psk_on = psk_on
        self._psk_on_callback(self.psk_on)
        self.analog_sig_source_x_6.set_amplitude(1 if self.psk_on else 0)

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase
        self.iqbalance_fix_cc_0.set_phase(self.phase)

    def get_nbfm_on(self):
        return self.nbfm_on

    def set_nbfm_on(self, nbfm_on):
        self.nbfm_on = nbfm_on
        self._nbfm_on_callback(self.nbfm_on)
        self.analog_sig_source_x_0.set_amplitude(1.0 / 7 if self.nbfm_on else 0)

    def get_magnitude(self):
        return self.magnitude

    def set_magnitude(self, magnitude):
        self.magnitude = magnitude
        self.iqbalance_fix_cc_0.set_mag(self.magnitude)

    def get_lsb_on(self):
        return self.lsb_on

    def set_lsb_on(self, lsb_on):
        self.lsb_on = lsb_on
        self._lsb_on_callback(self.lsb_on)
        self.analog_sig_source_x_3_0.set_amplitude(1.8 if self.lsb_on else 0)

    def get_i_offset(self):
        return self.i_offset

    def set_i_offset(self, i_offset):
        self.i_offset = i_offset
        self.blocks_add_const_vxx_1.set_k(self.i_offset + 1j * self.q_offset)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_sink_0.set_gain(self.gain, 0)

    def get_cw_on(self):
        return self.cw_on

    def set_cw_on(self, cw_on):
        self.cw_on = cw_on
        self._cw_on_callback(self.cw_on)
        self.analog_sig_source_x_5.set_amplitude(1 if self.cw_on else 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)

    def get_am_on(self):
        return self.am_on

    def set_am_on(self, am_on):
        self.am_on = am_on
        self._am_on_callback(self.am_on)
        self.analog_sig_source_x_2.set_amplitude(1 if self.am_on else 0)




def main(top_block_cls=multi_tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
