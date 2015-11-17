from Queue import Queue
import cv
from threading import Thread
from tempfile import NamedTemporaryFile
from socket import *
import struct

to_play = Queue(1)

class MThread(Thread):
    def __init__(self, to_play):
        Thread.__init__(self)
        self.to_play = to_play
        self.start()

    def run(self):
        for i in range(10):
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(('127.0.0.1', 1055))
            sock.sendall('Gvideot' + str(1) + str(i) + '.mp4\n')

            data = sock.recv(4)
            while len(data) < 4:
                data += sock.recv(4)
            size = struct.unpack('>I', data[:4])[0]

            while len(data) != size + 4:
                data += sock.recv(4096)
            sock.close()

            vfile = NamedTemporaryFile(prefix='PSB', delete=False)
            vfile.write(data[4:])
            vfile.flush()
            print(vfile.name)

            self.to_play.put(vfile.name)

MThread(to_play)

while True:
    vidFile = cv.CaptureFromFile(to_play.get())

    nFrames = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_COUNT))
    fps = cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FPS)
    waitPerFrameInMillisec = int(1/fps * 1000/1)

    print 'Num. Frames = ', nFrames
    print 'Frame Rate = ', fps, ' frames per sec'

    for f in xrange( nFrames ):
      frameImg = cv.QueryFrame( vidFile )
      cv.ShowImage("My Video Window", frameImg)
      cv.WaitKey(waitPerFrameInMillisec)

    cv.DestroyWindow( "My Video Window" )
