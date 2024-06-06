# import cv2
# from kivy.uix.image import Image
# from kivy.clock import Clock
# from kivy.graphics.texture import Texture
# from tcp_client import TCPClient
#
#
# class RTSPStream(Image):
#     def __init__(self, rtsp_url, tcp_client: TCPClient, on_issue, **kwargs):
#         super().__init__(**kwargs)
#         self.rtsp_url = rtsp_url
#         self.frame = None
#         self.texture = None
#         self.capture = None
#         self.tcp_client = tcp_client
#         self.on_issue = on_issue
#
#         # Start the TCP connection
#         self.tcp_client.connect()
#
#         # Initialize the RTSP stream
#         self.start_stream()
#
#         Clock.schedule_interval(self.update_texture, 1.0 / 30)  # Schedule update_texture to run at 30 FPS
#         Clock.schedule_interval(self.check_socket, 1.0 / 5)  # Schedule check_socket to run at 10 FPS
#
#     def start_stream(self):
#         self.capture = cv2.VideoCapture(self.rtsp_url)
#         Clock.schedule_interval(self.read_frame, 1.0 / 60)  # Schedule read_frame to run at 30 FPS
#
#     def read_frame(self, dt):
#         ret, frame = self.capture.read()
#         if ret:
#             buf1 = cv2.flip(frame, 0)
#             buf = buf1.tobytes()
#             self.frame = (buf, frame.shape[1], frame.shape[0])
#         else:
#             print("Failed to get frame, retrying...")
#             self.capture.release()
#             self.capture = cv2.VideoCapture(self.rtsp_url)
#             if not self.capture.isOpened():
#                 self.on_issue()
#
#     def check_socket(self, dt):
#         if not self.tcp_client.sock_connected:
#             self.tcp_client.connect()
#             return
#
#         # Check for any data from the TCP socket
#         self.tcp_client.check_socket()
#
#     def update_texture(self, dt):
#         if self.frame:
#             buf, width, height = self.frame
#             texture = Texture.create(size=(width, height), colorfmt='bgr')
#             texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#             self.texture = texture
#
#     def on_close(self):
#         self.tcp_client.close()
#         if self.capture:
#             self.capture.release()


import cv2
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from tcp_client import TCPClient


class RTSPStream(Image):
    def __init__(self, rtsp_url, tcp_client: TCPClient, on_issue, **kwargs):
        super().__init__(**kwargs)
        self.rtsp_url = rtsp_url
        self.frame = None
        self.texture = None
        self.capture = None
        self.tcp_client = tcp_client
        self.on_issue = on_issue

        # Start the TCP connection
        self.tcp_client.connect()

        # Initialize the RTSP stream
        self.start_stream()

        Clock.schedule_interval(self.update_texture, 1.0 / 30)  # Schedule update_texture to run at 30 FPS
        Clock.schedule_interval(self.check_socket, 1.0 / 5)  # Schedule check_socket to run at 10 FPS

        # Bind the size to update when the parent size changes
        self.bind(size=self.update_texture_size, pos=self.update_texture_size)

    def start_stream(self):
        self.capture = cv2.VideoCapture(self.rtsp_url)
        Clock.schedule_interval(self.read_frame, 1.0 / 60)  # Schedule read_frame to run at 60 FPS

    def read_frame(self, dt):
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
            if not self.capture.isOpened():
                self.on_issue()

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

    def check_socket(self, dt):
        if not self.tcp_client.sock_connected:
            self.tcp_client.connect()
            return

        # Check for any data from the TCP socket
        self.tcp_client.check_socket()

    def update_texture(self, dt):
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
