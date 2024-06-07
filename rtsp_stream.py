import asyncio

import cv2
import numpy as np
import time
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

_fake_frame_init_value = time.time()


def _create_fake_frame(h, w):
    et = time.time() - _fake_frame_init_value
    color = (0, 255, 0)
    f = np.zeros((w, h, 3), dtype=np.uint8)
    f[:] = color
    tl = (int((et * 50) % w), int((et * 30) % h))
    br = (tl[0] + 50, tl[1] + 50)
    cv2.rectangle(f, tl, br, (0, 0, 255), -1)
    return f


class RTSPStream(Image):
    def __init__(self, rtsp_url, fake=False, **kwargs):
        super().__init__(**kwargs)
        self.rtsp_url = rtsp_url
        self.frame = None
        self.texture = None
        self.capture = None
        self.fake = fake
        self.fps = 60

    async def texture_upd_loop(self):
        while True:
            await self.update_texture()
            await asyncio.sleep(1 / self.fps * 2)

    async def start_stream(self):
        if not self.fake:
            self.capture = cv2.VideoCapture(self.rtsp_url)
            self.fps = self.capture.get(cv2.CAP_PROP_FPS)
            print(f"Stream FPS: {self.fps}")
        self.bind(size=self.update_texture_size, pos=self.update_texture_size)

    async def stream_read(self):
        while True:
            await self.read_frame()
            await asyncio.sleep(1/self.fps)

    async def read_frame(self):
        if self.fake:
            frame = _create_fake_frame(640, 480)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            self.frame = (buf, frame.shape[1], frame.shape[0])
        else:
            ret, frame = self.capture.read()
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tobytes()
                self.frame = (buf, frame.shape[1], frame.shape[0])
            else:
                print("Failed to get frame, retrying...")
                self.capture.release()
                self.capture = cv2.VideoCapture(self.rtsp_url)

    def resize_frame(self, frame):
        # Get the dimensions of the widget
        widget_width, widget_height = self.width, self.height

        # Get the dimensions of the frame
        frame_height, frame_width = frame.shape[:2]

        # Calculate the aspect ratio of the frame
        aspect_ratio = frame_width / frame_height

        # Calculate the new dimensions while maintaining the aspect ratio
        if widget_width / widget_height > aspect_ratio:
            new_height = int(widget_height)
            new_width = int(widget_height * aspect_ratio)
        else:
            new_width = int(widget_width)
            new_height = int(widget_width / aspect_ratio)

        # Resize the frame to the new dimensions
        resized_frame = cv2.resize(frame, (new_width, new_height))
        return resized_frame

    async def update_texture(self):
        if self.frame:
            buf, width, height = self.frame
            frame = np.frombuffer(buf, dtype=np.uint8).reshape((height, width, 3))
            resized_frame = self.resize_frame(frame)

            resized_buf = resized_frame.tobytes()
            texture = Texture.create(size=(resized_frame.shape[1], resized_frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(resized_buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture
            self.canvas.ask_update()

    def update_texture_size(self, *args):
        self.texture_size = self.size

    def shot(self, filename):
        if self.frame is not None:
            buf, width, height = self.frame
            image = np.frombuffer(buf, dtype=np.uint8).reshape((height, width, 3))
            cv2.imwrite(filename, image)

    def on_close(self):
        if self.capture:
            self.capture.release()
