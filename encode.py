#!/usr/bin/python

def read_two_bytes(in_file):
    return int.from_bytes(in_file.read(2), 'little')

image = open('image.gif', 'rb')
im_size = image.seek(0, 2)
im_bits = ""
image.seek(0, 0)
while True:
    im_byte = image.read(1)
    if len(im_byte) == 0:
        break
    im_bin_str = bin(int.from_bytes(im_byte, 'little'))[2:]
    im_bin_str_len = len(im_bin_str)
    im_bits += '0' * (8 - im_bin_str_len) + im_bin_str

message = "Parabens! Agora faca o mesmo procedimento usando %d bytes a partir do final dessa mensagem, porem salve-os em um arquivo .gif\0" % im_size
message_bits = ""

for char in message:
    bin_str = bin(ord(char))[2:]
    bin_str_len = len(bin_str)
    message_bits += '0' * (8 - bin_str_len) + bin_str

print("Ecoded size %d" % (len(message_bits) + len(im_bits)))

wav_in = open('music.wav', 'rb')
wav_out = open('music_encoded.wav', 'wb')

wav_in.seek(20, 0) # AudioFormat
if read_two_bytes(wav_in) != 1:
    raise Exception("Cannot handle no PCM file")
wav_in.seek(34, 0) # BitsPerSample
if read_two_bytes(wav_in) != 16:
    raise Exception("Can only handle 16 bit encoding")
wav_in.seek(40, 0)
data_size = int.from_bytes(wav_in.read(4), 'little')
n_samples = int(data_size / 2)

wav_in.seek(0, 0)
header = bytearray(wav_in.read(44))
chunk_size = 36 + 2 * len(im_bits) + 2 * len(message_bits)
header[4:8] = chunk_size.to_bytes(4, 'little')
subchunk2_size = 2 * len(im_bits) + 2 * len(message_bits)
header[40:44] = subchunk2_size.to_bytes(4, 'little')
wav_out.write(header)

wav_in.seek(38 * 44100 * 4, 0)

for i in range(n_samples):
    b1 = int.from_bytes(wav_in.read(1), 'little')
    b2 = int.from_bytes(wav_in.read(1), 'little')
    if b2 & 0b10000000 != 0:
        sample = (b2 ^ 0b11111111) << 8
        sample += (b1 ^ 0b11111111)
    else:
        sample = b2 << 8
        sample += b1
    if i < len(message_bits):
        if int(message_bits[i]):
            b1_out = b1 | 0b1
        else:
            b1_out = b1 & 0b0
    elif i - len(message_bits) < len(im_bits):
        if int(im_bits[i-len(message_bits)]):
            b1_out = b1 | 0b1
        else:
            b1_out = b1 & 0b0
    else:
        break
    b2_out = b2
    wav_out.write(bytes([b1_out, b2_out]))
