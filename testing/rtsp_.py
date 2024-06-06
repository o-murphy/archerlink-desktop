import subprocess
import threading

import cv2
import  numpy as np
import time

def create_frame(w, h, color):
    f = np.zeros((w, h, 3), dtype=np.uint8)
    f[:] = color
    return f


def sim(w, h, fps):
    st = time.time()
    while True:
        et = time.time() - st
        color = (0, 255, 0)
        f = create_frame(w, h, color)

        tl = (int((et * 50) % w), int((et*30) %h))
        br = (tl[0]+50, tl[1]+50)
        cv2.rectangle(f, tl, br, (0, 0, 255), -1)
        yield f
        time.sleep(1/fps)


def start(w, h, fps, p):
    c = [
        'ffmpeg.exe',
        '-re',
        '-f',
        'rawvideo',
        '-pixel_format',
        'bgr24',
        '-video_size',
        f'{w}x{h}',
        '-framerate',
        str(fps),
        '-i',
        '-',
        '-c:v', 'libx264',
        # '-preset', 'ultrafast',
        '-f',
        'rtsp',
        f'rtsp://127.0.0.1:{p}/stream'
    ]

    pr = subprocess.Popen(c, stdin=subprocess.PIPE)

    i = 0
    for f in sim(w, h, fps):
        try:
            print(i)
            pr.stdin.write(f.tobytes())
            i += 1
        except BrokenPipeError:
            break

    pr.stdin.close()
    pr.wait()


if __name__ == '__main__':
    w, h, fps = 640, 480, 30
    p = 8554

    rt = threading.Thread(target=start, args=(w, h, fps, p))
    rt.start()

