from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import threading

class RTSPStream(Image):
    def __init__(self, rtsp_url, **kwargs):
        super().__init__(**kwargs)
        self.rtsp_url = rtsp_url
        self.frame = None
        self.texture = None
        self.capture = None
        self.stream_thread = threading.Thread(target=self.start_stream)
        self.stream_thread.daemon = True
        self.stream_thread.start()
        Clock.schedule_interval(self.update_texture, 1.0 / 30)  # Schedule update_texture to run at 30 FPS

    def start_stream(self):
        self.capture = cv2.VideoCapture(self.rtsp_url)
        while True:
            ret, frame = self.capture.read()
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tobytes()
                self.frame = (buf, frame.shape[1], frame.shape[0])
            else:
                print("Failed to get frame, retrying...")
                self.capture.release()
                self.capture = cv2.VideoCapture(self.rtsp_url)

    def update_texture(self, dt):
        if self.frame:
            buf, width, height = self.frame
            texture = Texture.create(size=(width, height), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

class StreamApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        rtsp_stream_widget = RTSPStream(rtsp_url='rtsp://192.168.100.1/stream0')
        layout.add_widget(rtsp_stream_widget)
        return layout

if __name__ == '__main__':
    StreamApp().run()
