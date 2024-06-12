import asyncio
import socket

import av
import cv2
from aiortc.contrib.media import MediaPlayer

class RTSPVideoStream:
    def __init__(self, url):
        self.url = url
        self.player = None
        self.connection_lost_handler = None

    async def connect(self):
        while True:
            try:
                self.player = MediaPlayer(self.url,
                                          'rtsp',
                                          {'rtsp_transport': 'tcp', 'fflags': 'nobuffer'},
                                          2)
                # await self.player.start()
                break
            except ConnectionError as e:
                print("Failed to connect:", e)
                await asyncio.sleep(2)  # Retry after 5 seconds
            except av.AVError as e:
                print("Failed to connect:", e)
                await asyncio.sleep(2)  # Retry after 5 seconds

    async def handle_stream(self):
        print("Handle")
        while True:
            soc = None
            try:
                soc = init_socket()
                if self.player and self.player.video:
                    frame = await self.player.video.recv()
                    if frame:
                        frame = frame.to_ndarray(format="bgr24")
                        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # frame = cv2.flip(frame, 0)
                        cv2.imshow("RTSP Stream", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    else:
                        print("No frame received")
                    await asyncio.sleep(1/50)  # Allow other tasks to run
                else:
                    raise ConnectionError("No player connected")
            except (ConnectionError, av.AVError) as e:
                print("Connection lost:", e)
                # if self.connection_lost_handler:
                #     await self.connection_lost_handler()
                await self.connect()  # Attempt to reconnect
            finally:
                if soc:
                    soc.close()


def send_command_receive_response(command, socket):
    socket.sendall(command.encode())
    response = socket.recv(1024)  # Adjust buffer size as needed
    return response.decode()

def init_socket():
    init_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    init_socket.connect(('192.168.100.1', 8888))
    # Send the command to start streaming
    init_command = "CMD_RTSP_TRANS_START"
    init_response = send_command_receive_response(init_command, init_socket)

    if "CMD_ACK_START_RTSP_LIVE" in init_response:
        return init_socket
    raise Exception("Soc err")

async def main():
    print("TCP OK")
    url = "rtsp://192.168.100.1/stream0"
    rtsp_stream = RTSPVideoStream(url=url)
    # await rtsp_stream.connect()

    # Start handling the stream
    await rtsp_stream.handle_stream()  # Change to await here

if __name__ == "__main__":
    asyncio.run(main())
