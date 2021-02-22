import wave
import sys

def decode(sound):
	parameters = sound.getparams()
	frame_bytes = bytearray(list(sound.readframes(sound.getnframes())))
	extracted_bits, data = '', ''
	for i in range(len(frame_bytes)):
		extracted_bits = extracted_bits + str(frame_bytes[i] & 1)
	for i in range(0, len(extracted_bits), 8):
		byte = extracted_bits[i : i + 8]
		character = chr(int(byte, 2))
		data = data + character
	data = data.split("___")[0]
	return data