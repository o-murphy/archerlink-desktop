import asyncio
import os
from dataclasses import dataclass
from datetime import datetime

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

import control
from rtsp_stream import RTSPStream
from tcp_client import TCPClient

# import os
# os.environ["KIVY_NO_CONSOLELOG"] = "1"

Builder.load_file("gui.kv")



@dataclass
class AppState:
    tcp: bool = False
    rtsp: bool = False
    ws: bool = False


class MainScreen(Screen):
    ...


class StreamApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Archer Link"
        self.appstate = AppState()
        self.screen = MainScreen()

        self.center_column = self.screen.ids.center_column
        self.placeholder = self.screen.ids.placeholder

        self.tcp_client = TCPClient(
            server_ip=TCP_IP,
            server_port=TCP_PORT,
            command='CMD_RTSP_TRANS_START',
        )
        self.rtsp_stream_widget = RTSPStream(
            rtsp_url=RTSP_URI,
            fake=DEBUG
        )

        self.watchdog_task = None
        self.tcp_socket_task = None
        self.rtsp_texture_task = None
        self.rtsp_capture_task = None
        self.rtsp_task = None

    async def watchdog(self):
        await self.status("Initializing...")
        prev_state = AppState()
        while True:
            if self.appstate != prev_state:
                prev_state = AppState(*self.appstate.__dict__.values())
                if self.appstate.tcp and self.appstate.rtsp:
                    await self.show_stream_widget()
                elif self.appstate.tcp:
                    self.rtsp_task = asyncio.create_task(self.rtsp_init())
                    # await self.hide_stream_widget()
                else:
                    if self.rtsp_task is not None:
                        self.rtsp_task.cancel()
                    await self.hide_stream_widget()
            await asyncio.sleep(1 / 4)

    def on_start(self):
        self.bind_ui()
        self.watchdog_task = asyncio.create_task(self.watchdog())
        self.tcp_socket_task = asyncio.create_task(self.init_tcp_socket())

    async def rtsp_init(self):
        await self.rtsp_stream_widget.start_stream()
        # print("RTSP started")
        self.rtsp_capture_task = asyncio.create_task(self.rtsp_stream_widget.stream_read())
        # print("RTSP stream loop")
        self.rtsp_texture_task = asyncio.create_task(self.rtsp_stream_widget.texture_upd_loop())
        # print("RTSP texture loop")
        self.appstate.rtsp = True

    def build(self):
        self.placeholder.color = "white"
        return self.screen

    async def _waiting_msg(self, msg):
        i = 0
        while True:
            await self.status(f"{msg}" + "." * i + " " * (3 - i))
            i += 1
            if i >= 4:
                i = 0
            await asyncio.sleep(0.5)
        pass

    def bind_ui(self):
        zoom_btn = self.screen.ids.zoom_btn
        agc_btn = self.screen.ids.agc_btn
        color_btn = self.screen.ids.color_btn
        ffc_btn = self.screen.ids.ffc_btn
        shot_btn = self.screen.ids.shot_btn
        zoom_btn.bind(on_press=lambda x: asyncio.create_task(self.on_zoom_press()))
        agc_btn.bind(on_press=lambda x: asyncio.create_task(self.on_agc_press()))
        color_btn.bind(on_press=lambda x: asyncio.create_task(self.on_color_press()))
        ffc_btn.bind(on_press=lambda x: asyncio.create_task(self.on_ffc_press()))
        shot_btn.bind(on_press=lambda x: asyncio.create_task(self.on_shot_btn()))

    async def init_tcp_socket(self):

        while True:
            self.appstate.tcp = False
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

            self.appstate.tcp = True
            while self.tcp_client.sock_connected:
                # print("Check TCP")
                res = await self.tcp_client.check_socket()
                # print("TCP res:", res)
                if res is False:
                    await asyncio.sleep(1 / 5)

    async def status(self, message):
        self.placeholder.text = message

    async def on_shot_btn(self):
        outdir = os.path.join(os.path.expanduser("~"), 'Pictures', 'ArcherLink')
        os.makedirs(outdir, exist_ok=True)
        dt = datetime.now().strftime("%y%m%d-%H%M%S")
        fname = os.path.join(outdir, f"{dt}.png")
        if self.appstate.rtsp and self.appstate.tcp:
            self.rtsp_stream_widget.shot(fname)
            await self.toast(f"Photo saved to\n{fname}")

    async def toast(self, text):
        MDSnackbar(
            MDSnackbarText(
                text=text,
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()

    async def on_zoom_press(self):
        await control.change_zoom()

    async def on_agc_press(self):
        await control.change_agc()

    async def on_color_press(self):
        await control.change_color_scheme()

    async def on_ffc_press(self):
        await control.send_trigger_ffc_command()

    async def show_stream_widget(self):
        self.center_column.remove_widget(self.placeholder)
        self.center_column.add_widget(self.rtsp_stream_widget)

    async def hide_stream_widget(self):
        self.center_column.remove_widget(self.rtsp_stream_widget)
        self.center_column.add_widget(self.placeholder)

    def on_stop(self):
        if self.tcp_socket_task is not None:
            self.tcp_socket_task.cancel()
        if self.rtsp_task is not None:
            self.rtsp_task.cancel()
        self.tcp_client.close()
        self.rtsp_stream_widget.on_close()


async def main():
    app = StreamApp()
    await app.async_run()


if __name__ == '__main__':
    DEBUG = False
    if DEBUG:
        TCP_IP = '127.0.0.1'
        TCP_PORT = 8888
        WS_PORT = 8080
        WS_URI = f'ws://{TCP_IP}:{WS_PORT}/websocket'
        RTSP_URI = f'rtsp://{TCP_IP}:8554/stream'
    else:
        TCP_IP = '192.168.100.1'
        TCP_PORT = 8888
        WS_PORT = 8080
        WS_URI = f'ws://{TCP_IP}:{WS_PORT}/websocket'
        RTSP_URI = f'rtsp://{TCP_IP}/stream0'

    control.set_uri(WS_URI)

    asyncio.run(main())
