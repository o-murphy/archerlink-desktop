import asyncio
import time
import av
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import os
import cv2

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "timeout;5000"  # 5 seconds

_fake_frame_init_value = time.time()

def _create_fake_frame(h, w):
    et = time.time() - _fake_frame_init_value
    color = (0, 255, 0)
    f = np.zeros((h, w, 3), dtype=np.uint8)
    f[:] = color
    tl = (int((et * 50) % w), int((et * 30) % h))
    br = (tl[0] + 50, tl[1] + 50)
    cv2.rectangle(f, tl, br, (0, 0, 255), -1)
    return f

class RTSPStream(Image):
    def __init__(self, rtsp_url, fake=False, on_conn_lost=None, **kwargs):
        super().__init__(**kwargs)
        self.rtsp_url = rtsp_url
        self.frame = None
        self.texture = None
        self.container = None
        self.fake = fake
        self.fps = 60
        self.initial_frames_to_skip = 60 * 3  # Number of initial frames to skip

        self.stream_read_task = None
        self.texture_task = None
        self.on_conn_lost = on_conn_lost

    async def texture_upd_loop(self):
        while True:
            await self.update_texture()
            await asyncio.sleep(1 / self.fps * 2)
            # await asyncio.sleep(1 / Clock.get_fps() * 2)

    async def start_stream(self):
        if not self.fake:
            self.container = av.open(self.rtsp_url)
            self.fps = self.container.streams.video[0].average_rate
            print(f"Stream FPS: {self.fps}")
            await self.warm_up_capture()
        self.bind(size=self.update_texture_size, pos=self.update_texture_size)
        self.stream_read_task = asyncio.create_task(self.stream_read())
        self.texture_task = asyncio.create_task(self.texture_upd_loop())

    async def warm_up_capture(self):
        # Read and discard a few initial frames to warm up the capture
        for _ in range(self.initial_frames_to_skip):
            if self.container:
                for frame in self.container.decode(video=0):
                    break
                await asyncio.sleep(0.01)  # Small delay to simulate frame reading time

    async def stream_read(self):
        while True:
            await self.read_frame_with_timeout(1 / self.fps)
            await asyncio.sleep(1 / self.fps)

    async def read_frame_with_timeout(self, timeout):
        try:
            await asyncio.wait_for(self.read_frame(), timeout)
        except asyncio.TimeoutError:
            print("Timeout while reading frame.")
            await self.handle_stream_error()

    async def read_frame(self):
        if self.fake:
            frame = _create_fake_frame(640, 480)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            self.frame = (buf, frame.shape[1], frame.shape[0])
        else:
            try:
                for packet in self.container.demux():
                    if packet.stream.type == 'video':
                        for frame in packet.decode():
                            img = frame.to_image()
                            frame = np.array(img)
                            buf1 = cv2.flip(frame, 0)
                            buf = buf1.tobytes()
                            # buf = frame.tobytes()
                            self.frame = (buf, frame.shape[1], frame.shape[0])
                            return
            except Exception as e:
                print(f"Error reading frame: {e}")
                await self.handle_stream_error()

    async def handle_stream_error(self):
        print("Stream error encountered. Attempting to reconnect...")
        if self.container:
            self.container.close()
        await asyncio.sleep(1)  # Wait for a second before retrying
        self.container = av.open(self.rtsp_url)
        if not self.container:
            print("Failed to reconnect to the stream.")
            if self.on_conn_lost:
                await self.on_conn_lost()

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
            texture = Texture.create(size=(resized_frame.shape[1], resized_frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(resized_buf, colorfmt='rgb', bufferfmt='ubyte')
            self.texture = texture
            self.canvas.ask_update()

    def update_texture_size(self, *args):
        self.texture_size = self.size

    def shot(self, filename):
        if self.frame is not None:
            buf, width, height = self.frame
            image = np.frombuffer(buf, dtype=np.uint8).reshape((height, width, 3))
            image = cv2.flip(image, 0)
            cv2.imwrite(filename, image)

    def on_close(self):
        if self.container:
            self.container.close()
