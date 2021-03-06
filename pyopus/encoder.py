# -*- coding: utf-8 -*-

'''Opus encoder.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'OpusEncoder',
        'FloatOpusEncoder',
        ]

from threading import Lock

from . import base
from . import binding
from . import llinterface
from . import ctl
from . import utils

# slightly larger than the recommended size of 4000 bytes, which is OK
PAYLOAD_BUFFER_SIZE = 4096


class BaseOpusEncoder(base.OpusCodec):
    '''Opus encoder.'''

    _encoder_fn = None

    def __init__(self, frequency, channels, application):
        # basic sanity check
        utils.check_freq(frequency)
        utils.check_channels(channels)
        utils.check_application(application)

        self._freq = frequency
        self._channels = channels
        self._mode = application

        # dispatch to encode functions with different sanity checking,
        # based on channel count
        self.encode = (
                self._stereo_encode
                if channels == 2
                else self._mono_encode
                )

        # initialize state
        super(BaseOpusEncoder, self).__init__()

        # output payload buffer
        # Since the codec is stateful, allowing reentrancy is pointless.
        # Just make one output buffer to avoid repeated memory allocations
        # (and deallocations), and lock it properly.
        self._out = binding.ffi.new('char[]', PAYLOAD_BUFFER_SIZE)
        self._buf = binding.ffi.buffer(self._out)
        self._buf_lock = Lock()

    def _get_state_size(self):
        return llinterface.encoder_get_size(self._channels)

    def _init_state(self):
        llinterface.encoder_init(
                self._state,
                self._freq,
                self._channels,
                self._mode,
                )

    def _stereo_encode(self, pcm):
        # basic frame-size check
        frame_size, rem = divmod(len(pcm), 2)
        if rem != 0:
            raise ValueError('PCM data length is not even for stereo input')

        return self._do_encode(pcm, frame_size)

    def _mono_encode(self, pcm):
        return self._do_encode(pcm, len(pcm))

    def _do_encode(self, pcm, frame_size):
        with self._buf_lock:
            len_payload = self._encoder_fn(
                    self._state,
                    pcm,
                    frame_size,
                    self._out,
                    PAYLOAD_BUFFER_SIZE,
                    )
            return self._buf[:len_payload]

    # Generic CTLs
    def reset_state(self):
        ctl.encoder_reset_state(self._state)

    @property
    def final_range(self):
        return ctl.encoder_get_final_range(self._state)

    @property
    def pitch(self):
        return ctl.encoder_get_pitch(self._state)

    @property
    def bandwidth(self):
        return ctl.encoder_get_bandwidth(self._state)

    # Encoder CTLs
    @bandwidth.setter
    def bandwidth(self, value):
        ctl.encoder_set_bandwidth(self._state, value)

    @property
    def complexity(self):
        return ctl.encoder_get_complexity(self._state)

    @complexity.setter
    def complexity(self, value):
        ctl.encoder_set_complexity(self._state, value)

    @property
    def bitrate(self):
        return ctl.encoder_get_bitrate(self._state)

    @bitrate.setter
    def bitrate(self, value):
        ctl.encoder_set_bitrate(self._state, value)

    @property
    def vbr(self):
        return ctl.encoder_get_vbr(self._state)

    @vbr.setter
    def vbr(self, value):
        ctl.encoder_set_vbr(self._state, value)

    @property
    def vbr_constraint(self):
        return ctl.encoder_get_vbr_constraint(self._state)

    @vbr_constraint.setter
    def vbr_constraint(self, value):
        ctl.encoder_set_vbr_constraint(self._state, value)

    @property
    def force_channels(self):
        return ctl.encoder_get_force_channels(self._state)

    @force_channels.setter
    def force_channels(self, value):
        ctl.encoder_set_force_channels(self._state, value)

    @property
    def max_bandwidth(self):
        return ctl.encoder_get_max_bandwidth(self._state)

    @max_bandwidth.setter
    def max_bandwidth(self, value):
        ctl.encoder_set_max_bandwidth(self._state, value)

    @property
    def signal(self):
        return ctl.encoder_get_signal(self._state)

    @signal.setter
    def signal(self, value):
        ctl.encoder_set_signal(self._state, value)

    @property
    def application(self):
        return ctl.encoder_get_application(self._state)

    @application.setter
    def application(self, value):
        ctl.encoder_set_application(self._state, value)

    @property
    def sample_rate(self):
        # XXX This is really just the frequency specified in the ctor...
        # Should the CTL request be completely removed?
        return ctl.encoder_get_sample_rate(self._state)

    @property
    def lookahead(self):
        return ctl.encoder_get_lookahead(self._state)

    @property
    def inband_fec(self):
        return ctl.encoder_get_inband_fec(self._state)

    @inband_fec.setter
    def inband_fec(self, value):
        ctl.encoder_set_inband_fec(self._state, value)

    @property
    def packet_loss_perc(self):
        return ctl.encoder_get_packet_loss_perc(self._state)

    @packet_loss_perc.setter
    def packet_loss_perc(self, value):
        ctl.encoder_set_packet_loss_perc(self._state, value)

    @property
    def dtx(self):
        return ctl.encoder_get_dtx(self._state)

    @dtx.setter
    def dtx(self, value):
        ctl.encoder_set_dtx(self._state, value)

    @property
    def lsb_depth(self):
        return ctl.encoder_get_lsb_depth(self._state)

    @lsb_depth.setter
    def lsb_depth(self, value):
        ctl.encoder_set_lsb_depth(self._state, value)

    @property
    def last_packet_duration(self):
        return ctl.encoder_get_last_packet_duration(self._state)

    @property
    def expert_frame_duration(self):
        return ctl.encoder_get_expert_frame_duration(self._state)

    @expert_frame_duration.setter
    def expert_frame_duration(self, value):
        ctl.encoder_set_expert_frame_duration(self._state, value)

    @property
    def prediction_disabled(self):
        return ctl.encoder_get_prediction_disabled(self._state)

    @prediction_disabled.setter
    def prediction_disabled(self, value):
        ctl.encoder_set_prediction_disabled(self._state, value)


class OpusEncoder(BaseOpusEncoder):
    _encoder_fn = staticmethod(llinterface.encode)


class FloatOpusEncoder(BaseOpusEncoder):
    _encoder_fn = staticmethod(llinterface.encode_float)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
