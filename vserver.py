from socket import *
import struct
import time

stop = True
nrec = 0

sock = socket(AF_INET, SOCK_STREAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

sock.bind(('', 1055))
sock.listen(128)
try:
    while True:
        client, addr = sock.accept()
        data = client.recv(4096)
        vdata = ''
        if data != '':
            if 'G' == data[0]:
                while True:
                    if '\n' in data:
                        break
                    else:
                        data += client.recv(4096)
                try:
                    vfile = open(data[1:-1], 'rb')
                    vdata = ''
                    while True:
                        buf = vfile.read()
                        if buf == '':
                            break
                        else:
                            vdata += buf
                except Exception:
                    pass
        vdata = struct.pack('>I', len(vdata)) + vdata
        sent = 0
        while sent < len(vdata):
            send = 8192
            if send + sent > len(vdata):
                send = len(vdata) - sent
            client.sendall(vdata[sent:sent+send])
            sent += send
            if stop and nrec > 2 and nrec < 7:
                print("sleep")
                time.sleep(0.7)
        print("out")
        nrec += 1
        client.close()
except KeyboardInterrupt:
    pass

sock.close()
