import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import av
import cv2
import numpy as np

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


class RTSPStreamer:
    def __init__(self, url, fake_stream=True):
        self.url = url
        self.container = None
        self.fps = 60
        self.frame = None
        self.status = 'stopped'
        self._stop_event = asyncio.Event()
        self._task = None
        self._fake_stream = fake_stream

        self.executor = ThreadPoolExecutor(max_workers=1)

    def shot(self, filename):
        if self.frame is not None:
            cv2.imwrite(filename, self.frame)

    async def fake_stream(self):
        until_err = 5
        try:
            self.fps = 60
            self.status = 'working'
            while not self._stop_event.is_set():
                frame = _create_fake_frame(480, 640)
                self.frame = frame
                await asyncio.sleep(1 / self.fps)
                until_err -= 1 / self.fps
                if until_err <= 0:
                    raise IOError("Simulate stream drop down")
            self.status = 'stopped'
        except Exception as e:
            self.status = f'error: {e}'
            print(f"Fake stream error: {e}")

    async def read_frame_with_timeout(self, timeout=5):
        retries = 5
        loop = asyncio.get_running_loop()
        while retries > 0:
            try:
                await asyncio.wait_for(loop.run_in_executor(self.executor, self.read_frame), timeout)
            except asyncio.TimeoutError:
                self.frame = None
            retries -= 1
        if self.frame is None:
            raise asyncio.TimeoutError("RSTP stream lost")

    def read_frame(self):
        for packet in self.container.demux():
            if packet.stream.type == 'video':
                for frame in packet.decode():
                    img = frame.to_image()
                    frame_array = np.array(img)
                    self.frame = cv2.flip(frame_array, 0)
                    return
        print("No video packet found")

    async def fetch_frames(self):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            try:
                print("Opening container")
                self.container = await loop.run_in_executor(pool, av.open, self.url)
                self.fps = self.container.streams.video[0].average_rate
                self.status = 'working'
                print("Entering streaming loop")
                print(f"Stop event is set: {self._stop_event.is_set()}")

                if self._stop_event.is_set():
                    print("Stop event was set before entering the loop.")
                    return
                while not self._stop_event.is_set():
                    await self.read_frame_with_timeout(1)
                    await asyncio.sleep(1 / self.fps)
                self.status = 'stopped'
                print("Exited streaming loop")
            except Exception as e:
                self.status = f'error: {e}'
                print(f"RTSP stream error: {e}")
            finally:
                if self.container:
                    self.container.close()
                print("Streaming stopped, container closed.")

    async def start(self):
        self._stop_event.clear()
        print("Starting stream, stop event cleared.")
        print(f"Stop event is set after clear: {self._stop_event.is_set()}")
        if self._fake_stream:
            self._task = asyncio.create_task(self.fake_stream())
        else:
            self._task = asyncio.create_task(self.fetch_frames())

    async def stop(self):
        print("Stopping stream, stop event set.")
        self._stop_event.set()
        print(f"Stop event is set in stop: {self._stop_event.is_set()}")
        if self._task:
            print("Awaiting task to finish")
            await self._task
        if self.container:
            self.container.close()
        self.status = 'stopped'
        print("Stream fully stopped.")
