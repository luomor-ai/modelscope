# Copyright (c) Alibaba, Inc. and its affiliates.
import re
import struct
import sys
from typing import Union
from urllib.parse import urlparse

import numpy as np

from modelscope.fileio.file import HTTPStorage

SEGMENT_LENGTH_TRAIN = 16000


class TtsTrainType(object):
    TRAIN_TYPE_SAMBERT = 'train-type-sambert'
    TRAIN_TYPE_BERT = 'train-type-bert'
    TRAIN_TYPE_VOC = 'train-type-voc'


def to_segment(batch, segment_length=SEGMENT_LENGTH_TRAIN):
    """
    Dataset mapping function to split one audio into segments.
    It only works in batch mode.
    """
    noisy_arrays = []
    clean_arrays = []
    for x, y in zip(batch['noisy'], batch['clean']):
        length = min(len(x['array']), len(y['array']))
        noisy = x['array']
        clean = y['array']
        for offset in range(segment_length, length + 1, segment_length):
            noisy_arrays.append(noisy[offset - segment_length:offset])
            clean_arrays.append(clean[offset - segment_length:offset])
    return {'noisy': noisy_arrays, 'clean': clean_arrays}


def audio_norm(x):
    rms = (x**2).mean()**0.5
    scalar = 10**(-25 / 20) / rms
    x = x * scalar
    pow_x = x**2
    avg_pow_x = pow_x.mean()
    rmsx = pow_x[pow_x > avg_pow_x].mean()**0.5
    scalarx = 10**(-25 / 20) / rmsx
    x = x * scalarx
    return x


def update_conf(origin_config_file, new_config_file, conf_item: [str, str]):

    def repl(matched):
        key = matched.group(1)
        if key in conf_item:
            value = conf_item[key]
            if not isinstance(value, str):
                value = str(value)
            return value
        else:
            return None

    with open(origin_config_file, encoding='utf-8') as f:
        lines = f.readlines()
    with open(new_config_file, 'w') as f:
        for line in lines:
            line = re.sub(r'\$\{(.*)\}', repl, line)
            f.write(line)


def extract_pcm_from_wav(wav: bytes) -> bytes:
    data = wav
    sample_rate = None
    if len(data) > 44:
        frame_len = 44
        file_len = len(data)
        try:
            header_fields = {}
            header_fields['ChunkID'] = str(data[0:4], 'UTF-8')
            header_fields['Format'] = str(data[8:12], 'UTF-8')
            header_fields['Subchunk1ID'] = str(data[12:16], 'UTF-8')
            if header_fields['ChunkID'] == 'RIFF' and header_fields[
                    'Format'] == 'WAVE' and header_fields[
                        'Subchunk1ID'] == 'fmt ':
                header_fields['SubChunk1Size'] = struct.unpack(
                    '<I', data[16:20])[0]
                header_fields['SampleRate'] = struct.unpack('<I',
                                                            data[24:28])[0]
                sample_rate = header_fields['SampleRate']

                if header_fields['SubChunk1Size'] == 16:
                    frame_len = 44
                elif header_fields['SubChunk1Size'] == 18:
                    frame_len = 46
                else:
                    return data, sample_rate

                data = wav[frame_len:file_len]
        except Exception:
            # no treatment
            pass

    return data, sample_rate


# This implementation is adopted from scipy.io.wavfile.write,
# made publicly available under the BSD-3-Clause license at
# https://github.com/scipy/scipy/blob/v1.9.3/scipy/io/wavfile.py
def ndarray_pcm_to_wav(fs: int, data: np.ndarray) -> bytes:
    dkind = data.dtype.kind
    if not (dkind == 'i' or dkind == 'f' or  # noqa W504
            (dkind == 'u' and data.dtype.itemsize == 1)):
        raise ValueError(f'Unsupported data type {data.dtype}')

    header_data = bytearray()
    header_data += b'RIFF'
    header_data += b'\x00\x00\x00\x00'
    header_data += b'WAVE'
    header_data += b'fmt '
    if dkind == 'f':
        format_tag = 0x0003
    else:
        format_tag = 0x0001
    if data.ndim == 1:
        channels = 1
    else:
        channels = data.shape[1]
    bit_depth = data.dtype.itemsize * 8
    bytes_per_second = fs * (bit_depth // 8) * channels
    block_align = channels * (bit_depth // 8)

    fmt_chunk_data = struct.pack('<HHIIHH', format_tag, channels, fs,
                                 bytes_per_second, block_align, bit_depth)
    if not (dkind == 'i' or dkind == 'u'):
        fmt_chunk_data += b'\x00\x00'
    header_data += struct.pack('<I', len(fmt_chunk_data))
    header_data += fmt_chunk_data

    if not (dkind == 'i' or dkind == 'u'):
        header_data += b'fact'
        header_data += struct.pack('<II', 4, data.shape[0])

    if ((len(header_data) - 8) + (8 + data.nbytes)) > 0xFFFFFFFF:
        raise ValueError('Data exceeds wave file size limit')

    header_data += b'data'
    header_data += struct.pack('<I', data.nbytes)
    if data.dtype.byteorder == '>' or (data.dtype.byteorder == '='
                                       and sys.byteorder == 'big'):
        data = data.byteswap()
    header_data += data.ravel().view('b').data
    size = len(header_data)
    header_data[4:8] = struct.pack('<I', size - 8)
    return bytes(header_data)


def load_bytes_from_url(url: str) -> Union[bytes, str]:
    sample_rate = None
    result = urlparse(url)
    if result.scheme is not None and len(result.scheme) > 0:
        storage = HTTPStorage()
        data = storage.read(url)
        data, sample_rate = extract_pcm_from_wav(data)
    else:
        data = url

    return data, sample_rate
