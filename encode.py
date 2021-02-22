import wave
import sys

def encode(sound, data, name):
    parameters = sound.getparams()
    frame_bytes = bytearray(list(sound.readframes(sound.getnframes())))
    encoding, data_bits, status = '', [], True
    if len(data * 8 * 8) > len(frame_bytes):
        status = False
    else:
        extra_bytes = int((len(frame_bytes)-(len(data) * 8 * 8)) / 8)
        data = data + extra_bytes *'_'
        for i in data:
            data_bit = bin(ord(i)).lstrip('08b').zfill(8)
            encoding = encoding + data_bit
        data_bits = list(map(int, encoding))
        for i, data_bit in enumerate(data_bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | data_bit
        frame_bytes = bytes(frame_bytes)
        encoded_sound = wave.open(f'encoded_{name}', 'wb')
        encoded_sound.setparams(parameters)
        encoded_sound.writeframes(frame_bytes)
        encoded_sound.close()
    return status
