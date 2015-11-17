import sys
wav_in = open('music_encoded.wav', 'rb')
gif_out = open('out.gif', 'wb')

wav_in.seek(44, 0)
image = False
while True:
    enc_byte = wav_in.read(8 * 2)
    if len(enc_byte) == 0:
        break
    byte_value = 0
    for i in range(0, 8 * 2, 2):
        byte_value += (enc_byte[i] & 1) << (7 - int(i/2))
    if not image:
        sys.stdout.write(chr(byte_value))
    else:
        gif_out.write(byte_value.to_bytes(1, 'little'))
    if byte_value == 0:
        image = True
sys.stdout.write('\n')
