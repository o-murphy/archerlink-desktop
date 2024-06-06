import socket

import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout


class RTSPStream(Image):
    def __init__(self, rtsp_url, server_ip, server_port, command, **kwargs):
        super().__init__(**kwargs)
        self.rtsp_url = rtsp_url
        self.server_ip = server_ip
        self.server_port = server_port
        self.command = command
        self.frame = None
        self.texture = None
        self.capture = None
        self.sock = None

        # Initialize and start the TCP connection
        self.send_command_to_tcp_server()

        # Initialize the RTSP stream
        self.start_stream()

        Clock.schedule_interval(self.update_texture, 1.0 / 30)  # Schedule update_texture to run at 30 FPS
        Clock.schedule_interval(self.check_socket, 1.0 / 10)  # Schedule check_socket to run at 10 FPS

    def send_command_to_tcp_server(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect the socket to the server's port
            server_address = (self.server_ip, self.server_port)
            print(f"Connecting to {self.server_ip} port {self.server_port}")
            self.sock.connect(server_address)

            # Send the command
            print(f"Sending: {self.command}")
            self.sock.sendall(self.command.encode())

            # Set the socket to non-blocking mode
            self.sock.setblocking(False)

        except Exception as e:
            print(f"Failed to connect or send command: {e}")

    def start_stream(self):
        self.capture = cv2.VideoCapture(self.rtsp_url)
        Clock.schedule_interval(self.read_frame, 1.0 / 60)  # Schedule read_frame to run at 30 FPS

    def read_frame(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            self.frame = (buf, frame.shape[1], frame.shape[0])
        else:
            print("Failed to get frame, retrying...")
            self.capture.release()
            self.capture = cv2.VideoCapture(self.rtsp_url)

    def check_socket(self, dt):
        # Check for any data from the TCP socket
        try:
            response = self.sock.recv(1024)
            if response:
                print(f"Received: {response.decode()}")
        except BlockingIOError:
            # No data received, continue
            pass

    def update_texture(self, dt):
        if self.frame:
            buf, width, height = self.frame
            texture = Texture.create(size=(width, height), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

    def on_close(self):
        if self.sock:
            self.sock.close()
        if self.capture:
            self.capture.release()


class StreamApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        rtsp_stream_widget = RTSPStream(
            rtsp_url='rtsp://192.168.100.1/stream0',
            server_ip='192.168.100.1',
            server_port=8888,
            command='CMD_RTSP_TRANS_START'
        )
        layout.add_widget(rtsp_stream_widget)
        return layout

    def on_stop(self):
        self.root.children[0].on_close()


if __name__ == '__main__':
    StreamApp().run()
