import asyncio

from kivy.base import async_runTouchApp
# import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

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
        # Clock.schedule_once(self.init_tcp_socket, 2)  # Adjust the delay as needed
        # Clock.schedule_once(self.init_rtsp_stream, 2)  # Adjust the delay as needed

        self.screen.ids.placeholder.text = "Initializing..."
        # asyncio.create_task(self._inf_loop())
        asyncio.create_task(self.init_tcp_socket())
        return self.screen

    async def _on_tcp_wait(self, *args):
        i = 0
        where = f"Connecting to 192.168.100.1:8888"
        while True:
            self.screen.ids.placeholder.text = f"{where}\nWaiting for device" + "." * i + " " * (3-i)
            i += 1
            if i >= 4:
                i = 0
            await asyncio.sleep(1)

    def bind_ui(self):
        zoom_btn = self.screen.ids.zoom_btn
        agc_btn = self.screen.ids.agc_btn
        color_btn = self.screen.ids.color_btn
        ffc_btn = self.screen.ids.ffc_btn
        zoom_btn.bind(on_press=lambda x: asyncio.create_task(self.on_zoom_press()))
        agc_btn.bind(on_press=lambda x: asyncio.create_task(self.on_agc_press()))
        color_btn.bind(on_press=lambda x: asyncio.create_task(self.on_color_press()))
        ffc_btn.bind(on_press=lambda x: asyncio.create_task(self.on_ffc_press()))

    async def init_tcp_socket(self):
        res = False
        while not res:
            loop_task = asyncio.create_task(self._on_tcp_wait())
            self.tcp_client = TCPClient(
                server_ip='192.168.100.1',
                server_port=8888,
                command='CMD_RTSP_TRANS_START',
            )
            # Start the TCP connection
            res = await self.tcp_client.connect()
            loop_task.cancel()
            if not res:
                self.screen.ids.placeholder.text = "Can't connect to device"
                await asyncio.sleep(1)
                self.screen.ids.placeholder.text = "Retrying..."
                await asyncio.sleep(1)

    async def on_zoom_press(self):
        await control.send(control.change_zoom())

    async def on_agc_press(self):
        await control.send(control.change_agc())

    async def on_color_press(self):
        await control.send(control.change_color_scheme())

    async def on_ffc_press(self):
        await control.send(control.send_trigger_ffc_command())

    # def init_rtsp_stream(self, dt):
    #
    #     self.rtsp_stream_widget = RTSPStream(
    #         rtsp_url='rtsp://192.168.100.1/stream0',
    #         tcp_client=self.tcp_client,
    #     )
    #
    #     self.center_column = self.screen.ids.center_column
    #     self.placeholder = self.screen.ids.placeholder
    #     self.center_column.remove_widget(self.placeholder)
    #     self.center_column.add_widget(self.rtsp_stream_widget)
    #
    # def on_stop(self):
    #     if hasattr(self, 'rtsp_stream_widget'):
    #         self.rtsp_stream_widget.on_close()


async def main():
    app = StreamApp()
    await app.async_run()


if __name__ == '__main__':
    asyncio.run(main())
