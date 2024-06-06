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

        self.center_column = self.screen.ids.center_column
        self.placeholder = self.screen.ids.placeholder

        self.status("Initializing...")


        self.tcp_client = TCPClient(
            server_ip=TCP_IP,
            server_port=TCP_PORT,
            command='CMD_RTSP_TRANS_START',
        )
        self.rtsp_stream_widget = RTSPStream(
            rtsp_url=RTSP_URI,
        )


        asyncio.create_task(self.init_tcp_socket())
        return self.screen

    async def _waiting_msg(self, msg):
        i = 0
        while True:
            await self.status(f"{msg}" + "." * i + " " * (3-i))
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


        while True:
            while not self.tcp_client.sock_connected:
                status_task = asyncio.create_task(
                    self._waiting_msg(
                        f"Connecting to {TCP_IP}:{TCP_PORT}\nWaiting for device"
                    )
                )

                # Start the TCP connection
                res = await self.tcp_client.connect()
                status_task.cancel()
                if not res:
                    await self.status("Can't connect to device")
                    print("Can't connect to device")
                    await asyncio.sleep(1)
                    await self.status("Retrying...")
                    print("Retrying...")
                    await asyncio.sleep(1)

            await self.status("Connected\nRunning RTSP stream...")

            status_task = asyncio.create_task(
                self._waiting_msg(
                    f"{RTSP_URI}\nStarting RTSP"
                )
            )
            # loop_task = asyncio.create_task(self.init_rtsp_stream())
            while self.tcp_client.sock_connected:
                res = await self.tcp_client.check_socket()
                if res is False:
                    status_task.cancel()

    async def status(self, message):
        self.placeholder.text = message

    async def on_zoom_press(self):
        await control.change_zoom()

    async def on_agc_press(self):
        await control.change_agc()

    async def on_color_press(self):
        await control.change_color_scheme()

    async def on_ffc_press(self):
        await control.send_trigger_ffc_command()

    async def init_rtsp_stream(self):
        # run stream self.rtsp_stream_widget
        ...

    async def show_stream(self):
        self.center_column.remove_widget(self.placeholder)
        self.center_column.add_widget(self.rtsp_stream_widget)

    async def hide_stream(self):
        self.center_column.remove_widget(self.rtsp_stream_widget)
        self.center_column.add_widget(self.placeholder)

    def on_stop(self):
        if hasattr(self, 'rtsp_stream_widget'):
            self.rtsp_stream_widget.on_close()


async def main():
    app = StreamApp()
    await app.async_run()


if __name__ == '__main__':
    DEBUG = True
    if DEBUG:
        TCP_IP = '127.0.0.1'
        TCP_PORT = 8888
        WS_PORT = 8080
        WS_URI = f'ws://{TCP_IP}:{WS_PORT}/websocket'
        RTSP_URI = f'rtsp://{TCP_IP}/stream0'
    else:
        TCP_IP = '192.168.100.1'
        TCP_PORT = 8888
        WS_PORT = 8080
        WS_URI = f'ws://{TCP_IP}:{WS_PORT}/websocket'
        RTSP_URI = f'rtsp://{TCP_IP}/stream0'

    control.set_uri(WS_URI)

    asyncio.run(main())
