# -*- coding: utf-8 -*-

'''libopus CFFI binding.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'ffi',
        'C',
        ]

import cffi

ffi = cffi.FFI()
ffi.cdef('''
/* opus_types.h */
typedef short opus_int16;
typedef unsigned short opus_uint16;
typedef int opus_int32;
typedef unsigned int opus_uint32;

typedef int opus_int;
typedef long long opus_int64;
typedef signed char opus_int8;

typedef unsigned int opus_uint;
typedef unsigned long long opus_uint64;
typedef unsigned char opus_uint8;


/* opus_defines.h */
#define OPUS_OK ...
#define OPUS_BAD_ARG ...
#define OPUS_BUFFER_TOO_SMALL ...
#define OPUS_INTERNAL_ERROR ...
#define OPUS_INVALID_PACKET ...
#define OPUS_UNIMPLEMENTED ...
#define OPUS_INVALID_STATE ...
#define OPUS_ALLOC_FAIL ...

#define OPUS_SET_APPLICATION_REQUEST ...
#define OPUS_GET_APPLICATION_REQUEST ...
#define OPUS_SET_BITRATE_REQUEST ...
#define OPUS_GET_BITRATE_REQUEST ...
#define OPUS_SET_MAX_BANDWIDTH_REQUEST ...
#define OPUS_GET_MAX_BANDWIDTH_REQUEST ...
#define OPUS_SET_VBR_REQUEST ...
#define OPUS_GET_VBR_REQUEST ...
#define OPUS_SET_BANDWIDTH_REQUEST ...
#define OPUS_GET_BANDWIDTH_REQUEST ...
#define OPUS_SET_COMPLEXITY_REQUEST ...
#define OPUS_GET_COMPLEXITY_REQUEST ...
#define OPUS_SET_INBAND_FEC_REQUEST ...
#define OPUS_GET_INBAND_FEC_REQUEST ...
#define OPUS_SET_PACKET_LOSS_PERC_REQUEST ...
#define OPUS_GET_PACKET_LOSS_PERC_REQUEST ...
#define OPUS_SET_DTX_REQUEST ...
#define OPUS_GET_DTX_REQUEST ...
#define OPUS_SET_VBR_CONSTRAINT_REQUEST ...
#define OPUS_GET_VBR_CONSTRAINT_REQUEST ...
#define OPUS_SET_FORCE_CHANNELS_REQUEST ...
#define OPUS_GET_FORCE_CHANNELS_REQUEST ...
#define OPUS_SET_SIGNAL_REQUEST ...
#define OPUS_GET_SIGNAL_REQUEST ...
#define OPUS_GET_LOOKAHEAD_REQUEST ...
#define OPUS_GET_SAMPLE_RATE_REQUEST ...
#define OPUS_GET_FINAL_RANGE_REQUEST ...
#define OPUS_GET_PITCH_REQUEST ...
#define OPUS_SET_GAIN_REQUEST ...
#define OPUS_GET_GAIN_REQUEST ...
#define OPUS_SET_LSB_DEPTH_REQUEST ...
#define OPUS_GET_LSB_DEPTH_REQUEST ...
#define OPUS_GET_LAST_PACKET_DURATION_REQUEST ...
#define OPUS_SET_EXPERT_FRAME_DURATION_REQUEST ...
#define OPUS_GET_EXPERT_FRAME_DURATION_REQUEST ...
#define OPUS_SET_PREDICTION_DISABLED_REQUEST ...
#define OPUS_GET_PREDICTION_DISABLED_REQUEST ...

#define OPUS_AUTO ...
#define OPUS_BITRATE_MAX ...

#define OPUS_APPLICATION_VOIP ...
#define OPUS_APPLICATION_AUDIO ...
#define OPUS_APPLICATION_RESTRICTED_LOWDELAY ...

#define OPUS_SIGNAL_VOICE ...
#define OPUS_SIGNAL_MUSIC ...
#define OPUS_BANDWIDTH_NARROWBAND ...
#define OPUS_BANDWIDTH_MEDIUMBAND ...
#define OPUS_BANDWIDTH_WIDEBAND ...
#define OPUS_BANDWIDTH_SUPERWIDEBAND ...
#define OPUS_BANDWIDTH_FULLBAND ...

#define OPUS_FRAMESIZE_ARG ...
#define OPUS_FRAMESIZE_2_5_MS ...
#define OPUS_FRAMESIZE_5_MS ...
#define OPUS_FRAMESIZE_10_MS ...
#define OPUS_FRAMESIZE_20_MS ...
#define OPUS_FRAMESIZE_40_MS ...
#define OPUS_FRAMESIZE_60_MS ...

const char *opus_strerror(int error);
const char *opus_get_version_string(void);


/* opus.h */
typedef ... OpusEncoder;

int opus_encoder_get_size(int channels);
OpusEncoder *opus_encoder_create(opus_int32 Fs, int channels, int application, int *error);
int opus_encoder_init(OpusEncoder *st, opus_int32 Fs, int channels, int application);
opus_int32 opus_encode(OpusEncoder *st, const opus_int16 *pcm, int frame_size, unsigned char *data, opus_int32 max_data_bytes);
opus_int32 opus_encode_float(OpusEncoder *st, const float *pcm, int frame_size, unsigned char *data, opus_int32 max_data_bytes);
void opus_encoder_destroy(OpusEncoder *st);
int opus_encoder_ctl(OpusEncoder *st, int request, ...);

typedef ... OpusDecoder;

int opus_decoder_get_size(int channels);
OpusDecoder *opus_decoder_create(opus_int32 Fs, int channels, int *error);
int opus_decoder_init(OpusDecoder *st, opus_int32 Fs, int channels);
int opus_decode(OpusDecoder *st, const unsigned char *data, opus_int32 len, opus_int16 *pcm, int frame_size, int decode_fec);
int opus_decode_float(OpusDecoder *st, const unsigned char *data, opus_int32 len, float *pcm, int frame_size, int decode_fec);
int opus_decoder_ctl(OpusDecoder *st, int request, ...);
void opus_decoder_destroy(OpusDecoder *st);

int opus_packet_parse(const unsigned char *data, opus_int32 len, unsigned char *out_toc, const unsigned char *frames[48], opus_int16 size[48], int *payload_offset);
int opus_packet_get_bandwidth(const unsigned char *data);
int opus_packet_get_samples_per_frame(const unsigned char *data, opus_int32 Fs);
int opus_packet_get_nb_channels(const unsigned char *data);
int opus_packet_get_nb_frames(const unsigned char packet[], opus_int32 len);
int opus_packet_get_nb_samples(const unsigned char packet[], opus_int32 len, opus_int32 Fs);
int opus_decoder_get_nb_samples(const OpusDecoder *dec, const unsigned char packet[], opus_int32 len);
void opus_pcm_soft_clip(float *pcm, int frame_size, int channels, float *softclip_mem);

typedef ... OpusRepacketizer;

int opus_repacketizer_get_size(void);
OpusRepacketizer *opus_repacketizer_init(OpusRepacketizer *rp);
OpusRepacketizer *opus_repacketizer_create(void);
void opus_repacketizer_destroy(OpusRepacketizer *rp);
int opus_repacketizer_cat(OpusRepacketizer *rp, const unsigned char *data, opus_int32 len);
opus_int32 opus_repacketizer_out_range(OpusRepacketizer *rp, int begin, int end, unsigned char *data, opus_int32 maxlen);
int opus_repacketizer_get_nb_frames(OpusRepacketizer *rp);
opus_int32 opus_repacketizer_out(OpusRepacketizer *rp, unsigned char *data, opus_int32 maxlen);
int opus_packet_pad(unsigned char *data, opus_int32 len, opus_int32 new_len);
opus_int32 opus_packet_unpad(unsigned char *data, opus_int32 len);
int opus_multistream_packet_pad(unsigned char *data, opus_int32 len, opus_int32 new_len, int nb_streams);
opus_int32 opus_multistream_packet_unpad(unsigned char *data, opus_int32 len, int nb_streams);
''')

C = ffi.verify('''
#include <opus/opus.h>
''', libraries=[str('opus')])


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
