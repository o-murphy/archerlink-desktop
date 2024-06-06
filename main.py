from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from rtsp_stream import RTSPStream
from tcp_client import TCPClient

Builder.load_file("gui.kv")


class MainScreen(Screen):
    ...


class StreamApp(MDApp):

    def build(self):
        self.title = "Archer Link"
        self.screen = MainScreen()

        # Schedule the RTSP stream initialization
        Clock.schedule_once(self.init_rtsp_stream, 2)  # Adjust the delay as needed

        return self.screen

    def on_sock_issue(self):
        raise ConnectionError("Socket closed")

    def on_rtsp_issue(self):
        raise ConnectionError("RTSP stream closed")

    def init_rtsp_stream(self, dt):
        self.tcp_client = TCPClient(
            server_ip='192.168.100.1',
            server_port=8888,
            command='CMD_RTSP_TRANS_START',
            on_issue=self.on_sock_issue
        )

        self.rtsp_stream_widget = RTSPStream(
            rtsp_url='rtsp://192.168.100.1/stream0',
            tcp_client=self.tcp_client,
            on_issue=self.on_rtsp_issue
        )

        self.center_column = self.screen.ids.center_column
        self.placeholder = self.screen.ids.placeholder
        self.center_column.remove_widget(self.placeholder)
        self.center_column.add_widget(self.rtsp_stream_widget)

    def on_stop(self):
        if hasattr(self, 'rtsp_stream_widget'):
            self.rtsp_stream_widget.on_close()


if __name__ == '__main__':
    StreamApp().run()
