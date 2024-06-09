import asyncio
import time
import av
from concurrent.futures import ThreadPoolExecutor
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

    def shot(self, filename):
        if self.frame is not None:
            # buf, width, height = self.frame
            # image = np.frombuffer(buf, dtype=np.uint8).reshape((height, width, 3))
            # image = cv2.flip(image, 0)
            cv2.imwrite(filename, self.frame)

    async def fake_stream(self):
        try:
            self.fps = 60
            self.status = 'working'
            while not self._stop_event.is_set():
                frame = _create_fake_frame(480, 640)
                self.frame = frame
                await asyncio.sleep(1 / self.fps)
            self.status = 'stopped'
        except Exception as e:
            self.status = f'error: {e}'
            print(f"Fake stream error: {e}")

    async def fetch_frames(self):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            try:
                self.container = await loop.run_in_executor(pool, av.open, self.url)
                stream = self.container.streams.video[0]
                self.fps = self.container.streams.video[0].average_rate
                self.status = 'working'
                while not self._stop_event.is_set():
                    frames = await loop.run_in_executor(pool, lambda: list(self.container.decode(stream)))
                    for frame in frames:
                        if self._stop_event.is_set():
                            break
                        self.frame = frame.to_ndarray(format='bgr24')  # Convert to numpy array
                        await asyncio.sleep(1 / self.fps)
                self.status = 'stopped'
            except Exception as e:
                self.status = f'error: {e}'
                print(f"RTSP fetch error: {e}")
                if self.container:
                    self.container.close()

    async def start(self):
        self._stop_event.clear()
        if self._fake_stream:
            self._task = asyncio.create_task(self.fake_stream())
        else:
            self._task = asyncio.create_task(self.fetch_frames())

    async def stop(self):
        self._stop_event.set()
        if self._task:
            await self._task
        if self.container:
            self.container.close()
        self.status = 'stopped'
