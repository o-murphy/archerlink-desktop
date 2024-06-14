import asyncio
import logging

import av

_log = logging.getLogger('Recorder')
_log.setLevel(logging.DEBUG)


class MovRecorder:
    def __init__(self, rtsp, on_error):
        self.filename = None
        self.rtsp = rtsp
        self.recording = False
        self.output_container = None
        self._task = None
        self._error = None
        self.on_error = on_error

    async def start_async_recording(self, filename):
        self.filename = filename + '.mov'
        self.recording = True
        self._task = asyncio.create_task(self.record_loop())

    async def stop_recording(self):
        self.recording = False
        if self._task:
            await self._task
        return self.filename, self._error

    async def record_loop(self):
        self._error = None
        try:
            self.output_container = av.open(self.filename, mode='w')
            stream = self.output_container.add_stream('h264', rate=self.rtsp.fps)
            height, width, _ = self.rtsp.frame.shape
            stream.width = width
            stream.height = height
            stream.pix_fmt = 'yuv420p'

            while self.recording:
                if (frame := self.rtsp.frame) is None:
                    await asyncio.sleep(0.01)
                    continue  # Skip if no frame is available

                # Convert numpy.ndarray to av.VideoFrame
                # frame = cv2.flip(self.rtsp.frame, 0)
                frame = av.VideoFrame.from_ndarray(frame, format='bgr24')

                # Reformat the frame to match the output stream settings
                frame = frame.reformat(width=stream.width, height=stream.height, format=stream.pix_fmt)

                # Encode the frame
                packet = stream.encode(frame)

                # Write the packet to the output file
                if packet:
                    self.output_container.mux(packet)

                # Simulate a small delay to avoid blocking the event loop
                await asyncio.sleep(1 / self.rtsp.fps)

            # Flush the encoder to make sure all frames are written
            packet = stream.encode(None)
            while packet:
                self.output_container.mux(packet)
                packet = stream.encode(None)

        except av.error.EOFError:
            _log.error("End of file reached or error encountered in the stream")

        except Exception as err:
            self._error = err
            _log.exception("Recording error")

        finally:
            if self.output_container:
                self.output_container.close()
            if self._error and callable(self.on_error):
                await self.on_error()
            if self.recording:
                self.recording = False
