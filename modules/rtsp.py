import asyncio
import logging
import socket
import subprocess
import sys
from enum import Enum

import av
import cv2
from aiortc.contrib.media import MediaPlayer
from aiortc.mediastreams import MediaStreamError

logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger('RTSP')
_log.setLevel(logging.DEBUG)


class RTSPClient:
    class Status(Enum):
        Running = "Running"
        Stopped = "Stopped"
        Error = "Error"

    def __init__(self, host: str = None, port: int = None, uri: str = None,
                 options: dict = None) -> None:
        self.host = host
        self.port = port
        self.rtsp_uri = uri
        self.options = options
        self.__player: [MediaPlayer, None] = None
        self.__socket: [socket, None] = None
        self.__fps = 50  # default
        self.__frame = None
        self.__status = RTSPClient.Status.Stopped

    @property
    def frame(self):
        return self.__frame

    @property
    def status(self):
        return self.__status

    @property
    def fps(self):
        return self.__fps

    @property
    def _player(self):
        return self.__player

    @property
    def _socket(self):
        return self.__socket

    async def _get_stream_fps(self):
        if self.__player:
            container = self.__player.__dict__.get("_MediaPlayer__container", None)
            if container:
                stream = container.streams.video[0]
                fps = stream.average_rate
                if fps:
                    self.__fps = fps
                else:
                    _log.warning(f"Stream FPS not available, adjusted to default")
                _log.info(f"Stream FPS: {self.__fps}")
            else:
                _log.info("No container available to retrieve FPS")

    async def _open(self):
        while True:
            try:
                if self.host and self.port:
                    self.__socket = init_socket(self.host, self.port)
                self.__player = MediaPlayer(file=self.rtsp_uri,
                                            format='rtsp',
                                            options=self.options,
                                            timeout=2)
                await self._get_stream_fps()
                break
            except TimeoutError as e:
                _log.error(e)
            except ConnectionError as e:
                _log.error(f"Failed to connect: {e}")
            except av.AVError as e:
                _log.error(f"Failed to connect: AVError: {e}")
            finally:
                await asyncio.sleep(1)

    async def _close(self):
        if self.__player:
            self.__player.video.stop()
            self.__player = None
        self.__frame = None
        if self.__socket is not None:
            self.__socket.close()
            self.__socket = None
        self.__status = RTSPClient.Status.Stopped

    async def _reconnect(self):
        if self.__player is None:
            _log.info("Connecting...")
        else:
            _log.info("Connection lost, Reconnecting...")
        await self._close()
        await self._open()  # Attempt to reconnect

    async def run_async(self):
        try:
            _log.info("Running RTSP client")
            await self._reconnect()
            while True:
                try:
                    if self.__player and self.__player.video:
                        frame = await self.__player.video.recv()
                        if frame:
                            self.__status = RTSPClient.Status.Running
                            self.__frame = frame.to_ndarray(format="bgr24")
                            # cv2.imshow("RTSP Stream", self.__frame)
                            # if cv2.waitKey(1) & 0xFF == ord('q'):
                            #     break
                        else:
                            _log.warning("No frame received")
                            self.__frame = None
                        await asyncio.sleep(0)  # Allow other tasks to run without delay
                        continue
                    else:
                        raise ConnectionError("No player connected")
                except (ConnectionError, av.AVError, MediaStreamError) as e:
                    self.__status = RTSPClient.Status.Error
                    _log.error(f"{e.__class__.__name__}: {e}")
                except Exception as e:
                    self.__status = RTSPClient.Status.Error
                    _log.exception(e)
                # cv2.destroyAllWindows()
                await asyncio.sleep(2)
                await self._reconnect()
        except asyncio.CancelledError:
            _log.debug("RTSP client canceled")
        finally:
            await self._close()
            _log.debug("RTSP client finalized")

    @staticmethod
    def resize_frame(frame, width, height):
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


def send_command_receive_response(command, socket):
    socket.sendall(command.encode())
    response = socket.recv(1024)  # Adjust buffer size as needed
    return response.decode()


def init_socket(host, port):
    if not ping(host):
        raise ConnectionError("Host is not reachable")
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((host, port))
    # Send the command to start streaming
    init_command = "CMD_RTSP_TRANS_START"
    init_response = send_command_receive_response(init_command, soc)
    print(init_response)
    if "CMD_ACK_START_RTSP_LIVE" in init_response:
        return soc
    raise Exception("Soc err")


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    param = '-n' if sys.platform == 'win32' else '-c'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    # Redirect output and error streams to DEVNULL to suppress them
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        stdout, stderr = process.communicate()
        return process.returncode == 0


async def main():
    rtsp_stream = RTSPClient('192.168.100.1', 8888, 'rtsp://192.168.100.1/stream0', {
    # rtsp_stream = RTSPClient(None, None, 'rtsp://127.0.0.1:8554/test', {
        'rtsp_transport': 'udp',  # Use UDP transport for lower latency
        'fflags': 'nobuffer',
        'max_delay': '500000',  # 500ms max delay
        'tune': 'zerolatency',
        'analyzeduration': '0',  # Skip analysis for lower latency
        'probesize': '32'  # Lower probe size for faster start
    })
    task = asyncio.create_task(rtsp_stream.run_async())
    try:
        await task
    except asyncio.CancelledError:
        _log.debug("RTSP client task successfully canceled")
    finally:
        _log.debug("RTSP client task successfully finished")


if __name__ == "__main__":
    asyncio.run(main())
