'''
import wave , getopt , sys
from struct import  *

def preprocess(wav_file):
    global sound , numberOfFrames , parameter , format , mask
    sound = wave.open(wav_file, "r")
    parameter = sound.getparams()
    numberOfChannels = sound.getnchannels()
    numberOfFrames = sound.getnframes()  # to how many pieces audio file is splat
    sampleWidth = sound.getsampwidth()
    numberOfSamples = numberOfFrames * numberOfChannels

    if (sampleWidth == 1):
        format = "{}B".format(numberOfSamples)  # changes into string
        mask = 252
    elif (sampleWidth == 2):
        format = "{}h".format(numberOfSamples)  # format is to tell me how i ll unpack audio file
        mask = 32764
    else:
        raise ValueError("Audio width is too high")

    #print(sound, numberOfChannels, numberOfFrames,mask, format)


def hide(wavName, text, resultFile):
    preprocess(wavName)
    maxByteToHide = (numberOfFrames * 2) // 8  # max bytes to hide

    rawData = list(unpack(format, sound.readframes(numberOfFrames)))  # frames in binary
    #rawData = bytearray(list(sound.readframes(sound.getnframes())))
    sound.close()
    textRawData = memoryview(open(text, "rb").read())  ## read text into tytes
    print(rawData[0:10])
    
    firstVaues = []
    indexOfText = 0
    buferLen = 0
    bufer = 0
    soundindex = 0

    while (indexOfText < len(textRawData)):  # incrementing lists index of the text

        while (buferLen < 2):  # every time bufer len drops below 2 move to the next letter
            bufer = textRawData[indexOfText]
            indexOfText += 1
            buferLen += 8

        currentData = bufer % (1 << 2)  # bytes from text file extracted backwards for each letter
        bufer >>= 2
        buferLen -= 2

        currentSample = rawData[soundindex]
        soundindex += 1

        sign = 1
        if (currentSample < 0):
            currentSample = - currentSample
            sign = -1

        changedSample = sign * (currentSample & mask) | currentData

        tempValue = pack(format[-1], changedSample)
        firstVaues.append(tempValue)

    while (indexOfText < len(rawData)):
        tempValue = pack(format[-1], rawData[indexOfText])
        firstVaues.append(tempValue)
        indexOfText += 1

    resultAudio = wave.open(resultFile, "w")
    resultAudio.setparams(parameter)
    resultAudio.writeframesraw(b"".join(firstVaues))
    resultAudio.close()
    print("data hidden")

hide('music.wav', 'data.txt', 'new.wav')
'''
'''
import wave
# read wave audio file
song = wave.open("music.wav", mode='rb')
# Read frames and convert to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# The "secret" text message
string='Peter Parker is the Spiderman!'
# Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.
string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
# Convert text to bit array
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
print(bits)

# Replace LSB of each byte of the audio data by one bit from the text bit array
for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
# Get the modified bytes
frame_modified = bytes(frame_bytes)

# Write bytes to a new wave audio file
with wave.open('song_embedded.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()
'''

'''
import wave
song = wave.open("encoded.wav", mode='rb')
# Convert audio to byte array
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Extract the LSB of each byte
extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
# Convert byte array back to string
string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# Cut off at the filler characters
decoded = string.split("___")[0]

# Print the extracted text
print("Sucessfully decoded: "+decoded)
song.close()

'''

import wave
import sys

def encode(sound, data, parameters):
    frame_bytes = bytearray(list(sound.readframes(sound.getnframes())))
    encoding, data_bits = '', []
    if len(data * 8 * 8) > len(frame_bytes):
        print("Cannot encode....")
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

        encoded_sound = wave.open('encoded.wav', 'wb')
        encoded_sound.setparams(parameters)
        encoded_sound.writeframes(frame_bytes)
        encoded_sound.close()

        print("Encoding completed successfully")
        


if __name__=="__main__": 
    file = open('data.txt', 'r') 
    data = file.read()
    file.close()

    sound = wave.open("music.wav", mode='rb')
    parameters = sound.getparams()
    encode(sound, data, parameters)
    sound.close()
    