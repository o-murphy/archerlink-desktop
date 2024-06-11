import asyncio
import os
import subprocess
from datetime import datetime

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import cv2
from kivy.config import Config
from kivy import platform

import sys
from kivy.resources import resource_add_path

from modules import MovRecorder, RTSPStreamer, file_toast
from modules.control import websocket

if platform == 'win' or platform == 'linux':
    Config.set('graphics', 'maxfps', '120')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from modules.tcp import TCPClient

os.environ["KIVY_NO_CONSOLELOG"] = "1"
# os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
ICO_PATH = 'icon.png'
KVGUI_PATH = "gui.kv"
CONFIG_PATH = "config.toml"

if platform == 'win':
    OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "AppData", "Local", "ArcherLink")
else:
    OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Pictures", 'ArcherLink')
os.makedirs(OUTPUT_DIR, exist_ok=True)


async def get_out_filename():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dt = datetime.now().strftime("%y%m%d-%H%M%S")
    return os.path.join(OUTPUT_DIR, f"{dt}")


async def open_output_dir():
    if sys.platform == "win32":
        os.startfile(OUTPUT_DIR)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", OUTPUT_DIR])
    else:
        subprocess.Popen(["xdg-open", OUTPUT_DIR])


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
        self.rtsp = RTSPStreamer(
            RTSP_URI,
            False
        )
        self.recorder = MovRecorder(self.rtsp, self.on_record_stop)

        self._tasks = None

    def bind_ui(self):
        self.screen.ids.zoom_btn.bind(on_press=lambda x: asyncio.create_task(websocket.change_zoom()))
        self.screen.ids.agc_btn.bind(on_press=lambda x: asyncio.create_task(websocket.change_agc()))
        self.screen.ids.color_btn.bind(on_press=lambda x: asyncio.create_task(websocket.change_color_scheme()))
        self.screen.ids.ffc_btn.bind(on_press=lambda x: asyncio.create_task(websocket.send_trigger_ffc_command()))
        self.screen.ids.shot_btn.bind(on_press=lambda x: asyncio.create_task(self.on_shot_button()))
        self.screen.ids.rec_btn.bind(on_press=lambda x: asyncio.create_task(self.on_rec_button()))
        self.screen.ids.folder_btn.bind(on_press=lambda x: asyncio.create_task(open_output_dir()))

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = 'Khaki'
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = "800"

        Window.set_icon(ICO_PATH)
        Window.minimum_width = 700
        Window.minimum_height = 400

        if DEBUG:
            Window.size = (700, 400)
            # Window.fullscreen = 'auto'
            # Window.borderless = True
        else:
            Window.maximize()
        return self.screen

    def on_start(self):
        self.bind_ui()
        self._tasks = asyncio.gather(
            asyncio.create_task(self.tcp_polling()),
            asyncio.create_task(self.update_texture()),
            asyncio.create_task(self.rtsp_stream_task())  # Added RTSP stream task
        )

    async def rtsp_stream_task(self):
        while True:
            if self.rtsp.status != 'working':
                print("RTSP stream error detected or stopped, attempting to restart")
                await self.rtsp.start()
            await asyncio.sleep(2)

    def resize_frame(self, frame):
        widget_width, widget_height = self.image.width, self.image.height
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height

        if widget_width / widget_height > aspect_ratio:
            new_height = int(widget_height)
            new_width = int(widget_height * aspect_ratio)
        else:
            new_width = int(widget_width)
            new_height = int(widget_width / aspect_ratio)

        resized_frame = cv2.resize(frame, (new_width, new_height))
        return resized_frame

    async def update_texture(self):
        while True:
            if self.rtsp.frame is not None:
                await self.show_stream_widget()
                resized_frame = self.resize_frame(self.rtsp.frame)
                buf = resized_frame.tobytes()
                texture = Texture.create(size=(resized_frame.shape[1], resized_frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                self.image.texture = texture
                self.image.canvas.ask_update()
                await asyncio.sleep(1 / self.rtsp.fps)
            else:
                await self.hide_stream_widget()
                await asyncio.sleep(1)

    async def start_stream(self):
        await self.rtsp.start()

    async def stop_stream(self):
        if self.rtsp.status == 'working':
            await self.rtsp.stop()
        self.tcp.close()

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

    async def spinn_message(self, msg):
        async def spinner():
            i = 0
            while True:
                await self.status(f"{msg}" + "." * i + " " * (3 - i))
                i += 1
                if i >= 4:
                    i = 0
                await asyncio.sleep(0.5)

        return asyncio.create_task(spinner())

    async def status(self, message):
        self.placeholder.text = message

    async def tcp_polling(self):
        while True:
            while not self.tcp.sock_connected:
                status_task = await self.spinn_message(
                    f"Connecting to {TCP_IP}:{TCP_PORT}\nWaiting for device"
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
                await asyncio.sleep(5)

    async def on_shot_button(self):
        filename = await get_out_filename()
        if self.rtsp.status == 'working' and self.tcp.sock_connected:
            filename = await self.rtsp.shot(filename)
            await file_toast(f"Photo saved to\n{filename}", filename)

    async def start_recording(self):
        fname = await get_out_filename()
        await self.recorder.start_async_recording(fname)

    async def on_record_stop(self):
        button = self.root.ids.rec_btn
        icon = self.root.ids.rec_btn_icon
        button.color_map = "surface"
        icon.text_color = self.theme_cls.primaryColor
        filename, err = await self.recorder.stop_recording()
        if not err:
            await file_toast(f"Video saved to\n{self.recorder.filename}", filename)

    async def on_rec_button(self):
        button = self.root.ids.rec_btn
        icon = self.root.ids.rec_btn_icon
        if not self.recorder.recording:
            button.color_map = "tertiary"
            icon.text_color = self.theme_cls.onErrorColor
            await self.start_recording()
        else:
            await self.on_record_stop()

    def on_stop(self):
        asyncio.create_task(self.cleanup())

    async def cleanup(self):
        await self.stop_stream()
        await asyncio.sleep(1)  # Give some time to complete the stopping process

async def main():
    app = StreamApp()
    await app.async_run()

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
        ICO_PATH = os.path.join(sys._MEIPASS, ICO_PATH)
        KVGUI_PATH = os.path.join(sys._MEIPASS, KVGUI_PATH)
        CONFIG_PATH = os.path.join(sys._MEIPASS, CONFIG_PATH)

    Config.set('kivy', 'window_icon', ICO_PATH)
    Builder.load_file(KVGUI_PATH)

    with open(CONFIG_PATH, 'rb') as fp:
        cfg = tomllib.load(fp)

    DEBUG = cfg.get('DEBUG', False)

    SERVER = cfg['debug-server' if DEBUG else 'server']

    TCP_IP = SERVER['TCP_IP']
    TCP_PORT = SERVER['TCP_PORT']
    WS_PORT = SERVER['WS_PORT']
    WS_URI = SERVER['WS_URI'].format(TCP_IP=TCP_IP, WS_PORT=WS_PORT)
    RTSP_URI = SERVER['RTSP_URI'].format(TCP_IP=TCP_IP)
    websocket.set_uri(WS_URI)

    if DEBUG:
        from modules import debug
        debug.open_tcp(TCP_IP, TCP_PORT)
        debug.open_vlc(RTSP_URI)

    asyncio.run(main())
