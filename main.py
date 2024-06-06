import asyncio

import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

import control
from rtsp_stream import RTSPStream
from tcp_client import TCPClient

Builder.load_file("gui.kv")


class MainScreen(Screen):
    ...


class StreamApp(MDApp):

    def build(self):
        self.title = "Archer Link"
        self.screen = MainScreen()
        self.bind_ui()
        # Schedule the RTSP stream initialization
        Clock.schedule_once(self.init_rtsp_stream, 2)  # Adjust the delay as needed

        return self.screen

    def bind_ui(self):
        zoom_btn = self.screen.ids.zoom_btn
        agc_btn = self.screen.ids.agc_btn
        color_btn = self.screen.ids.color_btn
        ffc_btn = self.screen.ids.ffc_btn
        zoom_btn.bind(on_press=self.on_zoom_press)
        agc_btn.bind(on_press=self.on_agc_press)
        color_btn.bind(on_press=self.on_color_press)
        ffc_btn.bind(on_press=self.on_ffc_press)

    def on_zoom_press(self, instance):
        asyncio.run(control.send(control.change_zoom()))

    def on_agc_press(self, instance):
        asyncio.run(control.send(control.change_agc()))

    def on_color_press(self, instance):
        asyncio.run(control.send(control.change_color_scheme()))

    def on_ffc_press(self, instance):
        asyncio.run(control.send(control.send_trigger_ffc_command()))

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
