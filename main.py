import asyncio
import os
from dataclasses import dataclass
from datetime import datetime

from kivy.config import Config
from kivy.core.window import Window
from kivy import platform
if platform == 'win' or platform == 'linux':
    Config.set('graphics', 'maxfps', '120')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

import control
from rtsp_stream_av import RTSPStream
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
            fake=DEBUG,
            on_conn_lost=self.conn_lost
        )

        self.watchdog_task = None
        self.tcp_socket_task = None
        # self.rtsp_texture_task = None
        # self.rtsp_capture_task = None
        self.rtsp_task = None

    # async def upd_framerate(self):
    #     while True:
    #         self.screen.ids.framerate.text = str(round(Clock.get_fps(), 2))
    #         await asyncio.sleep(1/30)

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
        # asyncio.create_task(self.upd_framerate())
        self.watchdog_task = asyncio.create_task(self.watchdog())
        self.tcp_socket_task = asyncio.create_task(self.init_tcp_socket())

    async def rtsp_init(self):
        await self.rtsp_stream_widget.start_stream()
        self.appstate.rtsp = True

    async def conn_lost(self):
        self.appstate.rtsp = False

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Khaki'
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "800"

        # ['Aliceblue', 'Antiquewhite', 'Aqua', 'Aquamarine', 'Azure',
        # 'Beige', 'Bisque', 'Black', 'Blanchedalmond', 'Blue', 'Blueviolet',
        # 'Brown', 'Burlywood', 'Cadetblue', 'Chartreuse', 'Chocolate',
        # 'Coral', 'Cornflowerblue', 'Cornsilk', 'Crimson', 'Cyan', 'Darkblue',
        # 'Darkcyan', 'Darkgoldenrod', 'Darkgray', 'Darkgrey', 'Darkgreen', 'Darkkhaki',
        # 'Darkmagenta', 'Darkolivegreen', 'Darkorange', 'Darkorchid', 'Darkred', 'Darksalmon',
        # 'Darkseagreen', 'Darkslateblue', 'Darkslategray', 'Darkslategrey', 'Darkturquoise', 'Darkviolet',
        # 'Deeppink', 'Deepskyblue', 'Dimgray', 'Dimgrey', 'Dodgerblue', 'Firebrick', 'Floralwhite',
        # 'Forestgreen', 'Fuchsia', 'Gainsboro', 'Ghostwhite', 'Gold', 'Goldenrod', 'Gray',
        # 'Grey', 'Green', 'Greenyellow', 'Honeydew', 'Hotpink', 'Indianred',
        # 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'Lavenderblush', 'Lawngreen',
        # 'Lemonchiffon', 'Lightblue', 'Lightcoral', 'Lightcyan', 'Lightgoldenrodyellow',
        # 'Lightgreen', 'Lightgray', 'Lightgrey', 'Lightpink', 'Lightsalmon', 'Lightseagreen',
        # 'Lightskyblue', 'Lightslategray', 'Lightslategrey', 'Lightsteelblue', 'Lightyellow',
        # 'Lime', 'Limegreen', 'Linen', 'Magenta', 'Maroon', 'Mediumaquamarine', 'Mediumblue',
        # 'Mediumorchid', 'Mediumpurple', 'Mediumseagreen', 'Mediumslateblue', 'Mediumspringgreen',
        # 'Mediumturquoise', 'Mediumvioletred', 'Midnightblue', 'Mintcream', 'Mistyrose',
        # 'Moccasin', 'Navajowhite', 'Navy', 'Oldlace', 'Olive', 'Olivedrab', 'Orange', 'Orangered',
        # 'Orchid', 'Palegoldenrod', 'Palegreen', 'Paleturquoise', 'Palevioletred', 'Papayawhip',
        # 'Peachpuff', 'Peru', 'Pink', 'Plum', 'Powderblue', 'Purple', 'Red', 'Rosybrown',
        # 'Royalblue', 'Saddlebrown', 'Salmon', 'Sandybrown', 'Seagreen', 'Seashell', 'Sienna', 'Silver', 'Skyblue', 'Slateblue', 'Slategray', 'Slategrey', 'Snow', 'Springgreen', 'Steelblue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise',
        # 'Violet', 'Wheat', 'White', 'Whitesmoke', 'Yellow', 'Yellowgreen']

        # self.placeholder.color = "white"
        # self.screen.ids.framerate.color = "white"

        Window.minimum_width = 700
        Window.minimum_height = 400
        # Set initial window size
        Window.size = (700, 400)

        # Bind the on_resize event to the handle_resize function
        # Window.bind(on_resize=self.handle_resize)
        return self.screen

    # def handle_resize(self, *args):
    #     if Window.height > Window.width:
    #         self.screen.ids.main_layout.orientation = 'vertical'
    #         self.screen.ids.right_column.orientation = 'horizontal'
    #         self.screen.ids.left_column.orientation = 'horizontal'
    #     else:
    #         self.screen.ids.main_layout.orientation = 'horizontal'
    #         self.screen.ids.right_column.orientation = 'vertical'
    #         self.screen.ids.left_column.orientation = 'vertical'

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
                    await asyncio.sleep(5)
            # self.tcp_client.close()

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
