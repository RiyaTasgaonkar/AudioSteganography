import wave
import sys

def decode(sound, parameter):
    frame_bytes = bytearray(list(sound.readframes(sound.getnframes())))
    extracted_bits, data = '', ''

    for i in range(len(frame_bytes)):
        extracted_bits = extracted_bits + str(frame_bytes[i] & 1)
    
    for i in range(0, len(extracted_bits), 8):
        byte = extracted_bits[i : i + 8]
        character = chr(int(byte, 2))
        data = data + character
    
    data = data.split("___")[0]
    print("Sucessfully decoded: "+ data)

if __name__=="__main__": 
    
    sound = wave.open("encoded.wav", mode='rb')
    parameters = sound.getparams()
    decode(sound, parameters)
    sound.close()