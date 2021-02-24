
Audio Steganography
============

[![](https://img.shields.io/badge/Made_with-Python3-blue?style=for-the-badge&logo=python)]()
[![](https://img.shields.io/badge/Made_with-streamlit-red?style=for-the-badge&logo=streamlit)]()

Enables a sender to secretly send their data, hidden within a song.

### LSB (Least Significant Bit) Algorithm:

LSB algorithm is a classic Steganography method used to conceal the existence of secret data inside a "public" cover. The LSB or "Least Significant Bit", in computing terms, represents the bit at the unit’s place in the binary representation of a number.

In the simplistic form, LSB algorithm replaces the LSB of each byte in the "carrier" data with one bit from the "secret" message. 

![embed](https://miro.medium.com/max/1050/1*THFuhBPeMI5lE4JiLcF-OQ.png)

The sender performs "embedding" of the bits of secret messages onto the carrier data byte-by-byte. Whereas the receiver performs the "extraction" procedure by reading LSB bits of each byte of received data, this way the receiver reconstructs the secret message.

![extract](https://miro.medium.com/max/1050/1*7ElCrXNicOSyqXdD9XMy3w.png)

**Note:** We can embed any text, document, audio, video within the carrier audio by simply encoding bits of the secret data within each byte of carrier audio. However, the carrier message has to have enough data bytes so as to carry all the bits of the secret message. 