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

    async def prepare(self):
        self.bind(size=self.update_texture_size, pos=self.update_texture_size)
        while True:
            await self.update_texture()
            await asyncio.sleep(1 / 30)

    async def start_stream(self):
        while True:
            await self.read_frame()
            await asyncio.sleep(1 / 60)

    async def read_frame(self):
        if self.fake:
            frame = self.resize_frame(_create_fake_frame(640, 480))
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            self.frame = (buf, frame.shape[1], frame.shape[0])
        else:
            ret, frame = self.capture.read()
            if ret:
                # Resize the frame to fit the widget's size
                # frame = cv2.resize(frame, (int(self.width), int(self.height)))
                frame = self.resize_frame(frame)
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tobytes()
                self.frame = (buf, frame.shape[1], frame.shape[0])
            else:
                print("Failed to get frame, retrying...")
                self.capture.release()
                self.capture = cv2.VideoCapture(self.rtsp_url)
                # if not self.capture.isOpened():
                #     self.on_issue()

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
            texture = Texture.create(size=(width, height), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture
            self.canvas.ask_update()

    def update_texture_size(self, *args):
        self.texture_size = self.size

    def on_close(self):
        self.tcp_client.close()
        if self.capture:
            self.capture.release()
