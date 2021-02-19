import wave
import sys
import streamlit as st
import time

st.title("Audio Steganography.")
st.markdown("Select an audio file to get started! 🎵")

def encode(sound, data, name):
	parameters = sound.getparams()
	frame_bytes = bytearray(list(sound.readframes(sound.getnframes())))
	encoding, data_bits = '', []
	if len(data * 8 * 8) > len(frame_bytes):
		print("Cannot encode...")
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
		st.markdown(f"Successfully hid your message! File saved as `encoded_{name}`")
		encoded_sound.close()

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

if __name__=="__main__": 
	steg_option = st.radio("Choose steganography option: ", ("Encode", "Decode"))
	if steg_option == "Encode":
		encode_audio = st.file_uploader("Choose an audio file to encode with secret message:")
		if encode_audio:
			file_name = encode_audio.name
			encode_audio = wave.open(encode_audio, mode ='rb')
			encode_option = st.radio("Choose data to be encoded: ", ("Type manually", "Upload file"))
			if encode_option == "Type manually":
				encode_text = st.text_area("Type something...")
			elif encode_option == "Upload file":
				try:
					encode_text = st.file_uploader("Choose a text file containing the secret message:")
					encode_text = str(encode_text.read())
				except:
					pass
			if encode_text:
				encode(encode_audio, encode_text, file_name)
				encode_audio.close()
	elif steg_option == "Decode":
		decode_audio = st.file_uploader("Choose an audio file to be decoded:")
		if decode_audio:
			file_name = decode_audio.name
			decode_audio = wave.open(decode_audio, mode ='rb')
			decoded_text = decode(decode_audio)
			decode_audio.close()
			if decoded_text:
				st.subheader("Sucessfully retrieved the hidden message: ")
				st.markdown(str(decoded_text))