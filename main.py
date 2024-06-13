# import faulthandler
#
# faulthandler.enable()

import asyncio

from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from modules import MovRecorder, TCPClient, RTSPClient, file_toast
from modules.control import websocket
from modules.env import *

Builder.load_file(KVGUI_PATH)
websocket.set_uri(WS_URI)


# def get_memory_usage():
#     process = psutil.Process(os.getpid())
#     mem_info = process.memory_info()
#     mem_usage_mb = mem_info.rss / 1024 / 1024  # Convert from bytes to MB
#     print(f"Current memory usage: {mem_usage_mb:.2f} MB")


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

        self.rtsp = RTSPClient(
            TCP_IP, TCP_PORT, RTSP_URI, AV_OPTIONS
        )
        self.recorder = MovRecorder(self.rtsp, self.on_record_stop)
        self._tasks = []

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
        else:
            Window.maximize()
        return self.screen

    def on_start(self):
        self.bind_ui()
        self._tasks = [
            asyncio.create_task(self.update_texture()),
            asyncio.create_task(self.rtsp.run_async())
        ]

    def adjust_frame(self, frame):
        widget_width, widget_height = self.image.width, self.image.height
        return self.rtsp.resize_frame(frame, widget_width, widget_height)

    async def update_texture(self):
        try:
            while True:
                if self.rtsp.frame is not None and self.rtsp.status == RTSPClient.Status.Running:
                    resized_frame = self.adjust_frame(self.rtsp.frame)
                    buf = resized_frame.tobytes()
                    texture = Texture.create(size=(resized_frame.shape[1], resized_frame.shape[0]), colorfmt='rgb')
                    texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
                    self.image.texture = texture
                    self.image.canvas.ask_update()
                    await self.show_stream_widget()
                    await asyncio.sleep(1 / self.rtsp.fps)
                else:
                    await self.hide_stream_widget()
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Update texture task cancelled")

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
                i += 1
                if i >= 4:
                    i = 0
                await asyncio.sleep(0.5)

        return asyncio.create_task(spinner())

    async def status(self, message):
        self.placeholder.text = message

    async def on_shot_button(self):
        filename = await get_out_filename()
        if self.rtsp.status == 'working':
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
        asyncio.run_coroutine_threadsafe(self.cleanup(), asyncio.get_event_loop())

    async def cleanup(self):
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        await asyncio.sleep(1)  # Give some time to complete the stopping process


async def main():
    app = StreamApp()
    await app.async_run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Application interrupted")
    finally:
        print("Application exit cleanup")
