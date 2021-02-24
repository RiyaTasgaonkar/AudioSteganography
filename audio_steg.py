import wave
import sys
import streamlit as st
import time
import encode
import decode

st.title("Audio Steganography.")
st.markdown("Select an audio file to get started! 🎵")

if __name__=="__main__": 

	st.sidebar.subheader("Algorithm used: LSB")
	st.sidebar.markdown("This algorithm replaces the LSB (Least Significant Bit) of each byte in the _carrier_ data with one bit from the _secret_ message.")
	st.sidebar.markdown("The sender performs _embedding_ of the bits of secret messages onto the carrier data byte-by-byte. The receiver performs the _extraction_ procedure by reading LSB bits of each byte of received data.")
	st.sidebar.markdown("[![](https://img.shields.io/badge/Made_with-Python3-blue?style=for-the-badge&logo=python)]() [![](https://img.shields.io/badge/Made_with-streamlit-red?style=for-the-badge&logo=streamlit)]()")
	st.sidebar.markdown("Made by: [Soumya Parekh (1811106)](https://github.com/rubyruins) and [Riya Tasgaonkar (1811122)](https://github.com/RiyaTasgaonkar)")

	steg_option = st.radio("Choose steganography option: ", ("Encode", "Decode"))
	if steg_option == "Encode":
		encode_audio = st.file_uploader("Choose an audio file to encode with secret message:", type = ['wav'])
		if encode_audio:
			file_name = encode_audio.name
			try:
				encode_audio = wave.open(encode_audio, mode ='rb')
				encode_option = st.radio("Choose data to be encoded: ", ("Type manually", "Upload file"))

				if encode_option == "Type manually":
					encode_text = st.text_area("Type something...")
				
				elif encode_option == "Upload file":
					try:
						encode_text = st.file_uploader("Choose a text file containing the secret message:", type = ['txt'])
						encode_text = str(encode_text.read())
					except:
						pass
				if encode_text:
					status = encode.encode(encode_audio, encode_text, file_name)
					if status:
						st.markdown(f"Successfully hid your message! File saved as `encoded_{file_name}`")
					else:
						st.markdown(f"Cannot encode. Text size exceeds file size.")
					encode_audio.close()
			except:
				st.markdown(f"Oops!! Something went wrong.")
				st.markdown(f"Please try again later.")

	elif steg_option == "Decode":
		
		decode_audio = st.file_uploader("Choose an audio file to be decoded:", type = ['wav'])
		try:
			if decode_audio:
				file_name = decode_audio.name
				decode_audio = wave.open(decode_audio, mode ='rb')
				decoded_text = decode.decode(decode_audio)
				decode_audio.close()
				
				if decoded_text:
					st.subheader("Sucessfully retrieved the hidden message: ")
					st.markdown(str(decoded_text))
		except:
				st.markdown(f"Oops!! Something went wrong.")
				st.markdown(f"Please try again later.")