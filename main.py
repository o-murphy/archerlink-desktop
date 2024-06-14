import asyncio
import logging

import cv2

from env import *

assert KVGUI_PATH
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from modules import MovRecorder, RTSPClient
from modules.control import websocket
from modules.toast import file_toast

_log = logging.getLogger("ArcherLink")
_log.setLevel(logging.DEBUG)

Builder.load_file(KVGUI_PATH)
websocket.set_uri(WS_URI)


class MainScreen(Screen):
    ...


class ArcherLink(MDApp):

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
        self.recorder = MovRecorder(self.rtsp, self.on_rec_stop)
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
            asyncio.create_task(self.rtsp.run_in_executor())
        ]

    async def adjust_frame(self, frame):
        widget_width, widget_height = self.image.width, self.image.height
        return await self.rtsp.resize_frame(frame, widget_width, widget_height)

    async def update_texture(self):
        try:
            while True:
                if self.rtsp.status == RTSPClient.Status.Running:
                    # print("RTSP Client Running")
                    # print(f"Frame is not None: {self.rtsp.frame is not None}")
                    if (frame := self.rtsp.frame) is not None:
                        # print("Processing frame")
                        try:
                            frame = cv2.flip(frame, 0)
                            resized_frame = await self.adjust_frame(frame)
                            # print("Frame resized")
                            buf = resized_frame.tobytes()
                            # print("Frame converted to bytes")
                            texture = Texture.create(size=(resized_frame.shape[1], resized_frame.shape[0]),
                                                     colorfmt='bgr')
                            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                            self.image.texture = texture
                            # print("Texture updated")
                            # self.image.canvas.ask_update()
                        except Exception as e:
                            _log.info(f"Error processing frame: {e}")
                        await self.show_stream_widget()
                    await asyncio.sleep(1 / self.rtsp.fps)
                else:
                    # _log.info("RTSP Client Not Running")
                    await self.hide_stream_widget()
                    await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            _log.info("Update texture task cancelled")

    async def show_stream_widget(self):
        if self.image not in self.center_column.children:
            self.center_column.remove_widget(self.placeholder)
            self.center_column.add_widget(self.image)
        # await asyncio.sleep(0)

    async def hide_stream_widget(self):
        if self.image in self.center_column.children:
            self.center_column.remove_widget(self.image)
            self.center_column.add_widget(self.placeholder)
        # await asyncio.sleep(0)

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
        filename = await get_output_filename()
        if self.rtsp.status == RTSPClient.Status.Running:
            filename = await self.rtsp.shot(filename)
            await file_toast(self, f"Photo saved to\n{filename}", filename)

    async def on_rec_stop(self):
        button = self.root.ids.rec_btn
        button.text_color = self.theme_cls.primaryColor
        button.md_bg_color = self.theme_cls.surfaceContainerColor
        filename, err = await self.recorder.stop_recording()
        if filename:
            msg = f"Video saved to\n{self.recorder.filename}"
            if not err:
                await file_toast(self, msg, self.recorder.filename)
            else:
                await file_toast(self,
                                 f"RECORDING ERROR!\n" + msg, self.recorder.filename, not not err)

    async def on_rec_start(self):
        button = self.root.ids.rec_btn
        button.text_color = self.theme_cls.errorContainerColor
        button.md_bg_color = self.theme_cls.onErrorContainerColor
        filename = await get_output_filename()
        _log.info("Starting recording")
        await self.recorder.start_async_recording(filename)

    async def on_rec_button(self):
        if not self.recorder.recording and self.rtsp.status == RTSPClient.Status.Running:
            await self.on_rec_start()
        else:
            await self.on_rec_stop()

    async def cleanup(self):
        # await self.on_rec_stop()
        for task in self._tasks:
            task.cancel()
        try:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        except asyncio.CancelledError:
            _log.info("App tasks cancelled")
        finally:
            await self.rtsp.stop()
            _log.info("All tasks finalized and resources cleaned up")

    def on_stop(self):
        asyncio.create_task(self.cleanup())


async def main():
    app = ArcherLink()
    await app.async_run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        _log.info("Application interrupted")
    finally:
        _log.info("Application exit cleanup")
