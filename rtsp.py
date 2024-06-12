import asyncio
import socket
from enum import Enum

import av
import cv2
from aiortc.contrib.media import MediaPlayer
from aiortc.mediastreams import MediaStreamError
import logging


logging.basicConfig(level=logging.DEBUG)
_log = logging.getLogger('RTSP')
_log.setLevel(logging.DEBUG)


class RTSPClient:

    class Status(Enum):
        Running = "Running"
        Stopped = "Stopped"
        Error = "Error"

    def __init__(self, address: str, port: int = None, path: str = None,
                 options: dict = None) -> None:
        self.address = address
        self.port = port
        self.path = path
        self.options = options
        self.player: [MediaPlayer, None] = None
        self.socket: [socket, None] = None
        self.fps = 50  # default
        self.frame = None
        self.status = RTSPClient.Status.Stopped

    @property
    def url(self) -> str:
        port = self.port
        path = self.path
        return f"rtsp://{self.address}{f':{port}' if port else ''}{path if path else ''}"

    async def _get_fps(self):
        if self.player:
            container = self.player.__dict__.get("_MediaPlayer__container", None)
            if container:
                stream = container.streams.video[0]
                fps = stream.average_rate
                if fps:
                    self.fps = fps
                else:
                    _log.warning(f"Stream FPS not available, adjusted to default")
                _log.info(f"Stream FPS: {self.fps}")
            else:
                _log.info("No container available to retrieve FPS")

    async def _open(self):
        while True:
            try:
                self.socket = init_socket()
                self.player = MediaPlayer(file=self.url,
                                          format='rtsp',
                                          options=self.options,
                                          timeout=2)
                await self._get_fps()
                break
            except ConnectionError as e:
                _log.error(f"Failed to connect: {e}")
            except av.AVError as e:
                _log.error(f"Failed to connect: AVError: {e}")
            finally:
                await asyncio.sleep(1)

    async def _close(self):
        if self.player:
            self.player.video.stop()
            self.player = None
        self.frame = None
        if self.socket is not None:
            self.socket.close()
            self.socket = None
        self.status = RTSPClient.Status.Stopped

    async def _reconnect(self):
        if self.player is None:
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
                    if self.player and self.player.video:
                        frame = await self.player.video.recv()
                        if frame:
                            self.status = RTSPClient.Status.Running
                            self.frame = frame.to_ndarray(format="bgr24")
                            cv2.imshow("RTSP Stream", self.frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                        else:
                            _log.warning("No frame received")
                            self.frame = None
                        await asyncio.sleep(1 / 50)  # Allow other tasks to run
                    else:
                        raise ConnectionError("No player connected")
                except (ConnectionError, av.AVError, MediaStreamError) as e:
                    self.status = RTSPClient.Status.Error
                    _log.error(e)
                    cv2.destroyAllWindows()
                    await asyncio.sleep(2)
                    await self._reconnect()
                except Exception as e:
                    self.status = RTSPClient.Status.Error
                    _log.exception(e)
                    # cv2.destroyAllWindows()
                    # await asyncio.sleep(2)
                    # await self._reconnect()
        except asyncio.CancelledError:
            _log.debug("RTSP client canceled")
        finally:
            await self._close()
            _log.debug("RTSP client finalized")


def send_command_receive_response(command, socket):
    socket.sendall(command.encode())
    response = socket.recv(1024)  # Adjust buffer size as needed
    return response.decode()


def init_socket():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # soc.connect(('127.0.0.1', 8554))
    # # Send the command to start streaming
    # init_command = "CMD_RTSP_TRANS_START"
    # init_response = send_command_receive_response(init_command, soc)
    # print(init_response)
    # if "CMD_ACK_START_RTSP_LIVE" in init_response:
    #     return soc
    # raise Exception("Soc err")
    return soc


async def main():
    rtsp_stream = RTSPClient('127.0.0.1', 8554, '/test', {
        # 'rtsp_transport': 'tcp',
        'fflags': 'nobuffer'
    })
    task = asyncio.create_task(rtsp_stream.run_async())
    try:
        await task
    except asyncio.CancelledError:
        print("RTSP client task successfully canceled")


if __name__ == "__main__":
    asyncio.run(main())
