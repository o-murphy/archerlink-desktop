import asyncio
import os
from datetime import datetime

import av
import cv2
from kivy.config import Config
from kivy import platform

from rtsp import RTSPStreamer

if platform == 'win' or platform == 'linux':
    Config.set('graphics', 'maxfps', '120')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

import control
from tcp_client import TCPClient

Builder.load_file("gui.kv")

class MainScreen(Screen):
    ...

class StreamApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Archer Link"
        self.screen = MainScreen()

        self.center_column = self.screen.ids.center_column
        self.placeholder = self.screen.ids.placeholder
        self.image = Image()

        self.tcp = TCPClient(
            server_ip=TCP_IP,
            server_port=TCP_PORT,
            command='CMD_RTSP_TRANS_START',
        )
        self.rtsp = RTSPStreamer(RTSP_URI, DEBUG)

        self.watchdog_task = None
        self.tcp_socket_task = None
        self.texture_task = None
        self.rtsp_task = None

        self.record = False

    async def watchdog(self):
        await self.status("Initializing...")
        while True:
            # print(f"TCP connected: {self.tcp.sock_connected}, RTSP status: {self.rtsp.status}")

            if self.tcp.sock_connected:
                if self.rtsp.status != 'working' and not self.rtsp_task:
                    print("Starting RTSP stream")
                    self.rtsp_task = asyncio.create_task(self.start_stream())
                elif self.rtsp.status == 'working' and self.rtsp_task:
                    await self.show_stream_widget()
                # elif self.rtsp.status != 'working' and self.rtsp_task:
                #     await self.on_stream_fallthrough()
                #     self.rtsp_task = None
                else:
                    pass
                    # print("Unexpected stream error")
                    # print(f"TCP connected: {self.tcp.sock_connected}, RTSP status: {self.rtsp.status}")
                    # await self.on_stream_fallthrough()
            else:
                await self.on_stream_fallthrough()
            await asyncio.sleep(1 / 4)

    def on_start(self):
        self.bind_ui()
        self.watchdog_task = asyncio.create_task(self.watchdog())
        self.tcp_socket_task = asyncio.create_task(self.init_tcp_socket())

    def resize_frame(self, frame):
        # Get the dimensions of the widget
        widget_width, widget_height = self.image.width, self.image.height

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

    async def update_texture(self):
        print("Updating texture task")

        while True:
            if self.rtsp.frame is not None:
                # print("Updating texture")
                frame = self.rtsp.frame
                resized_frame = self.resize_frame(frame)  # Resize frame to widget size
                buf = resized_frame.tobytes()
                texture = Texture.create(size=(resized_frame.shape[1], resized_frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.image.texture = texture
                self.image.canvas.ask_update()
                # print("Texture updated")
            # else:
                # print("No frame to update")
            await asyncio.sleep(1 / self.rtsp.fps)

    async def on_stream_fallthrough(self):
        await self.stop_stream()
        # await self.tcp.close()
        await self.hide_stream_widget()
        await self.status("RTSP stream lost\ntrying to restart...")
        await asyncio.sleep(1)

    async def start_stream(self):
        await self.rtsp.start()
        self.texture_task = asyncio.create_task(self.update_texture())

    async def stop_stream(self):
        if self.rtsp.status == 'working':
            await self.rtsp.stop()
        if self.rtsp_task:
            self.rtsp_task.cancel()
            self.rtsp_task = None
        if self.texture_task:
            self.texture_task.cancel()
            self.texture_task = None

    async def show_stream_widget(self):
        if self.image not in self.center_column.children:
            self.center_column.remove_widget(self.placeholder)
            self.center_column.add_widget(self.image)
        await asyncio.sleep(0)

    async def hide_stream_widget(self):
        if self.image in self.center_column.children:
            self.center_column.remove_widget(self.image)
            self.center_column.add_widget(self.placeholder)
        await asyncio.sleep(0)

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Khaki'
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "800"

        Window.minimum_width = 700
        Window.minimum_height = 400
        Window.size = (700, 400)
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
        rec_btn = self.screen.ids.rec_btn
        zoom_btn.bind(on_press=lambda x: asyncio.create_task(self.on_zoom_press()))
        agc_btn.bind(on_press=lambda x: asyncio.create_task(self.on_agc_press()))
        color_btn.bind(on_press=lambda x: asyncio.create_task(self.on_color_press()))
        ffc_btn.bind(on_press=lambda x: asyncio.create_task(self.on_ffc_press()))
        shot_btn.bind(on_press=lambda x: asyncio.create_task(self.on_shot_btn()))
        rec_btn.bind(on_press=lambda x: asyncio.create_task(self.on_rec_btn()))

    async def init_tcp_socket(self):
        while True:
            while not self.tcp.sock_connected:
                status_task = asyncio.create_task(
                    self._waiting_msg(
                        f"Connecting to {TCP_IP}:{TCP_PORT}\nWaiting for device"
                    )
                )
                res = await self.tcp.connect()
                status_task.cancel()
                if not res:
                    await self.status("Can't connect to device")
                    await asyncio.sleep(1)
                    await self.status("Retrying...")
                    await asyncio.sleep(1)

            while self.tcp.sock_connected:
                await self.tcp.check_socket()
                # if res is False:
                await asyncio.sleep(5)

    async def status(self, message):
        self.placeholder.text = message

    async def get_out_filename(self):
        outdir = os.path.join(os.path.expanduser("~"), 'Pictures', 'ArcherLink')
        os.makedirs(outdir, exist_ok=True)
        dt = datetime.now().strftime("%y%m%d-%H%M%S")
        return os.path.join(outdir, f"{dt}")

    async def on_shot_btn(self):
        fname = await self.get_out_filename()
        if self.rtsp.status == 'working' and self.tcp.sock_connected:
            self.rtsp.shot(fname + '.png')
            await self.toast(f"Photo saved to\n{fname}")

    async def start_rec(self):
        fname = await self.get_out_filename()
        self.output_container = av.open(fname + '.mov', mode='w')
        stream = self.output_container.add_stream('h264', rate=self.rtsp.fps)
        height, width, _ = self.rtsp.frame.shape
        stream.width = width
        stream.height = height
        stream.pix_fmt = 'yuv420p'

        try:
            while self.record:
                # Simulate a small delay to avoid blocking the event loop
                await asyncio.sleep(1 / self.rtsp.fps)

                if self.rtsp.frame is None:
                    continue  # Skip if no frame is available

                # Convert numpy.ndarray to av.VideoFrame
                frame = cv2.flip(self.rtsp.frame, 0)
                frame = av.VideoFrame.from_ndarray(frame, format='rgb24')

                # Reformat the frame to match the output stream settings
                frame = frame.reformat(width=stream.width, height=stream.height, format=stream.pix_fmt)

                # Encode the frame
                packet = stream.encode(frame)

                # Write the packet to the output file
                if packet:
                    self.output_container.mux(packet)

            # Flush the encoder to make sure all frames are written
            packet = stream.encode(None)
            while packet:
                self.output_container.mux(packet)
                packet = stream.encode(None)

        except av.error.EOFError:
            print("End of file reached or error encountered in the stream")

        finally:
            self.output_container.close()
            if self.record:
                self.record = False
                await self.on_rec_btn()

    async def on_rec_btn(self):
        button = self.root.ids.rec_btn
        icon = self.root.ids.rec_btn_icon
        if not self.record:
            button.color_map = "tertiary"
            icon.text_color = self.theme_cls.onErrorColor
            self.record = True
            self.rec_task = asyncio.create_task(self.start_rec())
        else:
            button.color_map = "surface"
            icon.text_color = self.theme_cls.primaryColor
            self.record = False
            await self.rec_task

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

    def on_stop(self):
        if self.tcp_socket_task is not None:
            self.tcp_socket_task.cancel()
        if self.rtsp._task is not None:
            self.rtsp._task.cancel()
        self.tcp.close()


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
        RTSP_URI = f'rtsp://{TCP_IP}:8554/'
    else:
        TCP_IP = '192.168.100.1'
        TCP_PORT = 8888
        WS_PORT = 8080
        WS_URI = f'ws://{TCP_IP}:{WS_PORT}/websocket'
        RTSP_URI = f'rtsp://{TCP_IP}/stream0'

    control.set_uri(WS_URI)

    asyncio.run(main())
