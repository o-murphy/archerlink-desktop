import asyncio
import cv2
import numpy as np
from aiortc.contrib.media import MediaPlayer
import time

class RTSPStreamer:
    def __init__(self, rtsp_uri):
        self.rtsp_uri = rtsp_uri
        self.player = None
        self.frame = None
        self.status = 'stopped'
        self._lock = asyncio.Lock()
        self._stop_event = asyncio.Event()
        self._frame_timestamps = []


    async def read_frame_with_timeout(self, timeout):
        # try:
        await asyncio.wait_for(self.read_frame(), timeout)
        # except asyncio.TimeoutError:
        #     print("Read frame timeout")

    async def read_frame(self):
        if self.player and self.player.video:
            try:
                frame = await self.player.video.recv()
                if frame:
                    img = frame.to_ndarray(format="bgr24")
                    # Convert frame from BGR to RGB
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    # Flip the frame vertically
                    self.frame = cv2.flip(img_rgb, 0)

                    # Calculate FPS
                    current_time = time.time()
                    self._frame_timestamps.append(current_time)
                    if len(self._frame_timestamps) > 10:
                        self._frame_timestamps.pop(0)

                    if len(self._frame_timestamps) > 1:
                        time_interval = self._frame_timestamps[-1] - self._frame_timestamps[0]
                        self.fps = len(self._frame_timestamps) / time_interval
                        # print(f"Calculated FPS: {fps:.2f}")
            except Exception as e:
                print(f"Error reading frame: {e}")
                raise asyncio.TimeoutError()

    async def initialize_player(self):
        self.player = MediaPlayer(self.rtsp_uri, format="rtsp", options={"rtsp_transport": "tcp", "fflags": "nobuffer"})
        # Wait for the player to initialize
        await asyncio.sleep(2)
        if not self.player.video:
            raise Exception("Failed to initialize video stream")

    async def fetch_frames(self):
        try:
            print(f"Opening RTSP stream: {self.rtsp_uri}")
            async with self._lock:
                await asyncio.wait_for(self.initialize_player(), timeout=10)  # 10-second timeout for initializing the player
            self.status = 'working'
            self.status = 'working'
            print("Entering streaming loop")
            while not self._stop_event.is_set():
                await self.read_frame_with_timeout(1)
                await asyncio.sleep(0.001)  # Small sleep to yield control
            self.status = 'stopped'
            print("Exited streaming loop")
        except Exception as e:
            self.status = f'error: {e}'
            print(f"RTSP stream error: {e}")
        finally:
            async with self._lock:
                if self.player:
                    # self.player.stop()
                    self.player = None
            print("Streaming stopped, RTSP stream closed.")
            self.frame = None
            await asyncio.sleep(1)

    async def start(self):
        self._stop_event.clear()
        await self.fetch_frames()

    async def stop(self):
        self._stop_event.set()

    def resize_frame(self, frame, width, height):
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height

        if width / height > aspect_ratio:
            new_height = int(height)
            new_width = int(height * aspect_ratio)
        else:
            new_width = int(width)
            new_height = int(width / aspect_ratio)

        resized_frame = cv2.resize(frame, (new_width, new_height))
        return resized_frame

    async def shot(self, filename):
        if self.frame is not None:
            rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(filename + '.png', rgb_frame)
            return filename + '.png'